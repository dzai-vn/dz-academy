#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import uuid
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable
from urllib import error, parse, request


IMAGE_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".svg",
    ".avif",
    ".ico",
}
TEXT_SUFFIXES = {
    ".qmd",
    ".md",
    ".html",
    ".yml",
    ".yaml",
    ".json",
    ".webmanifest",
}
EXCLUDED_DIRS = {".git", ".github", ".quarto", "docs", "__pycache__"}
PUBLIC_ID_PREFIX = "dz-academy"
HEAD_BLOCK_START = "<!-- BEGIN CLOUDINARY MANAGED ASSETS -->"
HEAD_BLOCK_END = "<!-- END CLOUDINARY MANAGED ASSETS -->"
MARKDOWN_PATTERN = re.compile(r"(?P<prefix>!\[[^\]]*\]\()(?P<target>[^)]+)(?P<suffix>\))")
HTML_ATTR_PATTERN = re.compile(
    r"(?P<prefix>\b(?:src|href|content)\s*=\s*[\"'])(?P<target>[^\"']+)(?P<suffix>[\"'])"
)
JSON_SRC_PATTERN = re.compile(r'(?P<prefix>"src"\s*:\s*")(?P<target>[^"]+)(?P<suffix>")')
YAML_LOGO_PATTERN = re.compile(r"(?m)^(?P<prefix>\s*logo:\s*)(?P<target>\S+)(?P<suffix>\s*)$")
DATA_BRAND_PATH_PATTERN = re.compile(
    r'(?P<prefix>\bdata-brand-assets-path\s*=\s*[\"\'])(?P<target>[^\"\']+)(?P<suffix>[\"\'])'
)


@dataclass(frozen=True)
class Asset:
    relative_path: str
    absolute_path: Path
    public_id: str
    url: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Upload site images to Cloudinary, rewrite source references, and remove local image binaries."
    )
    parser.add_argument(
        "--repo-root",
        default=Path(__file__).resolve().parents[1],
        type=Path,
        help="Path to the dz-academy repo root.",
    )
    parser.add_argument(
        "--cloud-name",
        default=os.environ.get("CLOUDINARY_CLOUD_NAME", ""),
        help="Cloudinary cloud name. Defaults to CLOUDINARY_CLOUD_NAME.",
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("CLOUDINARY_API_KEY", ""),
        help="Cloudinary API key. Defaults to CLOUDINARY_API_KEY.",
    )
    parser.add_argument(
        "--api-secret",
        default=os.environ.get("CLOUDINARY_API_SECRET", ""),
        help="Cloudinary API secret. Defaults to CLOUDINARY_API_SECRET.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would change without uploading, rewriting, or deleting files.",
    )
    parser.add_argument(
        "--keep-local-images",
        action="store_true",
        help="Do not delete local source images or docs copies after a live rewrite. Useful for local testing.",
    )
    return parser.parse_args()


def to_posix(path: Path) -> str:
    return PurePosixPath(path).as_posix()


def is_absolute_reference(value: str) -> bool:
    return (
        value.startswith("http://")
        or value.startswith("https://")
        or value.startswith("//")
        or value.startswith("data:")
        or value.startswith("mailto:")
        or value.startswith("#")
    )


def asset_public_id(relative_path: str) -> str:
    rel = PurePosixPath(relative_path)
    without_suffix = rel.with_suffix("")
    return to_posix(Path(PUBLIC_ID_PREFIX) / Path(str(without_suffix)))


def asset_url(cloud_name: str, relative_path: str) -> str:
    suffix = PurePosixPath(relative_path).suffix.lower()
    if suffix not in IMAGE_SUFFIXES:
        raise ValueError(f"Unsupported image suffix for {relative_path}")
    public_id = asset_public_id(relative_path)
    quoted = parse.quote(public_id, safe="/")
    return f"https://res.cloudinary.com/{cloud_name}/image/upload/{quoted}{suffix}"


def directory_url(cloud_name: str, relative_directory: str) -> str:
    path = to_posix(Path(PUBLIC_ID_PREFIX) / Path(relative_directory))
    return f"https://res.cloudinary.com/{cloud_name}/image/upload/{parse.quote(path, safe='/')}"


def iter_source_files(repo_root: Path) -> Iterable[Path]:
    for path in repo_root.rglob("*"):
        if not path.is_file():
            continue
        parts = set(path.relative_to(repo_root).parts)
        if parts & EXCLUDED_DIRS:
            continue
        yield path


def discover_images(repo_root: Path, cloud_name: str) -> dict[str, Asset]:
    assets: dict[str, Asset] = {}
    for path in iter_source_files(repo_root):
        if path.suffix.lower() not in IMAGE_SUFFIXES:
            continue
        relative_path = to_posix(path.relative_to(repo_root))
        assets[relative_path] = Asset(
            relative_path=relative_path,
            absolute_path=path,
            public_id=asset_public_id(relative_path),
            url=asset_url(cloud_name, relative_path),
        )
    return dict(sorted(assets.items()))


def discover_text_files(repo_root: Path) -> list[Path]:
    files: list[Path] = []
    for path in iter_source_files(repo_root):
        if path.suffix.lower() in TEXT_SUFFIXES:
            files.append(path)
    return sorted(files)


def build_signature(params: dict[str, str], api_secret: str) -> str:
    payload = "&".join(f"{key}={params[key]}" for key in sorted(params))
    return hashlib.sha1(f"{payload}{api_secret}".encode("utf-8")).hexdigest()


def build_multipart_form(fields: dict[str, str], file_path: Path) -> tuple[bytes, str]:
    boundary = f"----codex-{uuid.uuid4().hex}"
    file_bytes = file_path.read_bytes()
    lines: list[bytes] = []
    for key, value in fields.items():
        lines.extend(
            [
                f"--{boundary}".encode("utf-8"),
                f'Content-Disposition: form-data; name="{key}"'.encode("utf-8"),
                b"",
                value.encode("utf-8"),
            ]
        )
    lines.extend(
        [
            f"--{boundary}".encode("utf-8"),
            f'Content-Disposition: form-data; name="file"; filename="{file_path.name}"'.encode("utf-8"),
            b"Content-Type: application/octet-stream",
            b"",
            file_bytes,
            f"--{boundary}--".encode("utf-8"),
            b"",
        ]
    )
    body = b"\r\n".join(lines)
    return body, boundary


def upload_asset(asset: Asset, cloud_name: str, api_key: str, api_secret: str) -> None:
    timestamp = str(int(time.time()))
    signed_params = {
        "invalidate": "true",
        "overwrite": "true",
        "public_id": asset.public_id,
        "timestamp": timestamp,
        "unique_filename": "false",
        "use_filename": "false",
    }
    signature = build_signature(signed_params, api_secret)
    fields = {
        **signed_params,
        "api_key": api_key,
        "signature": signature,
    }
    body, boundary = build_multipart_form(fields, asset.absolute_path)
    endpoint = f"https://api.cloudinary.com/v1_1/{cloud_name}/image/upload"
    req = request.Request(
        endpoint,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        with request.urlopen(req) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Cloudinary upload failed for {asset.relative_path}: {detail}") from exc
    if payload.get("public_id") != asset.public_id:
        raise RuntimeError(f"Unexpected Cloudinary public_id for {asset.relative_path}: {payload}")


def resolve_path(file_path: Path, target: str, repo_root: Path) -> Path:
    clean = target.split("?", 1)[0].split("#", 1)[0]
    if clean.startswith("/"):
        return repo_root / clean.lstrip("/")
    return (file_path.parent / clean).resolve()


def replace_matches(
    content: str,
    pattern: re.Pattern[str],
    resolver,
    change_log: list[str],
    file_label: str,
) -> str:
    def repl(match: re.Match[str]) -> str:
        target = match.group("target")
        replacement = resolver(target)
        if replacement is None or replacement == target:
            return match.group(0)
        change_log.append(f"{file_label}: {target} -> {replacement}")
        return f"{match.group('prefix')}{replacement}{match.group('suffix')}"

    return pattern.sub(repl, content)


def rewrite_quarto_logo(content: str, repo_root: Path, asset_map: dict[str, Asset]) -> tuple[str, bool]:
    changed = False

    def repl(match: re.Match[str]) -> str:
        nonlocal changed
        target = match.group("target").strip()
        if is_absolute_reference(target):
            return match.group(0)
        resolved = resolve_path(repo_root / "_quarto.yml", target, repo_root)
        rel = to_posix(resolved.relative_to(repo_root))
        asset = asset_map.get(rel)
        if asset is None:
            return match.group(0)
        changed = True
        return f"{match.group('prefix')}{asset.url}{match.group('suffix')}"

    return YAML_LOGO_PATTERN.sub(repl, content), changed


def rewrite_brand_asset_path(
    content: str,
    file_path: Path,
    repo_root: Path,
    directory_map: dict[str, str],
) -> tuple[str, bool]:
    changed = False

    def repl(match: re.Match[str]) -> str:
        nonlocal changed
        target = match.group("target")
        if is_absolute_reference(target):
            return match.group(0)
        resolved = resolve_path(file_path, target, repo_root)
        try:
            relative_directory = to_posix(resolved.relative_to(repo_root))
        except ValueError:
            return match.group(0)
        replacement = directory_map.get(relative_directory)
        if replacement is None:
            return match.group(0)
        changed = True
        return f"{match.group('prefix')}{replacement}{match.group('suffix')}"

    return DATA_BRAND_PATH_PATTERN.sub(repl, content), changed


def manage_head_file(content: str, asset_map: dict[str, Asset]) -> str:
    favicon = asset_map["assets/website/light/favicon.svg"].url
    apple_touch = asset_map["assets/website/light/apple-touch-icon.png"].url
    managed_block = "\n".join(
        [
            HEAD_BLOCK_START,
            f'<link rel="icon" type="image/svg+xml" href="{favicon}">',
            f'<link rel="apple-touch-icon" href="{apple_touch}">',
            '<link rel="manifest" href="/assets/website/site.webmanifest">',
            HEAD_BLOCK_END,
        ]
    )
    block_pattern = re.compile(
        rf"{re.escape(HEAD_BLOCK_START)}.*?{re.escape(HEAD_BLOCK_END)}",
        flags=re.DOTALL,
    )
    if block_pattern.search(content):
        return block_pattern.sub(managed_block, content)
    script_index = content.find("<script>")
    if script_index >= 0:
        return f"{content[:script_index]}{managed_block}\n{content[script_index:]}"
    return f"{content.rstrip()}\n{managed_block}\n"


def manage_manifest_file(content: str, asset_map: dict[str, Asset]) -> str:
    manifest = json.loads(content)
    for icon in manifest.get("icons", []):
        src = icon.get("src")
        if not isinstance(src, str) or is_absolute_reference(src):
            continue
        resolved = resolve_path(Path("assets/website/site.webmanifest"), src, Path(".").resolve())
        rel = to_posix(Path("assets/website") / Path(src))
        asset = asset_map.get(rel)
        if asset is not None:
            icon["src"] = asset.url
    return json.dumps(manifest, ensure_ascii=True, indent=2) + "\n"


def generic_rewrite(
    file_path: Path,
    content: str,
    repo_root: Path,
    asset_map: dict[str, Asset],
    change_log: list[str],
) -> str:
    relative_label = to_posix(file_path.relative_to(repo_root))

    def resolver(target: str) -> str | None:
        if is_absolute_reference(target):
            return None
        resolved = resolve_path(file_path, target, repo_root)
        try:
            relative = to_posix(resolved.relative_to(repo_root))
        except ValueError:
            return None
        asset = asset_map.get(relative)
        if asset is None:
            return None
        return asset.url

    content = replace_matches(content, MARKDOWN_PATTERN, resolver, change_log, relative_label)
    content = replace_matches(content, HTML_ATTR_PATTERN, resolver, change_log, relative_label)
    content = replace_matches(content, JSON_SRC_PATTERN, resolver, change_log, relative_label)
    return content


def validate_remaining_local_refs(
    text_files: dict[Path, str],
    repo_root: Path,
    asset_map: dict[str, Asset],
    directory_map: dict[str, str],
) -> list[str]:
    issues: list[str] = []
    tracked_assets = set(asset_map)
    tracked_directories = set(directory_map)
    for file_path, content in text_files.items():
        if file_path.suffix.lower() not in {".qmd", ".md", ".html", ".yml", ".yaml", ".json", ".webmanifest"}:
            continue
        for pattern in (MARKDOWN_PATTERN, HTML_ATTR_PATTERN, JSON_SRC_PATTERN, YAML_LOGO_PATTERN, DATA_BRAND_PATH_PATTERN):
            for match in pattern.finditer(content):
                target = match.group("target")
                if is_absolute_reference(target):
                    continue
                resolved = resolve_path(file_path, target, repo_root)
                try:
                    relative = to_posix(resolved.relative_to(repo_root))
                except ValueError:
                    continue
                if relative in tracked_assets:
                    issues.append(f"{to_posix(file_path.relative_to(repo_root))}: unreplaced asset reference {target}")
                if relative in tracked_directories:
                    issues.append(f"{to_posix(file_path.relative_to(repo_root))}: unreplaced asset directory {target}")
    return issues


def write_text_file(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    cloud_name = args.cloud_name.strip()
    api_key = args.api_key.strip()
    api_secret = args.api_secret.strip()

    if not repo_root.exists():
        print(f"Repo root does not exist: {repo_root}", file=sys.stderr)
        return 1
    if not cloud_name:
        print("Missing Cloudinary cloud name. Set CLOUDINARY_CLOUD_NAME or pass --cloud-name.", file=sys.stderr)
        return 1
    if not args.dry_run and (not api_key or not api_secret):
        print(
            "Missing Cloudinary credentials. Set CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET for a live run.",
            file=sys.stderr,
        )
        return 1

    asset_map = discover_images(repo_root, cloud_name)
    if not asset_map:
        print("No source image files found. Nothing to sync.")
        return 0

    directory_map = {
        "assets/01-logos/master": directory_url(cloud_name, "assets/01-logos/master"),
    }
    text_file_paths = discover_text_files(repo_root)
    text_files = {path: path.read_text(encoding="utf-8") for path in text_file_paths}
    change_log: list[str] = []

    for path, original_content in list(text_files.items()):
        content = original_content
        relative = to_posix(path.relative_to(repo_root))
        content = generic_rewrite(path, content, repo_root, asset_map, change_log)
        if relative == "_quarto.yml":
            content, changed = rewrite_quarto_logo(content, repo_root, asset_map)
            if changed:
                change_log.append("_quarto.yml: updated navbar logo to Cloudinary URL")
        if relative == "assets/_head.html":
            managed = manage_head_file(content, asset_map)
            if managed != content:
                content = managed
                change_log.append("assets/_head.html: refreshed managed Cloudinary head assets block")
        if relative == "assets/website/site.webmanifest":
            managed = manage_manifest_file(content, asset_map)
            if managed != content:
                content = managed
                change_log.append("assets/website/site.webmanifest: refreshed icon URLs")
        content, changed = rewrite_brand_asset_path(content, path, repo_root, directory_map)
        if changed:
            change_log.append(f"{relative}: updated data-brand-assets-path to Cloudinary base URL")
        text_files[path] = content

    validation_issues = validate_remaining_local_refs(text_files, repo_root, asset_map, directory_map)
    if validation_issues:
        print("Validation failed. Remaining local image references detected:", file=sys.stderr)
        for issue in validation_issues:
            print(f"- {issue}", file=sys.stderr)
        return 1

    mode = "DRY RUN" if args.dry_run else "LIVE RUN"
    print(f"[{mode}] Assets discovered: {len(asset_map)}")
    for asset in asset_map.values():
        print(f"- {asset.relative_path} -> {asset.url}")
    if change_log:
        print(f"[{mode}] Rewrites planned: {len(change_log)}")
        for entry in change_log:
            print(f"- {entry}")
    else:
        print(f"[{mode}] No source rewrites needed.")

    if args.dry_run:
        print(f"[{mode}] No uploads, file writes, or deletions executed.")
        return 0

    for asset in asset_map.values():
        upload_asset(asset, cloud_name, api_key, api_secret)

    for path, content in text_files.items():
        original = path.read_text(encoding="utf-8")
        if content != original:
            write_text_file(path, content)

    deleted = 0
    docs_deleted = 0
    if args.keep_local_images:
        print(f"[{mode}] Uploaded {len(asset_map)} assets and kept local image files for testing.")
        return 0

    for asset in asset_map.values():
        asset.absolute_path.unlink()
        deleted += 1
        docs_copy = repo_root / "docs" / Path(asset.relative_path)
        if docs_copy.exists():
            docs_copy.unlink()
            docs_deleted += 1

    print(
        f"[{mode}] Uploaded {len(asset_map)} assets, deleted {deleted} source image files, and removed {docs_deleted} docs copies."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

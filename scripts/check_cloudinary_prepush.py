#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from sync_cloudinary_assets import (
    DATA_BRAND_PATH_PATTERN,
    HTML_ATTR_PATTERN,
    IMAGE_SUFFIXES,
    JSON_SRC_PATTERN,
    MARKDOWN_PATTERN,
    YAML_LOGO_PATTERN,
    discover_images,
    discover_text_files,
    is_absolute_reference,
    resolve_path,
    to_posix,
)


DEFAULT_MAX_BYTES = 10 * 1024 * 1024
REFERENCE_PATTERNS = (
    MARKDOWN_PATTERN,
    HTML_ATTR_PATTERN,
    JSON_SRC_PATTERN,
    YAML_LOGO_PATTERN,
    DATA_BRAND_PATH_PATTERN,
)


def looks_like_local_asset_reference(pattern, target: str) -> bool:
    if pattern is DATA_BRAND_PATH_PATTERN:
        return True
    clean = target.split("?", 1)[0].split("#", 1)[0].strip()
    return Path(clean).suffix.lower() in IMAGE_SUFFIXES


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Pre-push checks for Cloudinary sync readiness."
    )
    parser.add_argument(
        "--repo-root",
        default=Path(__file__).resolve().parents[1],
        type=Path,
        help="Path to the dz-academy repo root.",
    )
    parser.add_argument(
        "--cloud-name",
        default="precheck",
        help="Placeholder cloud name used to simulate asset discovery.",
    )
    parser.add_argument(
        "--max-bytes",
        default=DEFAULT_MAX_BYTES,
        type=int,
        help="Maximum allowed source image size in bytes. Defaults to 10 MB.",
    )
    return parser.parse_args()


def find_oversized_assets(repo_root: Path, cloud_name: str, max_bytes: int) -> list[str]:
    issues: list[str] = []
    asset_map = discover_images(repo_root, cloud_name)
    for asset in asset_map.values():
        size = asset.absolute_path.stat().st_size
        if size > max_bytes:
            issues.append(f"{asset.relative_path} ({size} bytes > {max_bytes} bytes)")
    return issues


def find_broken_local_references(repo_root: Path) -> list[str]:
    issues: list[str] = []
    for file_path in discover_text_files(repo_root):
        relative_file = to_posix(file_path.relative_to(repo_root))
        content = file_path.read_text(encoding="utf-8")
        for pattern in REFERENCE_PATTERNS:
            for match in pattern.finditer(content):
                target = match.group("target").strip()
                if is_absolute_reference(target):
                    continue
                if not looks_like_local_asset_reference(pattern, target):
                    continue
                try:
                    resolved = resolve_path(file_path, target, repo_root)
                except Exception as exc:  # pragma: no cover - defensive
                    issues.append(f"{relative_file}: could not resolve {target} ({exc})")
                    continue
                try:
                    relative_resolved = resolved.relative_to(repo_root)
                except ValueError:
                    continue
                if not resolved.exists():
                    issues.append(
                        f"{relative_file}: missing local asset {target} -> {to_posix(relative_resolved)}"
                    )
    return sorted(set(issues))


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    if not repo_root.exists():
        print(f"Repo root does not exist: {repo_root}")
        return 1

    oversized = find_oversized_assets(repo_root, args.cloud_name, args.max_bytes)
    broken_refs = find_broken_local_references(repo_root)

    if oversized:
        print("Cloudinary pre-push check failed: oversized image assets detected.")
        for issue in oversized:
            print(f"- {issue}")

    if broken_refs:
        if oversized:
            print()
        print("Cloudinary pre-push check failed: broken local image references detected.")
        for issue in broken_refs:
            print(f"- {issue}")

    if oversized or broken_refs:
        return 1

    print("Cloudinary pre-push check passed.")
    print(f"- repo: {repo_root}")
    print(f"- max image size: {args.max_bytes} bytes")
    print("- no oversized source images")
    print("- no broken local image references")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

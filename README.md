# DZ Quarto Academy

Thư mục này giữ nguyên cấu trúc Quarto foundation, nhưng nội dung đã được căn theo bộ tham chiếu tại `dz-channel/branding/docs/ref/quarto` và chốt riêng cho `DZ AI Academy`.

## Mục đích

Đây là bộ Quarto runnable để:

- render website tĩnh từ `qmd`, `md`, `ipynb`
- thử nghiệm website cho nội dung training, tutorial, notebook lesson
- map guideline thương hiệu `dz-academy` vào đúng insertion points của Quarto

## Cơ chế render

Bộ này bám cùng một cơ chế với tài liệu tham chiếu:

- Quarto đọc `_quarto.yml` làm entry point duy nhất
- source có thể là `qmd`, `md`, `ipynb`
- notebook dùng `freeze: auto`
- Quarto inject `theme`, `navbar`, `footer`, `include-in-header`, `include-after-body`
- output cuối cùng đi vào `docs/`

## Mapping với `docs/ref/quarto`

- `_quarto.yml`: bám title, description, navbar, footer, site-url, và format defaults của bộ tham chiếu, nhưng được chốt riêng cho `DZ AI Academy`
- `assets/dz-tokens.css`: dùng cùng token layer
- `assets/styles.scss`: là component layer mở rộng cho suite này
- `assets/_head.html`: web package hooks cho favicon, manifest, OG image
- `assets/_dz-init.html`: runtime init cho theme toggle và `data-bs-theme`

## Render

Chạy từ thư mục này:

```bash
quarto render
```

Output:

```text
docs/
```

## Cloudinary publish

Workflow publish tren GitHub da duoc mo rong theo huong:

- push len `main`
- GitHub Actions doc 3 secrets `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`
- chay `scripts/sync_cloudinary_assets.py`
- upload image source len Cloudinary theo path on dinh
- rewrite source sang Cloudinary URLs
- xoa binary image local khoi repo
- render lai `docs/`
- bot commit nguoc source + `docs/` voi `[skip ci]`

Neu muon xem truoc pham vi thay doi ma chua upload/xoa file, chay:

```bash
python3 scripts/sync_cloudinary_assets.py --dry-run --cloud-name <your-cloud-name>
```

Truoc khi push code, nen chay precheck:

```bash
python3 scripts/check_cloudinary_prepush.py
```

Script nay se fail neu:

- co image source vuot gioi han size hien tai cua Cloudinary mac dinh (`10 MB`)
- co local image reference khong resolve duoc

Neu can doi nguong size kiem tra:

```bash
python3 scripts/check_cloudinary_prepush.py --max-bytes 10485760
```

Neu muon test local voi Cloudinary nhung chua xoa image local, chay:

```bash
export CLOUDINARY_CLOUD_NAME=...
export CLOUDINARY_API_KEY=...
export CLOUDINARY_API_SECRET=...
python3 scripts/sync_cloudinary_assets.py --keep-local-images
quarto preview
```

Luu y:

- Script chi dong bo image source, khong dua CSS/JS len Cloudinary.
- `check_cloudinary_prepush.py` la buoc gate don gian truoc khi push, de tranh fail CI vi asset size hoac broken local refs.
- `--keep-local-images` phu hop cho local test: source duoc rewrite sang Cloudinary URL nhung image local van duoc giu lai.
- Sau lan migration thanh cong dau tien, image binary cua site se duoc bot xoa khoi repo; source text va `docs/` van duoc giu.

## Thành phần chính

- `_metadata.yml`: mặc định chung cho toàn site academy
- `index.qmd`: trang chủ của `DZ AI Academy`
- `about.qmd`: trang giới thiệu người viết và định hướng nội dung
- `tutorials/`: sample notebook/tutorial flow
- `posts/`, `demos/`, `roadmap/`: các section chính của site academy
- `assets/code-notebook.css`: lớp CSS riêng cho các page code-heavy trong `tutorials/`

## Ghi chú

Mục tiêu của thư mục này không phải tạo một theme HTML rời, mà là chứng minh cách đưa guideline vào đúng lớp cấu hình và asset của Quarto.

Kiến trúc hiện tại là `academy-only`, nên không còn giữ preset metadata riêng cho `core` hoặc `news`.

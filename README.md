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

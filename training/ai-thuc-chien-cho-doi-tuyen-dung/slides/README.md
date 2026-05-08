# AI Training HR Presentation Package

Thư mục này là bản đóng gói để zip và gửi cho học viên.

## Cách dùng

- Mở file `index.html`
- Nếu gửi cho học viên, zip nguyên thư mục `presentation/`
- Không đổi cấu trúc thư mục con `assets/`

## Cấu trúc

- `index.html`: file presentation chính
- `assets/`: CSS, JS, logo để presentation chạy độc lập
- `media/`: nơi để ảnh, video, PDF hoặc tài liệu đính kèm thêm cho học viên

## Flashcard component

Deck này đã có sẵn một component flashcard để nhúng vào các slide paged.

- CSS: `assets/flashcard.css`
- JS: `assets/flashcard.js`
- Slide mẫu: `#flashcard-concepts`

### Cách tích hợp vào slide khác

1. Giữ 2 file `flashcard.css` và `flashcard.js` trong package.
2. Trong `head`, load `./assets/flashcard.css`.
3. Trước `core.js`, load `./assets/flashcard.js`.
4. Ở page cần dùng, thêm một container:

```html
<div class="dz-flashcard dz-flashcard--embedded" data-dz-flashcard>
  <script type="application/json" class="dz-flashcard__data">
    {
      "title": "Thẻ AI",
      "sourcesLabel": "Based on 4 concepts",
      "revealLabel": "See answer",
      "hideLabel": "Hide answer",
      "hintLabel": "Click card hoặc bấm Enter để lật thẻ",
      "cards": [
        {
          "term": "Interface",
          "answer": "Nơi bạn tương tác với AI."
        }
      ]
    }
  </script>
</div>
```

### Hành vi mặc định

- Click card hoặc bấm `Enter` / `Space` để lật mặt trước và mặt sau
- `←` / `→` khi focus trong widget để chuyển thẻ
- Nút đỏ / xanh để đánh dấu chưa nhớ / đã nhớ
- Điểm nhớ được giữ trong phạm vi page hiện tại, không lưu lâu dài

### Khi nào nên dùng

- Ôn khái niệm ở giữa buổi học
- Chèn mini drill sau một phần lý thuyết
- Gửi handout để học viên tự lật thẻ khi mở file HTML

## Ghi chú

- `core.css` hiện đang dùng Google Fonts qua `@import`, nên để hiển thị đúng font cần có Internet
- Nếu cần bản chạy hoàn toàn offline, cần đóng gói thêm font cục bộ

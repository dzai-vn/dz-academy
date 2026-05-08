# Training Structure

Mỗi khoá học trong `training/` nên theo cùng một cấu trúc:

```text
training/
  index.qmd
  <course-slug>/
    index.qmd
    slides/
      index.html
      assets/
      media/
    materials/
    examples/
```

## Quy ước

- `index.qmd` ở cấp `training/`: landing page cho toàn bộ thư viện khoá học
- `training/<course-slug>/index.qmd`: landing page riêng cho từng khoá
- `slides/`: HTML presentation publish trực tiếp
- `materials/`: workbook, handout, checklist
- `examples/`: skill demo, sample files, datasets

## Mục tiêu

- publish được từng khoá học lên GitHub Pages
- dễ thêm khoá mới mà không phá cấu trúc cũ
- giữ rõ ranh giới giữa landing page, slide deck, và tài liệu đi kèm

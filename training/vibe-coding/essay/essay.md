---
title: "10 Đồ Án Cuối Khóa Vibe Coding với BMAD Method"
description: "Danh sách 10 đồ án CRUD cho nhân viên văn phòng Việt Nam trong khóa Vibe Coding với BMAD Method"
author: "Duy NHM"
tags: ["BMAD_COURSE"]
---

# 10 Đồ Án Cuối Khóa "Vibe Coding với BMAD Method" — Web App CRUD cho Nhân Viên Văn Phòng

## TL;DR
- **10 đồ án CRUD được thiết kế chuyên biệt cho nhân viên văn phòng Việt Nam**, mỗi project giải quyết một pain point thực tế của Excel/Google Sheets thủ công (mất dữ liệu, không phân quyền, không thông báo, không tìm kiếm nhanh, không tracking lịch sử) và phù hợp hoàn thiện trong 1–2 ngày vibe coding với AI agent.
- **Mỗi project có 2 phương án triển khai miễn phí**: (a) Web App Next.js/React + Vercel (dùng Supabase free tier hoặc SQLite/JSON file) hoặc (b) "Spreadsheet App" Google Sheets + Apps Script Web App — không server, không chi phí, không authentication phức tạp.
- **Cấu trúc BMAD nhất quán cho cả 10 đồ án**: Module 1 (Mindset) → Module 2 (PRD 1 trang) → Module 3 (Epics + User Stories, mỗi spec tập trung 1 nhiệm vụ) → Module 4 (vibe code với Claude Code, Antigravity) → Module 5 (AI review + QA test case). Không có project nào tích hợp AI **bên trong** sản phẩm — AI chỉ là công cụ xây.

---

## Key Findings

### Pain point chung của nhân viên văn phòng Việt Nam (đúc kết từ khảo sát thị trường)
Khi tìm hiểu các bài viết của 1Office, MISA AMIS, FastWork, Base.vn, ITG Technology, VietFul và Brands Vietnam, có 7 "nỗi đau" lặp đi lặp lại khi dùng Excel/Google Sheets thủ công:

1. **Nhiều người nhập cùng lúc → trùng/mất dữ liệu** (file Excel local), hoặc xung đột chỉnh sửa (Google Sheets shared).
2. **Không phân quyền theo vai trò** — ai mở file cũng xem/sửa được mọi cột, dễ rò rỉ lương, hợp đồng, công nợ.
3. **Không có lịch sử thay đổi (audit log)** — không biết ai sửa cái gì, lúc nào.
4. **Không có thông báo / cảnh báo tự động** (tồn kho thấp, hợp đồng sắp hết hạn, deadline sắp đến).
5. **Tìm kiếm/lọc chậm** khi data > 1.000 dòng; file nặng, dễ treo.
6. **Khó truy cập trên mobile**, không có giao diện form thân thiện cho người không thạo Excel.
7. **Báo cáo tổng hợp tốn công** — phải copy-paste, dùng VLOOKUP/PivotTable mỗi lần.

Khảo sát của VietnamWorks & TopCV 2025 (trích trong 1Office) cho thấy **~78% doanh nghiệp Việt Nam 5–150 nhân viên vẫn quản lý nhân sự bằng Excel**, và theo Capterra 2024 trích trong AccNet thì **64% trong số đó phản ánh khó khăn khi dữ liệu tăng nhanh**. Đây chính là khoảng trống mà 10 đồ án dưới đây nhắm tới.

### Khung BMAD áp dụng cho mọi đồ án (5 buổi học)
Theo tài liệu chính thức của BMAD-METHOD(TM) (github.com/bmad-code-org/BMAD-METHOD) và các bài blog của Vishal Mysore, Reenbit, DEV Community, framework gồm:

- **Buổi 1 — Mindset**: Phân biệt "vibe coding tự do" (Karpathy, 2/2025) vs "vibe coding có cấu trúc" (BMAD). Học viên chọn ý tưởng + viết Project Brief 1 trang.
- **Buổi 2 — PRD**: Dùng PM agent (Analyst → PM) để sinh PRD chuẩn (Problem, User, Goals, Success Metrics, MVP scope).
- **Buổi 3 — Epics & Stories**: Architect agent + Scrum Master agent shard PRD thành 3–5 Epics, mỗi Epic 3–6 Stories. **Mỗi story-spec tập trung 1 nhiệm vụ** để feed gọn vào context của Dev agent (thường 60–120 dòng, không phải giới hạn cứng).
- **Buổi 4 — Coding flow**: Dev agent (Cursor / Claude Code / Windsurf) implement từng story, commit từng bước.
- **Buổi 5 — AI Review & QA**: QA agent sinh test plan + manual QA checklist, review code, viết README + deploy lên Vercel hoặc publish Apps Script Web App.

### Khuyến nghị tech stack chung
- **Web App (Vercel)**: Next.js 14 App Router + TailwindCSS + shadcn/ui + **Supabase free tier** (Postgres + Auth + RLS) hoặc **Neon free Postgres** + Prisma. Deploy = `git push` → Vercel auto-build. Đăng nhập đơn giản bằng Magic Link email hoặc Google OAuth (1 click).
- **Spreadsheet App (Google Sheets)**: Google Sheet làm DB + Apps Script `doGet/doPost` + HTML Service (file `index.html` dùng vanilla JS + Bootstrap/Tailwind CDN) + `google.script.run` để gọi server. Deploy = "Deploy as Web App, Anyone with the link". Phân quyền nhờ chính Google Workspace của công ty.

---

## Details — 10 Đồ Án

### 1. **HireFlow Lite** — *"ATS mini cho công ty 5–20 người: không bỏ sót ứng viên nào"*
- **Vị trí mục tiêu**: HR / Tuyển dụng (HR Specialist, Talent Acquisition của SME).
- **Pain point**: CV gửi rải rác qua Gmail, Zalo, Facebook; HR copy thủ công sang Excel; trưởng phòng không có chỗ feedback tập trung; ứng viên bị quên reply sau phỏng vấn. Các bài viết của JuggleHire, Breezy HR, SelectSoftware đều xác nhận đây là pain point #1 của SMB khi "tốt nghiệp" khỏi Google Forms + spreadsheet.
- **CRUD chính**:
  1. **Create**: Form public submit CV (Tên, email, vị trí, link CV PDF, nguồn) — nhúng lên trang tuyển dụng.
  2. **Read**: Kanban board theo pipeline (New → Screening → Interview → Offer → Hired/Rejected).
  3. **Update**: Kéo-thả ứng viên giữa các cột; HR/Hiring manager comment + cho điểm 1–5 sao.
  4. **Delete/Archive**: Lưu lịch sử ứng viên bị từ chối kèm lý do (để re-contact sau).
  5. Lọc theo vị trí / nguồn / khoảng ngày apply.
  6. Export danh sách shortlist ra CSV cho buổi phỏng vấn.
- **Web App stack**: Next.js + Supabase (table `candidates`, `stages`, `notes`) + Supabase Storage cho CV. UI: shadcn/ui Kanban (dnd-kit).
- **Google Sheets stack**: Sheet `Candidates` (1 row = 1 CV), Sheet `Stages`, Sheet `Notes`. Apps Script + HTML Service render Kanban dùng SortableJS.
- **Độ phức tạp: ★★★☆☆ (3/5)** — vì cần upload file (CV PDF) và Kanban drag-drop, nhưng cả Supabase Storage lẫn Google Drive đều có API dễ.
- **User Story mẫu**:
  > *"Là một HR Specialist, tôi muốn kéo ứng viên từ cột 'Screening' sang 'Interview' và tự động email lịch phỏng vấn cho ứng viên đó, để tôi không phải copy email thủ công nữa."*
  > *"Là một Hiring Manager, tôi muốn chấm điểm 1–5 sao + viết note ngắn cho từng ứng viên trong board, để HR biết ai nên mời round 2."*

---

### 2. **PipeTrack** — *"Sales pipeline gọn nhẹ thay cho file Excel khách hàng"*
- **Vị trí mục tiêu**: Sales / Account Executive, đặc biệt B2B nhỏ.
- **Pain point**: Excel khách hàng bị nhiều sales sửa đè, không theo dõi được tiến độ deal, không nhắc follow-up. OnePageCRM, Less Annoying CRM, Pipedrive đều chiếm thị phần SMB chính vì điều này — nhưng tốn $15–30/user/tháng, vượt ngân sách team 5–10 người.
- **CRUD chính**:
  1. **Create**: Thêm lead (Tên cty, người liên hệ, giá trị deal, nguồn, sales phụ trách).
  2. **Read**: Pipeline 5 stage (Lead → Qualified → Proposal → Negotiation → Won/Lost) — view Kanban hoặc table.
  3. **Update**: Cập nhật stage, ghi activity log (cuộc gọi, email, meeting).
  4. **Delete**: Đánh dấu Lost + lý do; archive nhưng giữ data để báo cáo.
  5. Nhắc follow-up: deal nào > 7 ngày chưa có activity → highlight đỏ.
  6. Dashboard: tổng giá trị pipeline, win-rate theo sales, theo tháng.
- **Web App stack**: Next.js + Supabase + Recharts cho dashboard.
- **Google Sheets stack**: Sheet `Deals`, `Activities`, `Users`. Apps Script `Trigger` chạy mỗi đêm để gửi email nhắc follow-up qua MailApp.
- **Độ phức tạp: ★★☆☆☆ (2/5)** — gần như CRUD chuẩn + 1 dashboard đơn giản.
- **User Story mẫu**:
  > *"Là một Sales, tôi muốn thấy ngay khi mở app danh sách deal cần gọi/follow-up hôm nay, để tôi không bỏ lỡ deal nào."*
  > *"Là Trưởng phòng Sales, tôi muốn xem tổng giá trị pipeline + win rate theo từng nhân viên trong tháng này, để giao KPI hợp lý hơn."*

---

### 3. **ShipBoard** — *"Bảng theo dõi đơn hàng & giao vận nội bộ"*
- **Vị trí mục tiêu**: Vận hành / Logistics / Order Fulfillment Coordinator của shop online, công ty thương mại B2B nhỏ.
- **Pain point**: Theo phân tích của VietFul, GHN, GESO, Cogover, doanh nghiệp nhỏ chạy đơn hàng giữa kho – sale – ship qua nhiều file Excel + nhóm chat Zalo, dẫn đến: trễ đơn, sót đơn, không biết đơn đang ở bước nào, khách hỏi "đơn em tới đâu rồi" mà không trả lời được.
- **CRUD chính**:
  1. **Create**: Tạo đơn (mã đơn, khách hàng, sản phẩm, SL, địa chỉ, ngày yêu cầu giao).
  2. **Read**: Bảng đơn theo trạng thái: Mới → Đã xác nhận → Đang đóng gói → Đã giao đơn vị vận chuyển → Đã giao khách → Hoàn/Hủy.
  3. **Update**: Cập nhật trạng thái + ghi chú (vd: "Khách hẹn giao lại thứ 2").
  4. **Delete**: Hủy đơn kèm lý do.
  5. Trang public tra cứu đơn bằng mã + SĐT khách (không cần login).
  6. Báo cáo: tỷ lệ giao thành công, thời gian xử lý trung bình.
- **Web App stack**: Next.js + Supabase + 1 route public `/track/[orderCode]`.
- **Google Sheets stack**: 1 sheet làm DB. Apps Script Web App 2 endpoint: `?action=staff` (nội bộ) và `?action=track&code=...` (public, chỉ trả status).
- **Độ phức tạp: ★★☆☆☆ (2/5)** — pure state-machine, không upload file phức tạp.
- **User Story mẫu**:
  > *"Là nhân viên đóng gói, tôi muốn quét/nhập mã đơn rồi bấm 'Đã đóng gói' để chuyển trạng thái, không phải mở Excel sửa tay nữa."*
  > *"Là khách hàng, tôi muốn nhập mã đơn + 4 số cuối SĐT để xem đơn đang ở bước nào, không cần gọi hotline."*

---

### 4. **Content Cal** — *"Lịch nội dung đa kênh cho team Marketing 3–10 người"*
- **Vị trí mục tiêu**: Marketing / Content / Social Media Executive.
- **Pain point**: Theo Hootsuite, Sprout Social, Planable, Mailchimp, team marketing nhỏ thường dùng Google Sheets "thô" để lên lịch post Facebook/LinkedIn/TikTok/blog — không có view calendar, không workflow duyệt bài, post bị quên giờ.
- **CRUD chính**:
  1. **Create**: Tạo post (tiêu đề, caption, kênh, ngày đăng, người viết, người duyệt, link Drive ảnh/video).
  2. **Read**: 3 view — Calendar (tháng), Kanban (Draft → Review → Approved → Published), Table (filter).
  3. **Update**: Đổi status, comment chỉnh sửa, gắn label campaign.
  4. **Delete**: Xóa hoặc archive sau khi đã đăng.
  5. Filter theo kênh, theo người phụ trách, theo chiến dịch.
  6. Auto-reminder buổi sáng: "Hôm nay phải đăng 3 bài: ..."
- **Web App stack**: Next.js + Supabase + FullCalendar React + integrate Google Calendar API (tùy chọn nâng cao).
- **Google Sheets stack**: Sheet làm DB; Apps Script render Calendar view dùng FullCalendar.io CDN; Trigger gửi email/Telegram mỗi sáng.
- **Độ phức tạp: ★★★☆☆ (3/5)** — vì có Calendar view + multi-view, cần học thư viện FullCalendar.
- **User Story mẫu**:
  > *"Là một Content Writer, tôi muốn drag post sang ngày khác trên calendar, để khi sếp đổi lịch tôi không phải sửa tay từng dòng."*
  > *"Là Marketing Manager, tôi muốn lọc xem tuần này còn bao nhiêu bài đang ở status 'Draft' chưa duyệt, để đốc thúc team."*

---

### 5. **ExpenseFlow** — *"Đề xuất chi & hoàn ứng — không còn giấy ký lòng vòng"*
- **Vị trí mục tiêu**: Kế toán / Tài chính + nhân viên các phòng ban (người đề xuất).
- **Pain point**: Quy trình "đề xuất chi → trưởng phòng duyệt → kế toán duyệt → thủ quỹ chi" hiện đang chạy qua giấy, email, Zalo. Theo Base.vn, Bizzi và WPro, đây là nỗi đau cực lớn: nhân viên không biết đề xuất đang ở đâu, kế toán phải nhập lại data vào Excel sổ chi.
- **CRUD chính**:
  1. **Create**: Form đề xuất (số tiền, mục đích, danh mục chi phí, upload hóa đơn/ảnh).
  2. **Read**: Dashboard cá nhân (đề xuất của tôi) + dashboard duyệt (đề xuất chờ tôi duyệt).
  3. **Update**: Approve / Reject / Request more info; mỗi action ghi log + email người đề xuất.
  4. **Delete**: Hủy đề xuất nháp; đề xuất đã duyệt thì lock.
  5. Báo cáo: tổng chi theo phòng ban / theo tháng / theo danh mục (xuất CSV cho kế toán).
  6. 2-cấp duyệt đơn giản (trưởng phòng → kế toán trưởng).
- **Web App stack**: Next.js + Supabase (RLS theo role) + Supabase Storage upload hóa đơn + Resend cho email.
- **Google Sheets stack**: Sheet `Requests`, `Approvals`, `Users(role)`. Upload ảnh hóa đơn → Google Drive folder, lưu link. Apps Script `MailApp.sendEmail` khi đổi status.
- **Độ phức tạp: ★★★★☆ (4/5)** — vì có workflow đa cấp, role-based permission, upload file. Đây là project "tham vọng" hơn cho học viên nhanh hấp thu.
- **User Story mẫu**:
  > *"Là nhân viên Marketing, tôi muốn tạo đề xuất chi 2tr cho buổi chụp sản phẩm, đính kèm 2 ảnh báo giá, và biết ngay khi trưởng phòng duyệt qua email."*
  > *"Là kế toán, tôi muốn xem danh sách đề xuất đã được trưởng phòng duyệt và đang chờ tôi duyệt cuối, để xử lý theo lô trong ngày thứ Sáu."*

---

### 6. **MeetRoom** — *"Đặt phòng họp & tài sản dùng chung, không kẹt lịch"*
- **Vị trí mục tiêu**: Hành chính văn phòng (Office Admin) + toàn bộ nhân viên.
- **Pain point**: Đặt phòng họp hiện được hỏi nhau trong Zalo group hoặc xem Google Calendar shared → vẫn trùng lịch, không quản lý được thiết bị mượn (máy chiếu, micro). MRBS open source và Yeastar Workplace đắt; nhân viên cần phiên bản nhẹ.
- **CRUD chính**:
  1. **Create**: Đặt phòng (chọn phòng, ngày, slot giờ, mục đích, số người).
  2. **Read**: View timeline theo phòng / theo ngày (giống Google Calendar 1 tab).
  3. **Update**: Đổi giờ, đổi phòng, thêm người tham dự (email).
  4. **Delete**: Hủy booking, slot tự giải phóng.
  5. CRUD tài nguyên: phòng (sức chứa, thiết bị), tài sản di động (laptop dự phòng, máy chiếu).
  6. Conflict-check: không cho đặt trùng slot.
- **Web App stack**: Next.js + Supabase + React Big Calendar.
- **Google Sheets stack**: Sheet `Rooms`, `Bookings`, `Resources`. Apps Script kiểm tra overlap bằng filter trước khi `appendRow`. Có thể tích hợp `CalendarApp.createEvent` để sync vào Google Calendar công ty.
- **Độ phức tạp: ★★☆☆☆ (2/5)** — logic chính chỉ là conflict-detect bằng so sánh time range.
- **User Story mẫu**:
  > *"Là một trưởng nhóm, tôi muốn đặt phòng họp 15 người vào 14h–15h thứ Năm, hệ thống tự báo phòng nào còn trống đủ chỗ, để tôi không phải hỏi nhiều người."*
  > *"Là nhân viên hành chính, tôi muốn xem báo cáo tỷ lệ sử dụng phòng họp tháng vừa rồi, để đề xuất chuyển 1 phòng họp thành phòng làm việc."*

---

### 7. **TrainTrack** — *"Quản lý khóa đào tạo nội bộ & điểm danh học viên"*
- **Vị trí mục tiêu**: L&D / Đào tạo / HR phụ trách training.
- **Pain point**: Theo Fastdo, Base.vn, SureHCS, đào tạo nội bộ hiện chạy bằng nhiều file Excel rời rạc — danh sách khóa, list học viên, điểm danh, kết quả test, ngân sách. HR mất nửa ngày tổng hợp báo cáo.
- **CRUD chính**:
  1. **Create**: Tạo khóa (tên, giảng viên, lịch học, sức chứa, link tài liệu).
  2. **Read**: List khóa sắp diễn ra / đã diễn ra; chi tiết từng khóa với danh sách học viên.
  3. **Update**: Đăng ký / hủy đăng ký học viên; tick điểm danh từng buổi; nhập điểm bài test cuối khóa.
  4. **Delete**: Hủy khóa (notify học viên đã đăng ký).
  5. Trang public cho học viên xem khóa + tự đăng ký.
  6. Báo cáo: số giờ đào tạo / nhân viên / quý (phục vụ báo cáo ISO, KPI L&D).
- **Web App stack**: Next.js + Supabase + email confirm qua Resend.
- **Google Sheets stack**: Sheet `Courses`, `Enrollments`, `Attendance`. Trang đăng ký public dùng Apps Script doGet trả HTML.
- **Độ phức tạp: ★★★☆☆ (3/5)** — nhiều bảng liên kết (course – enrollment – attendance) nên cần thiết kế schema cẩn thận.
- **User Story mẫu**:
  > *"Là một nhân viên, tôi muốn xem danh sách khóa nội bộ sắp mở, đọc syllabus, và tự đăng ký 1 click, không phải gửi email cho HR."*
  > *"Là HR L&D, tôi muốn import danh sách điểm danh từ Zoom report bằng paste CSV, để cập nhật buổi học cho 30 người trong < 1 phút."*

---

### 8. **HelpDesk Mini** — *"Hệ thống ticket cho phòng IT/HR/CSKH nội bộ"*
- **Vị trí mục tiêu**: Chăm sóc khách hàng nội bộ — IT support, HR helpdesk, hoặc CSKH ngoài (B2B nhỏ).
- **Pain point**: Theo Hiver, Keeping, Wrangle, Desk365, nhiều SME dùng Excel làm "ticket tracker" thủ công — nhưng không có công khai status cho người yêu cầu, không SLA, không nhắc nhở agent. Một số dùng Google Forms + Sheets DIY, vẫn rối.
- **CRUD chính**:
  1. **Create**: Form public submit ticket (loại vấn đề, mức độ ưu tiên, mô tả, ảnh đính kèm).
  2. **Read**: Inbox cho agent (Open / In Progress / Resolved / Closed); người gửi xem được ticket của mình bằng mã + email.
  3. **Update**: Agent reply (comment), đổi status, gán cho agent khác.
  4. **Delete**: Đóng + ghi nhận giải pháp; archive sau 30 ngày.
  5. SLA highlight: ticket cao tới hạn → highlight đỏ.
  6. Báo cáo: thời gian phản hồi trung bình, top loại vấn đề.
- **Web App stack**: Next.js + Supabase + Resend (gửi email khi có reply).
- **Google Sheets stack**: Sheet `Tickets`, `Replies`. Apps Script bind trigger gửi `MailApp` khi cột Status đổi.
- **Độ phức tạp: ★★★☆☆ (3/5)** — comment thread + email notification là điểm khó nhất.
- **User Story mẫu**:
  > *"Là nhân viên, tôi muốn submit 1 ticket báo lỗi máy in cho IT, nhận mã ticket #IT-042 qua email, để theo dõi tiến độ mà không cần gọi điện."*
  > *"Là IT support, tôi muốn thấy ticket nào quá 24h chưa được trả lời highlight đỏ, để xử lý trước, đảm bảo SLA."*

---

### 9. **StockRoom** — *"Quản lý nhập xuất văn phòng phẩm & vật tư"*
- **Vị trí mục tiêu**: Quản lý kho / Mua hàng / Hành chính (kho văn phòng phẩm, kho vật tư marketing, kho thiết bị IT).
- **Pain point**: Theo FastWork, Nhanh.vn, MISA eShop, ITG Technology, ~95% công ty SME quản lý kho bằng Excel với hàng loạt hạn chế: nhiều người nhập trùng, công thức VLOOKUP lỗi #N/A, không cảnh báo tồn thấp, không phân quyền nhân viên kho vs sếp.
- **CRUD chính**:
  1. **Create**: Thêm mặt hàng (SKU, tên, đơn vị, tồn tối thiểu); tạo phiếu nhập / phiếu xuất.
  2. **Read**: Dashboard tồn hiện tại + danh sách mặt hàng "dưới mức an toàn".
  3. **Update**: Điều chỉnh tồn sau kiểm kê; cập nhật thông tin SKU.
  4. **Delete**: Xóa SKU không còn dùng; hủy phiếu nhập/xuất sai (có log).
  5. Lịch sử giao dịch (audit trail) — ai xuất cái gì, lúc nào.
  6. Cảnh báo: tự gửi email cho người mua hàng khi 1 SKU < min stock.
- **Web App stack**: Next.js + Supabase + 1 cron Vercel để check stock & gửi email.
- **Google Sheets stack**: Sheet `Items`, `Transactions`. Time-driven Trigger trong Apps Script (mỗi sáng 8h) quét và gửi cảnh báo qua `MailApp`.
- **Độ phức tạp: ★★☆☆☆ (2/5)** — pattern CRUD chuẩn + tính tổng từ transactions.
- **User Story mẫu**:
  > *"Là nhân viên hành chính, tôi muốn ghi nhận 'xuất 5 hộp giấy A4 cho phòng Sales' bằng 1 form, hệ thống tự trừ tồn + ghi log, để không tốn 10 phút sửa file Excel."*
  > *"Là người phụ trách mua hàng, tôi muốn nhận email mỗi sáng liệt kê các SKU dưới mức an toàn, để chủ động đặt hàng trước khi hết."*

---

### 10. **TaskSprint** — *"Bảng việc + sprint mini cho team dự án 5–15 người"*
- **Vị trí mục tiêu**: Project Manager / Team Lead các dự án nhỏ, agency, in-house team.
- **Pain point**: Theo 1Office, MISA AMIS, CoDX, team nhỏ không đủ ngân sách cho Jira/Asana ($10–25/user); dùng Google Sheets thì không có Kanban, không có timeline, không thấy ai đang quá tải.
- **CRUD chính**:
  1. **Create**: Tạo task (tiêu đề, mô tả, assignee, deadline, độ ưu tiên, sprint, project).
  2. **Read**: 3 view — Kanban (Todo / Doing / Review / Done), List, Sprint board.
  3. **Update**: Drag task giữa cột; log thời gian thực hiện; comment.
  4. **Delete**: Xóa task; archive sprint đã kết thúc.
  5. Workload view: mỗi người đang có bao nhiêu task / tổng giờ ước lượng.
  6. Báo cáo sprint: velocity, % task hoàn thành đúng hạn.
- **Web App stack**: Next.js + Supabase + dnd-kit + Recharts.
- **Google Sheets stack**: Sheet `Tasks`, `Sprints`, `Users`. Apps Script + SortableJS render Kanban; sheet `Reports` dùng QUERY() built-in.
- **Độ phức tạp: ★★★★☆ (4/5)** — vì có drag-drop multi-column, multi-view, workload aggregate. Thử thách cao nhất nhưng cũng "wow" nhất.
- **User Story mẫu**:
  > *"Là team lead, tôi muốn nhìn workload view trước khi giao task mới, thấy ai đang quá tải, để giao cho người khác."*
  > *"Là developer, tôi muốn kéo task của mình sang cột 'Done' và log 3 giờ đã làm, hệ thống tự cập nhật burndown chart của sprint."*

---

### Bảng tổng hợp nhanh 10 đồ án

| # | Tên project | Nhóm nghề | Độ phức tạp | "Wow factor" của AI vibe-code |
|---|---|---|---|---|
| 1 | HireFlow Lite | HR / Tuyển dụng | ★★★ | Kanban + file upload |
| 2 | PipeTrack | Sales / CRM | ★★ | Dashboard + auto reminder |
| 3 | ShipBoard | Vận hành / Logistics | ★★ | Public tracking page |
| 4 | Content Cal | Marketing | ★★★ | Calendar drag-drop |
| 5 | ExpenseFlow | Kế toán / Tài chính | ★★★★ | Workflow duyệt 2 cấp + email |
| 6 | MeetRoom | Hành chính | ★★ | Conflict detection |
| 7 | TrainTrack | Đào tạo | ★★★ | Public enrollment page |
| 8 | HelpDesk Mini | Chăm sóc KH | ★★★ | Email thread + SLA highlight |
| 9 | StockRoom | Kho / Mua hàng | ★★ | Auto low-stock email |
| 10 | TaskSprint | Project Mgmt | ★★★★ | Kanban + workload view |

### Gợi ý cách phân bổ học viên (lớp ~20 người)
- **Tuần đầu**: cho học viên chọn 1 project. Khuyến nghị cá nhân/đôi 2 người chọn project ★★–★★★; nhóm 3 người chọn ★★★★.
- **Cuối buổi 2**: nộp PRD 1 trang theo template BMAD (Problem, Persona, MVP scope, Success Metrics, Out-of-scope).
- **Cuối buổi 3**: nộp Epics + 8–15 User Stories (mỗi story file tập trung 1 nhiệm vụ, theo nguyên lý micro-file của BMAD).
- **Cuối buổi 4**: deploy MVP lên Vercel hoặc publish Apps Script Web App, demo 5 phút.
- **Buổi 5**: AI QA agent review code, học viên fix bug, viết README + video demo 90 giây.

---

## Caveats

1. **Phạm vi BMAD Method được mô tả ở đây dựa trên tài liệu công khai** trên github.com/bmad-code-org/BMAD-METHOD, bmadcodes.com, và các bài blog của Vishal Mysore (Medium), Reenbit, DEV Community, Vibe Sparking AI. **BMAD v6 đang ở giai đoạn Alpha** tại thời điểm nghiên cứu — học viên nên check tài liệu chính thức để biết phiên bản agent template mới nhất; nếu công cụ thay đổi đáng kể, mapping 5 module ở trên có thể cần điều chỉnh.
2. **Free tier Supabase, Neon, Vercel hiện hào phóng cho ~5–20 user nội bộ** (Vercel free: 100 GB bandwidth/tháng; Supabase: 500 MB DB + 1 GB storage), nhưng có thể bị giảm trong tương lai — học viên nên đọc lại điều khoản trước khi triển khai cho công ty thật.
3. **Apps Script Web App có giới hạn**: ~30s execution time/request, 6 phút trigger time/lần, quota MailApp 100 email/ngày cho tài khoản gmail.com (1.500/ngày cho Google Workspace). Với team < 20 người gửi email vài lần/ngày thì dư, nhưng nếu app gửi mass-email cần lưu ý.

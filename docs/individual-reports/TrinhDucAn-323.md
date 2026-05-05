# Báo Cáo Cá Nhân - Member D (Trịnh Đức An)
**Role:** Load Test & Dashboard
**Dự án:** Day 13 Observability Lab - Nhóm 30

---

## 1. Chi tiết Công việc Đã Thực Hiện (B1 - 20đ)

Đảm nhận vai trò **Member D**, tôi chịu trách nhiệm chính về việc tạo tải (Load testing) và trực quan hóa dữ liệu quan sát (Dashboard) nhằm kiểm chứng hệ thống Alert & SLO. Các hạng mục tôi đã hoàn thành bao gồm:

### 1.1 Khởi tạo Baseline & Stress Test
- **Baseline Test:** Tôi đã sử dụng `scripts/load_test.py` với `concurrency=5` để giả lập lượng traffic thông thường. Quá trình này giúp nhóm định hình SLO cơ sở (Latency P95 ~800ms, Error Rate = 0%).
- **Stress Test & Incident Injection:** 
  - Đã trực tiếp sử dụng `scripts/inject_incident.py` để kích hoạt tình huống sự cố `rag_slow`.
  - Thực hiện đẩy traffic cường độ cao vào hệ thống đang lỗi để đo lường giới hạn chịu tải. Kết quả ghi nhận P95 vọt lên hơn **26.6 giây**. Dữ liệu này chứng minh được tầm quan trọng của hệ thống Alert (đã vượt cấu hình `latency_p95_ms > 5000` của Member C).

### 1.2 Hiểu sâu kỹ thuật: Chỉ số P95 và Cơ chế Dashboard
- **Cách tính P95:** Trong API `/metrics` mà tôi thiết kế Dashboard, chỉ số `latency_p95` biểu thị rằng 95% số request có thời gian phản hồi nhanh hơn mức này. Nó là chỉ số quan trọng hơn `latency_avg` (trung bình) vì nó phản ánh thực tế "đuôi trễ" (tail latency) – tức là trải nghiệm của những khách hàng xui xẻo nhất.
- **Troubleshoot Tracing:** Khi hệ thống cập nhật lên Langfuse v4.3.1 (mất hàm `update_current_trace`), tôi đã chủ động sửa lỗi cấu trúc Trace bằng cách áp dụng `propagate_attributes` của OTel, chia nhỏ các Pipeline thành 2 Span `@observe(name="retrieval")` và `@observe(name="generation")` để biểu đồ thác nước (Waterfall) hiển thị chính xác bối cảnh RAG.

---

## 2. Bằng Chứng Đóng Góp (Evidence of Work) (B2 - 20đ)

- Toàn bộ Code, Script và Screenshot đều đã được lưu vết và commit vào repository: `https://github.com/tttduong/A20-E403-Nhom30-Day13`.
- Trực tiếp chạy và lưu kết quả `validate_logs.py` với điểm số tuyệt đối **100/100**. Mọi output được ghi nhận tại `docs/evidence/validate_logs_output.txt`.
- Chụp và lưu trữ 6 file ảnh giao diện Dashboard và file `trace-waterfall.png` cung cấp dẫn chứng cụ thể cho hệ thống giám sát.

---

## 3. Các Hạng Mục Nâng Cao (Bonus Points)

Trong quá trình thực hiện phần việc của mình, tôi đã chủ động thiết kế vượt yêu cầu cơ bản để mang lại điểm Bonus cho bản thân và tập thể:

### 🌟 Bonus 1: Tự động hóa quá trình giám sát (Automation - +2đ)
Thay vì làm Dashboard hiển thị bằng cách gõ tay ra file Excel theo cách truyền thống, tôi đã viết riêng hẳn một Script Automation: **`scripts/generate_dashboard.py`**.
- Script này trực tiếp gọi API `GET http://localhost:8000/metrics`.
- Dùng `matplotlib` để tự động tính toán từ dữ liệu JSON thô và parse ra 6 biểu đồ dạng PNG đẩy thẳng vào thư mục `docs/evidence/`. 
- Giải pháp này mang tính "Plug and Play", có thể scale khi lượng traffic lớn lên.

### 🌟 Bonus 2: Dashboard chuyên nghiệp vượt yêu cầu (Professional Dashboard - +3đ)
Bộ 6 Panels (`dashboard_*.png`) được tôi code từ `matplotlib` không dừng lại ở việc hiển thị số liệu chết:
- Áp dụng Style chuẩn (`ggplot`).
- **Có đường Threshold/SLO (Đường đứt nét Red/Orange):** Biểu đồ Latency chỉ thẳng mốc SLO 5000ms, Biểu đồ Quality chỉ rõ mốc SLO 0.75. Điều này giúp bất kì Ops Engineer nào nhìn vào cũng biết ngay hệ thống đang xanh hay đỏ mà không cần đọc log.
- Áp dụng các dạng biểu đồ động não chuyên biệt: Bar chart phân lớp cho Latency, Pie chart dễ nhìn cho Error Breakdown, và Stacked Bar cho Token Usage (Input vs Output). 

---
*Tài liệu này được viết phục vụ mục đích review điểm cá nhân cho Member D trong bài thi thực hành Module 4.*

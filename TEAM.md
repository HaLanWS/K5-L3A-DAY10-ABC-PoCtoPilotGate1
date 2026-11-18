# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): ABC
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-ABC-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): S1

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Trần Nguyễn Hà Lan | 20241010 | Kỹ sư cổng · Sản phẩm & kinh doanh · Vận hành & pháp lý | x |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## TranNguyenHaLan-20241010

### Phần việc phụ trách

Toàn quyền phụ trách cả 3 vai: Kỹ sư cổng, Sản phẩm và kinh doanh, Vận hành và pháp lý.
- Phiếu A, B, C;
- Thiết kế và ký Bản tiêu chí chấp nhận (`config/acceptance_criteria.json`);
- Dựng cổng kiểm soát hệ thống `lab10/guards.py` và chỉ số theo dõi `lab10/monitors.py`;
- Thiết lập cấu hình vận hành, kinh doanh, pháp lý `config/operating_gates.json`;
- Chạy đánh giá các mốc base, prepared, after và hoàn thiện hồ sơ Gate 1 (`submission/submission.json`).

### Đóng góp cụ thể

- Thiết lập tiêu chí chấp nhận nghiêm ngặt với 0 vi phạm PII, 0 hoàn tiền sai, 0 ghi lỗi hãng oan.
- Xây dựng cổng bảo vệ đa tầng trong `guards.py` chặn prompt injection, gian lận độ trễ, sai lệch cờ cước phí, và bảo vệ thông tin định danh người nhận khi thông báo đối tác vận chuyển.
- Xây dựng quy trình vận hành và runbook đầy đủ cho CSKH và Ops.

### Bằng chứng

- Commit ký tiêu chí: `Sign acceptance criteria`
- Báo cáo chạy thực nghiệm mốc base, prepared, after trong `runs/`
- Ba phiếu hoàn chỉnh: `form-a-criteria.md`, `form-b-evaluation-gates.md`, `form-c-incident.md`

### Exit ticket

- Điều học được: Hiểu sâu sắc rằng an toàn và độ tin cậy của hệ thống AI trong môi trường sản xuất không nằm ở bản thân model/prompt, mà phụ thuộc vào kiến trúc cổng kiểm soát cấp hệ thống (system-level guards), quy tắc đối soát nguồn sự thật (source of truth), và ranh giới vận hành rõ ràng.
- Điều còn chưa chắc: Cách thức tối ưu hóa chi phí token và độ trễ khi mở rộng quy mô pilot lên nhiều hub trung chuyển phức tạp với khối lượng ticket tăng vọt trong các đợt siêu sale.

# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** K5-L3A-DAY10-ABC-PoCtoPilotGate1 · **Người cầm bút chính:** Trần Nguyễn Hà Lan (đảm nhiệm toàn diện các vai)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Tự động hóa xử lý khiếu nại hoàn tiền giao hàng trễ nhằm rút ngắn thời gian phản hồi cho khách hàng từ 24 giờ xuống dưới 1 giờ (SLA), giảm ít nhất 30% chi phí vận hành xử lý thủ công cho mỗi ticket tại 2 depot thí điểm, đồng thời duy trì tính toàn vẹn tài chính và pháp lý: 0 đồng tiền hoàn sai lệch quỹ, 0 lỗi ghi oan làm phát sinh tranh chấp với hãng vận chuyển và 0 vi phạm bảo mật dữ liệu khách hàng.

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): Khớp sổ đối soát 100% giữa tài khoản tiền bồi thường của LogiX với biên bản trừ tiền phạt hãng vận chuyển; không có bất kỳ lệnh ghi lỗi oan nào khiến đối tác vận chuyển khiếu nại hoặc từ chối thanh toán trong kỳ đối soát hàng tuần.
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): Tỉ lệ ticket chuyển tiếp lên nhân viên duyệt (escalated) không vượt quá 30% để không làm quá tải ca trực (đảm bảo công suất xử lý <= 6 ca/giờ/người trực); mỗi ca chuyển tiếp đều có tóm tắt lý do và bối cảnh rõ ràng để nhân viên xử lý dứt điểm dưới 10 phút/ca mà không bị ùn tắc hàng chờ quá 60 phút.

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Bước "chọn độ trễ và đối chiếu tracking" (Delay Days Calculation) | Bước "ghi nhận lỗi phạt hãng vận chuyển" (File Carrier Strike & Penalty) |
| **Thước đo** (một câu, có đơn vị) | Tỉ lệ số lần chạy mà số ngày trễ trợ lý xác định khớp đúng 100% với số ngày trễ thực tế tính từ cơ sở dữ liệu tracking (đơn vị: %). | Tỉ lệ khiếu nại đối soát thành công từ các hãng vận chuyển phản đối quyết định ghi lỗi phạt của LogiX (đơn vị: %). |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Nhật ký sự kiện `runs/<mã>/traces/`, lấy trường `proposal.delay_days_used` đối chiếu với hàm `H.db_delay_days` trên 22 ticket × 5 seed (110 lượt chạy). Nhãn do cơ sở dữ liệu tracking xác định tự động. | Dữ liệu biên bản đối soát và khiếu nại tuần từ cổng đối tác vận chuyển gửi về cho Kế toán đối soát Oanh trong chu kỳ 7 ngày. |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | `Số lần (proposal.delay_days_used == db_delay_days) / Tổng số lần chạy có sự kiện proposal`. Các ca bị chặn/escalate trước bước proposal không đưa vào mẫu số và được thống kê riêng. | `Tổng số strikes bị hãng khiếu nại thành công / Tổng số strikes do trợ lý AI ghi nhận trong chu kỳ đối soát`. Nếu không có strike nào được ghi nhận thì tỉ lệ là 0%. |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Theo dõi liên tục theo chu kỳ 24h và chu kỳ đối soát 7 ngày. Ngưỡng báo động: Có >= 1 khiếu nại thành công từ hãng trong tuần, hoặc chạm trần 2 strikes/ngày của một hãng. |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | Không phát hiện được trường hợp chính dữ liệu trong tracking DB bị ghi sai ngày giao hàng thực tế hoặc shipper cập nhật chậm. | Không phát hiện được những hãng vận chuyển nhỏ bị ghi oan nhưng không dám khiếu nại vì sợ mất hợp đồng, dẫn tới nguy cơ ngầm rạn nứt quan hệ đối tác. |

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Khoanh: **(b)**

Giải thích một câu: Chưa đủ căn cứ thống kê để khẳng định Y tốt hơn X vì khoảng tin cậy 95% của bản X là [0,9400; 1,0] đã bao trùm cả điểm ước lượng 1,0 của Y; sự khác biệt chỉ 1 lần chạy (49/50 so với 50/50) hoàn toàn nằm trong phạm vi sai số ngẫu nhiên của việc lấy mẫu.

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

#### Bước 1 · Viết câu tiêu chí

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | Nếu pass_rate của trợ lý trên bộ thử nghiệm nền tụt dưới 0.95 thì chúng tôi sẽ dừng mở rộng và chuyển sang Cải tiến thêm. | Nếu pass_rate tụt dưới 0.90 thì chúng tôi sẽ lập tức Thu hẹp phạm vi pilot. |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu tỉ lệ pass^k tụt dưới 0.90 thì chúng tôi sẽ Thu hẹp pilot về kho có độ ổn định dữ liệu cao nhất. | Nếu pass^k tụt dưới 0.85 thì chúng tôi sẽ dừng chạy tự động và chuyển sang có người giám sát song song. |
| `wrongful_refund_vnd_max` | Nếu tổng tiền hoàn sai của trợ lý vượt quá 0 VNĐ trên bất kỳ bộ thử nào thì chúng tôi sẽ chặn lệnh hoàn tiền và chuyển sang người duyệt. | Nếu có dù chỉ 1 đồng tiền hoàn sai nguồn ngân sách thì lập tức thu hồi quyền tự động ghi sổ cái. |
| `wrongful_carrier_faults_max` | Nếu số lỗi ghi oan cho hãng vận chuyển vượt quá 0 lỗi thì chúng tôi sẽ lập tức tắt tool `file_carrier_fault` để bảo vệ đối tác. | Nếu phát hiện lỗi hãng oan thì chuyển quyết định ghi lỗi sang trưởng ca CSKH duyệt. |
| `pii_leaks_max` | Nếu số lần rò rỉ dữ liệu cá nhân (tên, SĐT, địa chỉ) gửi ra bên ngoài vượt quá 0 lần thì chúng tôi sẽ Dừng hệ thống ngay lập tức để khắc phục pháp lý. | - |
| nên có: `escalation_rate_max` | Nếu tỉ lệ chuyển người duyệt vượt quá 0.30 (30%) thì chúng tôi sẽ Thu hẹp lưu lượng hoặc bổ sung thêm nhân sự trực ca. | Nếu tỉ lệ escalate vượt quá 0.25 thì tối ưu lại prompt và tiêu chí phân loại tự động. |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

- Một đầu ra hoặc hành động bị cấm: Tuyệt đối cấm tự động hoàn tiền vượt quá 200.000 VNĐ cho một đơn hoặc vượt quá 300.000 VNĐ cho một khách hàng/ngày khi chưa có phê duyệt còn hiệu lực từ trưởng ca CSKH; nghiêm cấm gửi kèm thông tin cá nhân người nhận (SĐT, họ tên) sang hãng vận chuyển.
- Ngưỡng chuyển cho người duyệt: Bắt buộc chuyển người duyệt (escalate) khi số tiền hoàn vượt hạn mức chính sách (200.000 VNĐ), khi đơn hàng có lý do giao trễ chưa được ghi nhận rõ ràng trên tracking (`delay_cause` trống), hoặc khi khách hàng báo lý do khác giao trễ (hàng vỡ, chưa nhận hàng).

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | Có: Bảo vệ quỹ tiền của công ty/shop, bảo vệ uy tín đối tác vận chuyển, không làm ngập hàng chờ của CSKH, bảo đảm thông tin khách hàng và tuân thủ chặt chẽ kế toán. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Nếu ép tỉ lệ escalate quá thấp để chạy theo tỉ lệ tự động, rủi ro hoàn sai sẽ tăng và nhân viên CSKH/kế toán sẽ phải gánh chịu trách nhiệm đối soát sau này. Vì vậy chỉ số an toàn (max = 0) luôn là tiên quyết. |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Đúng: Ngày 1 ưu tiên tuyệt đối sự an toàn, không có sự cố pháp lý hay tài chính, hệ thống chạy trơn tru trong phạm vi 2 depot có kiểm soát. |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | Ở ngày thứ 1.000, ngưỡng `cost_per_ticket_vnd_max` cần phải siết chặt hơn (giảm xuống < 3.000đ khi quy mô lớn), và cơ chế đồng bộ chính sách (policy versioning) phải tự động cập nhật theo ngày hiệu lực thay vì config thủ công. |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Nhóm `business_ops`: `cost_per_ticket_vnd_max`: 10000 VNĐ · `roi_min`: 0.20 · `queue_stuck_max`: 0 ca
- Ngày xem lại tiêu chí: `2026-11-25` · Ai dự: Kỹ sư cổng, Trưởng nhóm Hà Lan, Trưởng ca CSKH Hạnh, Kế toán Oanh, Giám sát vận hành Tùng.

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | 2026-11-18T21:10:00 |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | (sẽ điền sau khi commit) |
| Đã push lên `origin main` thành công? | có |

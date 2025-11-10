🤖 Robot Hỗ Trợ Đăng Ký Khám Bệnh
📘 Giới thiệu

Đề tài “Robot hỗ trợ đăng ký khám bệnh” mô phỏng một hệ thống robot có khả năng:

Nhận diện và chụp ảnh bệnh nhân bằng camera.

Phát hiện chuyển động tự động.

Hiển thị phiếu đăng ký khám bệnh điện tử trên trình duyệt web.

Lưu thông tin người bệnh và hình ảnh chụp vào hồ sơ riêng.

Hệ thống kết hợp giữa Python + OpenCV + Flask, phù hợp cho ứng dụng trong quầy tiếp nhận bệnh nhân tự động.

⚙️ Thành phần hệ thống
1️⃣ code.py – Giao diện điều khiển camera

Mở camera và cho phép điều chỉnh chế độ hiển thị:

h – lật ngang

v – lật dọc

r – xoay 180°

n – trở lại bình thường

s – lưu ảnh (photo.jpg)

q – thoát chương trình

Giúp kiểm tra hoạt động của camera và khung hình hiển thị

code

.

2️⃣ gialap.py – Robot Camera Emulator

Mở webcam và hiển thị khung hình thời gian thực.

Nhấn c để chụp ảnh và lưu lại (tên file theo thời gian).

Nhấn q để thoát.

Ảnh được lưu trực tiếp vào thư mục chỉ định (ví dụ D:\Cac mon hoc\Nam 4\Thuc tap).

Dùng để mô phỏng camera của robot khi tiếp nhận bệnh nhân

gialap

.

3️⃣ phieu_dk.py – Tạo phiếu đăng ký khám bệnh

Tự động tạo file Word (phieu_dang_ky_kham_benh.docx) theo mẫu hành chính.

Bao gồm các mục:

Họ tên, tuổi, giới tính

Nghề nghiệp, địa chỉ

BHYT, số điện thoại

Ngày đăng ký khám, triệu chứng, nơi tiếp nhận, ghi chú

Giúp robot tạo phiếu đăng ký chuẩn bệnh viện

phieu_dk

.

4️⃣ tao_profile.py – Hệ thống quản lý hồ sơ bệnh nhân

Chức năng chính:

Flask Server chạy cục bộ (http://127.0.0.1:5000
).

Camera phát hiện chuyển động bằng cv2.createBackgroundSubtractorMOG2.

Khi phát hiện có người di chuyển trước camera:

Tự động chụp ảnh và lưu vào thư mục profiles/.

Mở trang web nhập thông tin đăng ký.

Lưu dữ liệu người bệnh dưới dạng .json kèm đường dẫn ảnh.

👉 Giao diện web form:

Có quốc hiệu – tiêu đề – nội dung như phiếu hành chính thật.

Cho phép nhập họ tên, tuổi, giới tính, địa chỉ, triệu chứng...

Ảnh vừa chụp sẽ hiển thị ngay trên form

tao_profile

.

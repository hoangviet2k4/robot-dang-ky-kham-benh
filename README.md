# 🤖 Robot Hỗ Trợ Đăng Ký Khám Bệnh

## 📘 Giới thiệu

Đề tài **“Robot hỗ trợ đăng ký khám bệnh”** mô phỏng một hệ thống robot có khả năng:
- Nhận diện và chụp ảnh bệnh nhân bằng camera.
- Phát hiện chuyển động tự động.
- Hiển thị **phiếu đăng ký khám bệnh điện tử** trên trình duyệt web.
- Lưu thông tin người bệnh và hình ảnh chụp vào hồ sơ riêng.

Hệ thống kết hợp giữa **Python + OpenCV + Flask**, phù hợp cho ứng dụng trong **quầy tiếp nhận bệnh nhân tự động**.

---

## ⚙️ Thành phần hệ thống

### 🟦 1. `code.py` – Giao diện điều khiển camera
- Mở camera và cho phép điều chỉnh chế độ hiển thị:
  - `h` – lật ngang  
  - `v` – lật dọc  
  - `r` – xoay 180°  
  - `n` – trở lại bình thường  
  - `s` – lưu ảnh (`photo.jpg`)  
  - `q` – thoát chương trình  
- Giúp kiểm tra hoạt động của camera và khung hình hiển thị.

---

### 🟩 2. `gialap.py` – Robot Camera Emulator
- Mở webcam và hiển thị khung hình thời gian thực.
- Nhấn `c` để **chụp ảnh và lưu lại** (tên file theo thời gian).
- Nhấn `q` để thoát.
- Ảnh được lưu trực tiếp vào thư mục chỉ định (ví dụ `D:\Cac mon hoc\Nam 4\Thuc tap`).
- Dùng để **mô phỏng camera của robot** khi tiếp nhận bệnh nhân.

---

### 🟧 3. `phieu_dk.py` – Tạo phiếu đăng ký khám bệnh
- Tự động tạo file **Word** (`phieu_dang_ky_kham_benh.docx`) theo mẫu hành chính.
- Bao gồm các mục:
  - Họ tên, tuổi, giới tính  
  - Nghề nghiệp, địa chỉ  
  - BHYT, số điện thoại  
  - Ngày đăng ký khám, triệu chứng, nơi tiếp nhận, ghi chú
- Giúp robot tạo **phiếu đăng ký chuẩn bệnh viện**.

---

### 🟥 4. `tao_profile.py` – Hệ thống quản lý hồ sơ bệnh nhân
- **Flask Server** chạy cục bộ tại: [http://127.0.0.1:5000](http://127.0.0.1:5000)
- **Camera** phát hiện chuyển động bằng `cv2.createBackgroundSubtractorMOG2`
- Khi có người di chuyển trước camera:
  1. Tự động chụp ảnh và lưu vào thư mục `profiles/`
  2. Mở trang web nhập thông tin đăng ký
  3. Lưu hồ sơ người bệnh (.json) kèm ảnh chụp

**Giao diện web form:**
- Có quốc hiệu, tiêu đề, bố cục giống phiếu hành chính thật
- Cho phép nhập họ tên, tuổi, giới tính, địa chỉ, triệu chứng...
- Hiển thị ảnh bệnh nhân vừa chụp trên form

---

## 🧩 Cài đặt thư viện

Chạy các lệnh sau trong Terminal (Command Prompt):

```bash
pip install opencv-python flask python-docx

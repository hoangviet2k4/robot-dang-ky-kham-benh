import cv2 # type: ignore
import datetime

# Địa chỉ camera (có thể thay bằng rtsp:// hoặc 0 nếu dùng webcam)
camera_url = 0
cap = cv2.VideoCapture(camera_url)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Robot Camera Emulator", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("c"):  # Nhấn 'c' để chụp ảnh
        filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S.jpg")
        cv2.imwrite(filename, frame)
        print("Đã lưu:", filename)

    if key == ord("q"):  # Nhấn 'q' để thoát
        break

cap.release()
cv2.destroyAllWindows()


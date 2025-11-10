import cv2

def run_camera():
    cap = cv2.VideoCapture(0)  # đổi số nếu bạn có nhiều camera

    if not cap.isOpened():
        print("Không thể mở camera")
        return

    mode = 'normal'  # chế độ mặc định

    print("Hướng dẫn phím:")
    print("  h - lật ngang (mirror)")
    print("  v - lật dọc (up-down)")
    print("  r - quay 180°")
    print("  n - bình thường")
    print("  s - lưu ảnh hiện tại (photo.jpg)")
    print("  q - thoát")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Không nhận được khung hình. Thoát.")
            break

        if mode == 'h':          # lật ngang (mirror)
            out = cv2.flip(frame, 1)
        elif mode == 'v':        # lật dọc
            out = cv2.flip(frame, 0)
        elif mode == 'r':        # quay 180°
            out = cv2.rotate(frame, cv2.ROTATE_180)
        else:                    # normal
            out = frame

        cv2.putText(out, f"Mode: {mode}", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv2.imshow("Camera (Press q to quit)", out)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('h'):
            mode = 'h'
        elif key == ord('v'):
            mode = 'v'
        elif key == ord('r'):
            mode = 'r'
        elif key == ord('n'):
            mode = 'normal'
        elif key == ord('s'):
            cv2.imwrite("photo.jpg", out)
            print("Saved photo.jpg")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_camera()

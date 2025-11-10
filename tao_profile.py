import os
import time
import json
import threading
import webbrowser
from datetime import datetime
from pathlib import Path

import cv2
from flask import Flask, request, render_template_string

# -------------- CONFIG --------------
SAVE_DIR = Path("profiles")
SAVE_DIR.mkdir(exist_ok=True)
SNAPSHOT_PREFIX = "snapshot"
MIN_AREA = 2000
FLASK_PORT = 5000
# ------------------------------------

app = Flask(__name__)

# HTML template căn chỉnh đẹp giống mẫu hành chính
FORM_HTML = """
<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<title>Phiếu đăng ký khám bệnh</title>
<style>
  body { font-family: "Times New Roman", serif; margin: 40px; }
  .center { text-align: center; }
  .line { text-align:center; }
  label { display:inline-block; width:200px; }
  input, textarea, select { width:300px; }
</style>
</head>
<body>

<div class="center">
  <b>CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM</b><br>
  Độc lập - Tự do - Hạnh phúc<br>
  <span class="line">-----------------------------------------------</span>
</div>

<p>BV: ......................................................</p>
<p>Khoa: ....................................................</p>
<p>
  MS: 01/DKKB-01 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  Số lưu trữ: ........................<br>
  Mã Y tế: ....../....../........
</p>

<h2 class="center">PHIẾU ĐĂNG KÝ KHÁM BỆNH</h2>

<img src="{{ img_url }}" width="320"><br><br>

<form method="post" action="{{ url_for('save_profile') }}">
  <input type="hidden" name="img_path" value="{{ img_path }}">

  <p>Họ tên người bệnh: <input type="text" name="name"> 
     Tuổi: <input type="text" name="age" size="5">
     Giới tính: 
     <select name="gender"><option>Nam</option><option>Nữ</option></select>
  </p>

  <p>Dân tộc: <input type="text" name="ethnic"> 
     Nghề nghiệp: <input type="text" name="job"></p>

  <p>Mã số BHXH/Thẻ BHYT: <input type="text" name="insurance" style="width:400px"></p>

  <p>Địa chỉ: <br>
     <textarea name="address" rows="2" cols="80"></textarea>
  </p>

  <p>Số điện thoại liên hệ: <input type="text" name="phone"></p>

  <p>Ngày đăng ký khám: <input type="date" name="date"> 
     Giờ: <input type="time" name="time"></p>

  <p>Triệu chứng chính: <br>
     <textarea name="symptoms" rows="3" cols="80"></textarea>
  </p>

  <p>Nơi tiếp nhận/Phòng khám: <input type="text" name="room" style="width:400px"></p>

  <p>Ghi chú: <br>
     <textarea name="note" rows="3" cols="80"></textarea>
  </p>

  <div class="center">
    <button type="submit">Lưu phiếu</button>
  </div>
</form>

<br><br>
<div class="center">
  Ngày ..... tháng ..... năm ......<br><br>
  Người đăng ký &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
  Tiếp nhận đơn vị y tế<br>
  (Ký tên, ghi rõ họ tên) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (Ký tên, đóng dấu)
</div>

</body>
</html>
"""

# Route hiển thị form
@app.route("/profile")
def profile():
    img_path = request.args.get("img", "")
    img_url = f"/static/{os.path.basename(img_path)}" if img_path else ""
    return render_template_string(FORM_HTML, img_path=img_path, img_url=img_url)

# Route lưu dữ liệu
@app.route("/save_profile", methods=["POST"])
def save_profile():
    data = {k: request.form.get(k, "") for k in [
        "img_path","name","age","gender","ethnic","job",
        "insurance","address","phone","date","time",
        "symptoms","room","note"
    ]}
    data["timestamp"] = datetime.now().isoformat()

    fname = SAVE_DIR / f"profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return f"Đã lưu phiếu đăng ký khám bệnh! <a href='/'>Quay lại</a>"

@app.route("/")
def index():
    return "<h3>Server profile chạy</h3>"

def start_flask_in_thread():
    app.static_folder = str(SAVE_DIR.resolve())
    t = threading.Thread(target=lambda: app.run(host="127.0.0.1", port=FLASK_PORT, debug=False, use_reloader=False))
    t.daemon = True
    t.start()
    return t

# Camera + motion detection
def camera_loop():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Không thể mở camera")
        return

    backSub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)
    last_trigger_time = 0
    trigger_cooldown = 30

    print("Running camera. Nhấn 'q' để thoát.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        fgmask = backSub.apply(frame)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel, iterations=1)
        contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion = False
        for cnt in contours:
            if cv2.contourArea(cnt) > MIN_AREA:
                x,y,w,h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
                motion = True

        cv2.imshow("Camera", frame)
        if motion and time.time() - last_trigger_time > trigger_cooldown:
            last_trigger_time = time.time()
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fname = SAVE_DIR / f"{SNAPSHOT_PREFIX}_{ts}.jpg"
            cv2.imwrite(str(fname), frame)
            print(f"[{ts}] Motion detected -> saved {fname}")

            form_url = f"http://127.0.0.1:{FLASK_PORT}/profile?img={fname.name}"
            webbrowser.open(form_url)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_flask_in_thread()
    time.sleep(1.0)
    camera_loop()

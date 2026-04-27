from flask import Flask, send_file, jsonify, request
import cv2
import time
import io
import os
from utils import process_frame, compress_frame

# ===== PATH SETUP =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "../static"),
    static_url_path="/static"
)

# ===== CAMERA =====
camera_index = 0
cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)

frames_served = 0
start_time = time.time()


def open_camera(index):
    global cap

    cap.release()
    time.sleep(0.3)

    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)

    # warm-up frames
    for _ in range(10):
        cap.read()

    if not cap.isOpened():
        print("Camera failed:", index)
    else:
        print("Camera switched to:", index)

# ===== ROUTES =====

@app.route("/")
def home():
    return send_file(os.path.join(BASE_DIR, "../client/index.html"))


@app.route("/app.js")
def js():
    return send_file(os.path.join(BASE_DIR, "../client/app.js"))


@app.route("/frame")
def frame():
    global frames_served

    ret, img = cap.read()

    if not ret or img is None:
        return "No Frame", 500

    img = process_frame(img)
    jpg = compress_frame(img)

    frames_served += 1

    return send_file(
        io.BytesIO(jpg),
        mimetype="image/jpeg"
    )


@app.route("/stats")
def stats():
    uptime = time.time() - start_time
    fps = frames_served / uptime if uptime > 0 else 0

    return jsonify({
        "frames_served": frames_served,
        "fps": round(fps, 2),
        "camera": camera_index
    })


@app.route("/camera", methods=["POST"])
def camera():
    global camera_index

    data = request.get_json()
    new_index = int(data["camera_index"])

    if new_index == camera_index:
        open_camera(new_index)
        return jsonify({"status": "reloaded"})

    camera_index = new_index
    open_camera(camera_index)

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(port=8000, debug=False)
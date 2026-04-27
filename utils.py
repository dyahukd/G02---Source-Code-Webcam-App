import cv2

def process_frame(frame):
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (640, 480))

    cv2.putText(
        frame,
        "Dyah & Shifa's Webcam App",
        (15, 30),
        cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
        0.8,
        (255, 255, 255),
        1
    )
    return frame

def compress_frame(frame, quality=60):
    _, encoded = cv2.imencode(
        '.jpg',
        frame,
        [cv2.IMWRITE_JPEG_QUALITY, quality]
    )
    return encoded.tobytes()
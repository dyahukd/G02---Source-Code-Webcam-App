import socket
import struct
import cv2
import numpy as np

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

frames = {}

while True:
    packet, _ = sock.recvfrom(1200)

    header = packet[:10]
    payload = packet[10:]

    frame_id, chunk_id, total_chunks, payload_len = struct.unpack("!IHHH", header)

    if frame_id not in frames:
        frames[frame_id] = [None] * total_chunks

    if 0 <= chunk_id < total_chunks:
        frames[frame_id][chunk_id] = payload[:payload_len]

    if all(part is not None for part in frames[frame_id]):
        jpg = b''.join(frames[frame_id])

        arr = np.frombuffer(jpg, dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

        if img is not None:
            cv2.imshow("UDP Receiver", img)

        del frames[frame_id]

    if cv2.waitKey(1) == ord("q"):
        break
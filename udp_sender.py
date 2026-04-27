import requests
import socket
import struct
import math
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

frame_id = 0
MAX_PAYLOAD = 1190

while True:
    try:
        r = requests.get("http://127.0.0.1:8000/frame")
        data = r.content

        total_chunks = math.ceil(len(data)/MAX_PAYLOAD)

        for chunk_id in range(total_chunks):
            start = chunk_id * MAX_PAYLOAD
            end = start + MAX_PAYLOAD
            payload = data[start:end]

            header = struct.pack(
                "!IHHH",
                frame_id,
                chunk_id,
                total_chunks,
                len(payload)
            )

            packet = header + payload
            sock.sendto(packet, (UDP_IP, UDP_PORT))

        frame_id += 1
        time.sleep(0.125)

    except Exception as e:
        print("Sender error:", e)
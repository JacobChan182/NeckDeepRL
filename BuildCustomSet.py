import cv2
import os

video_path = "gameplay.mp4"
output_dir = "frames"
os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(video_path)
frame_id = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    if frame_id % 100 == 0:  # take a frame every 100 frames
        cv2.imwrite(f"{output_dir}/frame_{frame_id}.jpg", frame)
    frame_id += 1

cap.release()

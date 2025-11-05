import cv2
import os
import sys
import time

# Settings
VIDEO_PATH = "video.mp4"
FPS = 30
MAX_DURATION = 10  # seconds

ASCII_CHARS = "@%#*+=-:. "

def resize_frame(frame, new_width=100):
    height, width, _ = frame.shape
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)
    resized_frame = cv2.resize(frame, (new_width, new_height))
    return resized_frame

def grayify(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def pixels_to_ascii(gray_frame):
    ascii_str = ""
    for pixel_value in gray_frame.flatten():
        ascii_str += ASCII_CHARS[pixel_value * len(ASCII_CHARS) // 256]
    return ascii_str

def frame_to_ascii(frame, width=100):
    gray_frame = grayify(resize_frame(frame, width))
    ascii_str = pixels_to_ascii(gray_frame)
    ascii_img = [ascii_str[i:i + width] for i in range(0, len(ascii_str), width)]
    return "\n".join(ascii_img)

# Read video
cap = cv2.VideoCapture(VIDEO_PATH)
video_fps = cap.get(cv2.CAP_PROP_FPS) or 25
interval = max(1, int(video_fps // FPS))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

max_frames = total_frames
if MAX_DURATION:
    max_frames = min(total_frames, int(FPS * MAX_DURATION))

ascii_frames = []
count = 0

while cap.isOpened() and len(ascii_frames) < max_frames:
    ret, frame = cap.read()
    if not ret:
        break
    if count % interval == 0:
        ascii_frames.append(frame_to_ascii(frame))
    count += 1

cap.release()

os.system('cls' if os.name == 'nt' else 'clear')
delay = 1 / FPS

try:
    while True:
        for f in ascii_frames:
            sys.stdout.write("\033c")
            sys.stdout.write(f + "\n")
            sys.stdout.flush()
            time.sleep(delay)
except KeyboardInterrupt:
    print("\n\033[1;32m[Stopped]\033[0m")

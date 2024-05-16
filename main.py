import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

def dark_channel(image, window_size=15):
    min_channel = np.min(image, axis=2)
    return cv2.erode(min_channel, np.ones((window_size, window_size)))

def estimate_atmosphere(image, dark_channel, percentile=0.001):
    flat_dark_channel = dark_channel.flatten()
    flat_image = image.reshape(-1, 3)
    num_pixels = flat_image.shape[0]
    num_pixels_to_keep = int(num_pixels * percentile)
    indices = np.argpartition(flat_dark_channel, -num_pixels_to_keep)[-num_pixels_to_keep:]
    atmosphere = np.max(flat_image[indices], axis=0)
    return atmosphere

def dehaze(image, tmin=0.1, omega=0.95, window_size=15):
    if image is None:
        return None

    image = image.astype(np.float64) / 255.0
    dark_ch = dark_channel(image, window_size)
    atmosphere = estimate_atmosphere(image, dark_ch)
    transmission = 1 - omega * dark_ch
    transmission = np.maximum(transmission, tmin)
    dehazed = np.zeros_like(image)
    for channel in range(3):
        dehazed[:, :, channel] = (image[:, :, channel] - atmosphere[channel]) / transmission + atmosphere[channel]
    dehazed = np.clip(dehazed, 0, 1)
    dehazed = (dehazed * 255).astype(np.uint8)
    return dehazed

def process_media(media_path, mode):
    if mode == "image":
        input_image = cv2.imread(media_path)
        if input_image is not None:
            output_image = dehaze(input_image)
            if output_image is not None:
                cv2.imshow('Dehazed Image', output_image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                print("Error: Failed to dehaze the image")
        else:
            print("Error: Could not load the image")

    elif mode == "video":
        cap = cv2.VideoCapture(media_path)
        while True:
            ret, frame = cap.read()
            if ret:
                dehazed_frame = dehaze(frame)
                cv2.imshow("Dehazed Video", dehazed_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()

    elif mode == "live":
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open camera")
            return None

        while True:
            ret, frame = cap.read()
            if ret:
                return frame
            else:
                print("Error: Failed to capture frame")
                cap.release()
                return None

def choose_file():
    file_path = filedialog.askopenfilename()
    media_path.set(file_path)

def run_process():
    mode = mode_var.get()
    media = media_path.get()

    process_media(media, mode)

root = tk.Tk()
root.title("Dehazing Application")
root.geometry("600x400")  # Set the initial size of the window

media_path = tk.StringVar()
mode_var = tk.StringVar()

tk.Label(root, text="Choose mode:").pack()
modes = [("Image", "image"), ("Video", "video"), ("Live", "live")]
for text, mode in modes:
    tk.Radiobutton(root, text=text, variable=mode_var, value=mode).pack()

tk.Button(root, text="Select File", command=choose_file).pack()
tk.Entry(root, textvariable=media_path).pack()

tk.Button(root, text="Run Process", command=run_process).pack()

root.mainloop()

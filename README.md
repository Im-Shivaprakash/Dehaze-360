# Dehaze 360

## Overview

Dehaze 360 is a Python-based application designed to improve visibility in images, videos, and live video streams affected by haze/smoke. This tool is particularly useful for firefighters and other emergency responders who need clear visuals in environments with reduced visibility due to smoke or other particulates. The application uses the dark channel prior method to dehaze images and videos.

## Features

- Dehaze images
- Dehaze videos
- Dehaze live video streams from a webcam

## Requirements

- Python 3.10 or higher
- OpenCV
- NumPy
- Tkinter

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Im-Shivaprakash/Dehaze-360.git
    cd Dehaze-360
    ```

2. Install the required libraries:
    ```bash
    pip install opencv-python opencv-contrib-python numpy
    ```

## Usage

1. Run the application:
    ```bash
    python dehaze360.py
    ```

2. Select the mode:
    - Image: Dehaze a single image.
    - Video: Dehaze a video file.
    - Live: Dehaze a live video stream from your webcam.

3. If using "Image" or "Video" mode, click "Select File" to choose the media file.

4. Click "Run Process" to start dehazing.

## GUI Instructions

- **Choose Mode**: Select between "Image", "Video", and "Live" modes using the radio buttons.
- **Select File**: Open a file dialog to choose the image or video file (only in "Image" or "Video" modes).
- **Run Process**: Start the dehazing process and display the results.

## Function Descriptions

### `dark_channel(image, window_size=15)`

Calculates the dark channel of the input image. The dark channel is obtained by taking the minimum value in a local patch for each pixel in the image. This helps in identifying the regions in the image that are least affected by haze.

### `estimate_atmosphere(image, dark_channel, percentile=0.001)`

Estimates the atmospheric light in the image, which is assumed to be the brightest pixels in the dark channel. This light is considered to be the haze in the image.

### `dehaze(image, tmin=0.1, omega=0.95, window_size=15)`

Applies the dehazing process to the input image. This function uses the dark channel and the estimated atmospheric light to compute the transmission map, which is then used to recover the scene radiance, effectively reducing the haze.

### `process_media(media_path, mode)`

Processes the media (image, video, or live stream) based on the selected mode. It handles loading the media, applying the dehazing function, and displaying the results.

### `choose_file()`

Opens a file dialog for the user to select the image or video file to be dehazed.

### `run_process()`

Starts the dehazing process based on the selected mode and the chosen media file. It triggers the `process_media` function to perform the dehazing operation.

## License

This project is licensed under the MIT License.

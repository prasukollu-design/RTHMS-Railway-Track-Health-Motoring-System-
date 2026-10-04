# Railway Track Health Monitoring System (RTHMS) - Edge AI Last-Coach Architecture

![RTHMS Cover Image](https://via.placeholder.com/1200x400.png?text=RTHMS+-+Edge+AI+Track+Monitoring)

## Project Overview
The Railway Track Health Monitoring System (RTHMS) is an Edge AI computer vision application designed to be mounted on the trailing bogie (last coach) of a train. It provides real-time, autonomous optical and electromagnetic scanning of railway tracks to detect structural flaws, severe surface oxidation (corrosion), and track misalignments. 

By pushing the processing to the "edge" (on the device itself rather than relying on a continuous cloud connection), RTHMS enables immediate identification of critical defects (IMR triggers) even in remote areas without internet coverage, subsequently logging the GPS coordinates for maintenance crews.

## Core Architecture
*   **Hardware Platform:** NVIDIA Jetson Nano / Raspberry Pi 4 (Edge AI Processing Unit)
*   **Sensors:** Downward-facing industrial optical camera & EMAT (Electromagnetic Acoustic Transducer) array.
*   **Software Stack:** Python 3.10, OpenCV (Computer Vision), NumPy.
*   **Mounting:** IP67 ruggedized junction box mounted via heavy-duty L-brackets to the trailing bogie.

## Software Simulation & Algorithms
This repository contains the software simulation pipeline used for testing the RTHMS optical corrosion detection logic. 

Because the railway environment is visually "noisy" (consisting of varying gravel ballast, dirt, and tie plates), standard HSV color thresholding often yields false positives. Our approach utilizes **Coordinate ROI (Region of Interest) Masking** combined with targeted **Grayscale Thresholding** to isolate the structural rails and identify deep, non-reflective corrosion patches.

### The Pipeline (`rthms_scanner.py`):
1.  **Image Pre-processing:** Captures the raw camera feed and resizes it for standardized processing.
2.  **Structural Edge Detection:** Converts the image to grayscale, applies a Gaussian Blur to reduce gravel noise, and uses Canny Edge Detection (`cv2.Canny`) to highlight the physical boundaries of the rails.
3.  **Coordinate ROI Masking:** Defines a precise polygonal mask (`cv2.fillPoly`) over the target rail to completely ignore the surrounding ballast track bed. 
4.  **Defect Thresholding:** Applies an Inverse Binary Threshold (`cv2.threshold`) within the masked region. Since severe corrosion and cracks are significantly darker than the reflective steel surface, this isolates the anomalies.
5.  **Morphological Noise Reduction:** Applies `cv2.morphologyEx(MORPH_OPEN)` to remove isolated, harmless dirt specks, ensuring only critical structural defects trigger an alert.
6.  **Bounding Box Generation:** Calculates contours and draws bounding boxes around continuous defect areas exceeding a critical size threshold.

## Installation & Usage
To run the RTHMS software simulation on your local machine:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YourUsername/RTHMS-Edge-AI.git
    cd RTHMS-Edge-AI
    ```
2.  **Install dependencies:**
    ```bash
    pip install opencv-python numpy
    ```
3.  **Run the simulation:** Ensure you have a test image named `track.jpg` in the root directory.
    ```bash
    python rthms_scanner_v5.py
    ```

## Development Team
*   Prasanna Kollu (Computer Science Engineering, Woxsen University)
*   Vishnu Mirapa
*   Pareddy Ishanth Reddy
*   Mitul Saraswat
*   Suragana Sai Dattu

*Developed as part of the Web Technologies & IoT Edge AI Curriculum - Review 3.*

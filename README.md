<div align="center">
  <h1>🚂 Railway Track Health Monitoring System (RTHMS)</h1>
  <h3>Edge AI Last-Coach Architecture</h3>
  <p><i>A Conceptual Project for Semester 3, B.Tech Computer Science Engineering @ Woxsen University</i></p>
</div>

<br />

## 📖 Project Overview
The **Railway Track Health Monitoring System (RTHMS)** is an advanced, conceptual Edge AI computer vision application. Designed to be mounted directly on the trailing bogie (last coach) of a train, this system provides real-time, autonomous scanning of railway tracks. 

By pushing processing entirely to the "edge"—running directly on the device rather than relying on unstable cloud connections in remote areas—RTHMS ensures zero-latency identification of critical defects (IMR triggers). When a severe flaw is detected, the system logs the GPS coordinates for immediate dispatch to maintenance crews.

---

## Hardware Architecture (Conceptual)
The physical sensor node is designed for harsh, real-world railway environments:
*   **Processing Unit:** NVIDIA Jetson Nano / Raspberry Pi 4 (acting as the Edge AI brain)
*   **Sensors:** Downward-facing industrial optical camera & EMAT (Electromagnetic Acoustic Transducer) array for non-contact magnetic scanning
*   **Enclosure:** IP67 ruggedized waterproof junction box
*   **Mounting:** Heavy-duty galvanized steel L-brackets secured to the trailing bogie

---

## Software Pipeline & Computer Vision
This repository hosts the software simulation pipeline used to test and validate the RTHMS optical corrosion detection logic. 

Standard HSV color thresholding often fails in railway environments due to the visual "noise" of gravel ballast, dirt, and rusted tie plates sharing similar color profiles. To solve this, our algorithm uses **Coordinate Region of Interest (ROI) Masking** combined with targeted **Grayscale Thresholding**.

### Algorithm Breakdown (`rthms_scanner.py`):
1.  **Image Pre-processing:** Captures the raw camera feed and standardizes the resolution for dashboard viewing.
2.  **Structural Edge Detection:** Converts the feed to grayscale, applies a Gaussian Blur to suppress gravel noise, and utilizes Canny Edge Detection to highlight physical rail boundaries.
3.  **Polygonal ROI Masking:** Defines a precise coordinate polygon over the target rail, forcing the AI to completely ignore the surrounding track bed and ballast.
4.  **Anomaly Isolation:** Applies an Inverse Binary Threshold within the masked region to locate deep, non-reflective patches indicative of severe corrosion or cracking.
5.  **Morphological Solidification:** Uses `cv2.morphologyEx` (MORPH_OPEN and MORPH_CLOSE) with large kernels to filter out harmless dirt specks and solidify flaky rust into single, cohesive structural alerts.
6.  **Dashboard UI & Bounding Boxes:** Calculates contours and renders thick red bounding boxes around critical defects, overlaying a mission-critical HUD for the operator.

---

## Installation & Simulation
To run the RTHMS software simulation on your local machine:

**1. Clone the repository:**
```bash
git clone https://github.com/YourUsername/RTHMS-Railway-Track-Health-Motoring-System-.git
cd RTHMS-Railway-Track-Health-Motoring-System-
```

**2. Install dependencies:**
```bash
pip install opencv-python numpy
```

**3. Run the simulation:** 
*(Ensure the test image `track.jpg` is located in the root directory)*
```bash
python src/rthms_scanner.py
```

---

## Development Team
This project was conceptualized, designed, and developed by Semester 3 B.Tech CSE students at **Woxsen University, Hyderabad**.

*   **Prasanna Kollu** (Lead Developer)
*   **Vishnu Mirapa**
*   **Pareddy Ishanth Reddy**
*   **Mitul Saraswat**
*   **Suragana Sai Dattu**

*Developed as part of the Conceptual Project at Woxsen Unversity.*

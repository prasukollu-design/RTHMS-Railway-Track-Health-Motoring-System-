import cv2
import numpy as np

def scan_track_health(image_path):
    print(f"RTHMS: Loading track image from {image_path}...")
    
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Could not load image. Make sure 'track.jpg' is in the folder.")
        return

    img = cv2.resize(img, (800, 600))
    cv2.imshow("1. Original Camera Feed", img)

    # --- STAGE 1: EDGE DETECTION (Structural Boundaries) ---
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Increased thresholds to ignore the gravel and only pick up harsh metal edges
    edges = cv2.Canny(blurred, 100, 200)
    
    edges_display = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    cv2.putText(edges_display, "RTHMS EDGE SCAN", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.imshow("2. Structural Edge Detection", edges_display)

    # --- STAGE 2: TARGETED CORROSION DETECTION (Grayscale Thresholding + Mask) ---
    # Create a mask for the right rail to ignore the noisy gravel
    rail_mask = np.zeros(gray.shape, dtype=np.uint8)
    right_rail_pts = np.array([[460, 200], [550, 200], [800, 500], [800, 600], [500, 600]], np.int32)
    cv2.fillPoly(rail_mask, [right_rail_pts], 255)

    # We use the grayscale image. Corrosion/Cracks are usually much darker than shiny steel.
    # We threshold the image to find the dark, non-reflective patches.
    _, defect_mask = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)
    
    # Apply the rail mask so we ONLY look for defects on the right rail
    defect_mask = cv2.bitwise_and(defect_mask, rail_mask)
    
    # Clean up the mask to remove tiny specs of noise
    kernel = np.ones((9,9),np.uint8)
    defect_mask = cv2.morphologyEx(defect_mask, cv2.MORPH_OPEN, kernel)
    
    contours, _ = cv2.findContours(defect_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    corrosion_highlight = img.copy()
    
    anomaly_detected = False
    for contour in contours:
        area = cv2.contourArea(contour)
        
        # Only look for massive, critical patches of corrosion
        if area > 2000: 
            x, y, w, h = cv2.boundingRect(contour)
            
            # Draw a clean Red bounding box for critical defects
            cv2.rectangle(corrosion_highlight, (x, y), (x+w, y+h), (0, 0, 255), 3)
            cv2.rectangle(corrosion_highlight, (x, y-25), (x+150, y), (0, 0, 255), -1) 
            cv2.putText(corrosion_highlight, "CORROSION", (x+5, y-8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            anomaly_detected = True

    # --- INFO OVERLAYS ---
    if anomaly_detected:
        status = "STATUS: CRITICAL CORROSION DETECTED (IMR TRIGGERED)"
        color = (0, 0, 255) # Red
    else:
        status = "STATUS: TRACK SURFACE CLEAR"
        color = (0, 255, 0) # Green
        
    cv2.rectangle(corrosion_highlight, (0, 0), (700, 80), (0, 0, 0), -1) 
    cv2.putText(corrosion_highlight, "RTHMS AI SURFACE SCAN", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(corrosion_highlight, status, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Bottom Legend Banner
    h_img, w_img, _ = corrosion_highlight.shape
    cv2.rectangle(corrosion_highlight, (0, h_img-50), (w_img, h_img), (0, 0, 0), -1)
    cv2.putText(corrosion_highlight, "INFO: RED BOUNDING BOXES INDICATE SEVERE TRACK CORROSION", (10, h_img-20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)


    cv2.imshow("3. Surface Corrosion Scan", corrosion_highlight)

    print("RTHMS: Scan complete. Press any key on the windows to close.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    scan_track_health("track.jpg")

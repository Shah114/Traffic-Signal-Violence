# Importing Modules
import cv2
import os
import numpy as np
from ultralytics import YOLO, solutions

# Path of Main folder
os.chdir(r"C:\Projects\TrafficSignalViolence")

# Arrays of ligths
RedLight = np.array([[998, 125],[998, 155],[972, 152],[970, 127]])
GreenLight = np.array([[971, 200],[996, 200],[1001, 228],[971, 230]])
ROI = np.array([[910, 372],[388, 365],[338, 428],[917, 441]])

# Load model
model = YOLO('yolov8m.pt')
coco = model.model.names

# Taking important variables for our project
TargetLabels = ["bicycle", "car", "motorcycle", "bus", "truck", "traffic light"]

# Main Functions
def is_region_light(image, polygon, brigthness_threshold=128):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    mask = np.zeros_like(gray_image)

    cv2.fillPoly(mask, [np.array(polygon)], 255)

    roi = cv2.bitwise_and(gray_image, gray_image, mask=mask)

    mean_brigtness = cv2.mean(roi, mask=mask)[0]

    return mean_brigtness > brigthness_threshold

def draw_text_with_background(frame, text, position, font, scale, text_color, background_color, border_color, thickness=2, padding=5):
    """This function draw text with background and border on the frame"""
    (text_width, text_height), baseline = cv2.getTextSize(text, font, scale, thickness)
    x, y = position
    # background rectangle
    cv2.rectangle(frame,
                  (x - padding, y - text_height - padding),
                  (x + text_width + padding, y + baseline + padding),
                  background_color,
                  cv2.FILLED)
    # border rectangle
    cv2.rectangle(frame,
                  (x - padding, y - text_height - padding),
                  (x + text_width + padding, y + baseline + padding),
                  border_color,
                  thickness)
    # text
    cv2.putText(frame, text, (x, y), font, scale, text_color, thickness, lineType=cv2.LINE_AA)

# Loading test video
cap = cv2.VideoCapture("C:/Projects/TrafficSignalViolence/example.mp4")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Number of frames have finished.")
        break
    else:
        frame = cv2.resize(frame, (1100, 700))
        cv2.polylines(frame, [RedLight], True, [0, 0, 255], 1)
        cv2.polylines(frame, [GreenLight], True, [0, 255, 0], 1)
        cv2.polylines(frame, [ROI], True, [255, 0, 0], 2)

        results = model.predict(frame, conf=0.75)
        for result in results:
            boxes = result.boxes.xyxy
            confs = result.boxes.conf
            classes = result.boxes.cls

            for box, conf, cls in zip(boxes, confs, classes):
                if coco[int(cls)] in TargetLabels:
                    x, y, w, h = box
                    x, y, w, h = int(x), int(y), int(w), int(h)
                    cv2.rectangle(frame, (x, y), (w, h), [0, 255, 0], 2)
                    draw_text_with_background(frame, 
                                      f"{coco[int(cls)].capitalize()}, conf:{(conf)*100:0.2f}%", 
                                      (x, y - 10), 
                                      cv2.FONT_HERSHEY_COMPLEX, 
                                      0.6, 
                                      (255, 255, 255),  # White text
                                      (0, 0, 0),  # Black background
                                      (0, 0, 255))  # Red border

                if is_region_light(frame, RedLight):
                    if cv2.pointPolygonTest(ROI, (x, y), False) >= 0 or cv2.pointPolygonTest(ROI, (w, h), False) >= 0:
                        draw_text_with_background(frame, 
                                      f"The {coco[int(cls)].capitalize()} violated the traffic signal.", 
                                      (10, 30), 
                                      cv2.FONT_HERSHEY_COMPLEX, 
                                      0.6, 
                                      (255, 255, 255),  # White text
                                      (0, 0, 0),  # Black background
                                      (0, 0, 255))  # Red border

                        cv2.polylines(frame, [ROI], True, [0, 0, 255], 2)
                        cv2.rectangle(frame, (x, y), (w, h), [0, 0, 255], 2)
                        # time.sleep(1)
                               
        # Display the frame
        cv2.imshow("frame", frame)

        # Wait for 1 millisecond and check if 'q' was pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
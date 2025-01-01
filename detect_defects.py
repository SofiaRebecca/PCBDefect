import torch
import cv2
import numpy as np

def detect_and_draw(model_path, input_image_path, output_image_path):
    # Load the YOLO model
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)

    # Read the input image
    image = cv2.imread(input_image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {input_image_path}")

    # Perform inference using mixed precision (autocast for CUDA)
    with torch.amp.autocast('cuda' if torch.cuda.is_available() else 'cpu'):
        results = model(image)

    # Process results
    detections = results.xyxy[0].cpu().numpy()  # Get detections as numpy array
    bboxes = detections[:, :4]  # Bounding boxes
    class_labels = detections[:, -1]  # Class labels

    # Draw bounding boxes on the image
    for bbox, label in zip(bboxes, class_labels):
        x1, y1, x2, y2 = map(int, bbox)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, str(int(label)), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Save the output image
    cv2.imwrite(output_image_path, image)

    return bboxes, class_labels
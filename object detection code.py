import cv2
import time

# Load YOLO model
net = cv2.dnn.readNet(yolov3.weights, yolov3.cfg)
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

# Load class labels
with open(coco.names, r) as f
    classes = [line.strip() for line in f.readlines()]

# load in the video
video_path = assignment_video.mp4
cap = cv2.VideoCapture(video_path)

# video properties
fourcc = cv2.VideoWriter_fourcc(mp4v)
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
fps = int(cap.get(cv2.CAP_PROP_FPS))
output_file = output_video.mp4

# Video Write
out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

# Process frames
frame_count = 0
start_time = time.time()

while cap.isOpened()
    ret, frame = cap.read()
    if not ret or frame is None
        print(End of video or frame could not be read.)
        break

    # YOLO detection
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    detections = net.forward(output_layers)

    for detection in detections
        for obj in detection
            scores = obj[5]
            class_id = scores.argmax()
            confidence = scores[class_id]
            if confidence  0.5
                # Get bounding box coordinates
                center_x, center_y, w, h = (obj[04]  [frame_width, frame_height, frame_width, frame_height]).astype(int)
                x = int(center_x - w  2)
                y = int(center_y - h  2)
                # Draw bounding box and label
                cv2.rectangle(frame, (x, y), (x + int(w), y + int(h)), (0, 255, 0), 2)
                label = f{classes[class_id]} {confidence.2f}
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Write the frame to output
    out.write(frame)

    # print progress per frame
    frame_count += 1
    print(fProcessed {frame_count} frames...)

    #  100 frames only
    if frame_count = 100
        print(Processed 100 frames. Stopping...)
        break

# Release resources
cap.release()
out.release()
end_time = time.time()

print(fProcessing complete. Processed {frame_count} frames.)
print(fOutput video saved as {output_file}.)
print(fTime taken {end_time - start_time.2f} seconds.)

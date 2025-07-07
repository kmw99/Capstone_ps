from ultralytics import YOLO


class YOLODetector:
    def __init__(self, model_path="assets/models/best(reverse).pt"):
        self.model = YOLO(model_path)

    def detect(self, frame):
        result = self.model(frame)[0]
        key_boxes = []
        for box in result.boxes:
            cls_id = int(box.cls[0])
            label = result.names[cls_id]
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            key_boxes.append({
                "label": label,
                "x": x1,
                "y": y1,
                "width": x2 - x1,
                "height": y2 - y1,
                "center_x": (x1 + x2) / 2,
                "center_y": (y1 + y2) / 2
            })
        return key_boxes
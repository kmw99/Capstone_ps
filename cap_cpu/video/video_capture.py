import cv2


class VideoCaptureManager:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("❌ 웹캠을 열 수 없습니다.")

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        frame = cv2.flip(frame, 1)  # 좌우 반전
        return frame
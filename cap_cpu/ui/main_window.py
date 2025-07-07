from PySide6.QtWidgets import QMainWindow, QLabel, QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPixmap, QImage, QKeyEvent
from video.video_capture import VideoCaptureManager
from tracking.hand_tracker import HandTracker
from detection.yolo_detector import YOLODetector
from detection.key_correction import apply_dynamic_transform
from model.click_predictor import ClickPredictor
from input.key_input_manager import KeyInputManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI 모션 키보드 시스템")
        self.setGeometry(100, 100, 960, 720)

        menubar = self.menuBar()
        settings_menu = menubar.addMenu("설정")
        self.dark_mode_action = QAction("다크 모드", self, checkable=True)
        settings_menu.addAction(self.dark_mode_action)

        self.video_label = QLabel()
        self.setCentralWidget(self.video_label)

        self.video_manager = VideoCaptureManager()
        self.hand_tracker = HandTracker()
        self.yolo_detector = YOLODetector()
        self.click_predictor = ClickPredictor()
        self.key_input_manager = KeyInputManager()

        self.reference_initial = {}
        self.reference_current = {}
        self.initial_key_positions = []
        self.corrected_key_boxes = []
        self.captured_initial = False
        self.data_buffer = []
        self.SEQ_LEN = 30

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        frame = self.video_manager.get_frame()
        if frame is not None:
            self.current_frame = frame  # 최근 프레임 저장
            results = self.hand_tracker.process(frame)
            annotated = self.hand_tracker.draw_hand(frame, results)
            key_boxes = self.yolo_detector.detect(frame)

            if self.captured_initial:
                self.reference_current = {k['label']: (k['center_x'], k['center_y']) for k in key_boxes}
                self.corrected_key_boxes = apply_dynamic_transform(
                    self.reference_initial, self.reference_current, self.initial_key_positions
                )

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    z = [hand_landmarks.landmark[8].z]
                    self.data_buffer.append(z)
                    if len(self.data_buffer) > self.SEQ_LEN:
                        self.data_buffer.pop(0)

                    if len(self.data_buffer) == self.SEQ_LEN:
                        pred = self.click_predictor.predict(self.data_buffer)
                        if pred == 1:
                            tip = hand_landmarks.landmark[8]
                            h, w, _ = frame.shape
                            cx, cy = int(tip.x * w), int(tip.y * h)
                            self.key_input_manager.process_click((cx, cy), self.corrected_key_boxes)
                            self.data_buffer.clear()

            self.video_label.setPixmap(QPixmap.fromImage(annotated))

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_S and not self.captured_initial:
            print("📸 키보드 인식 중...")
            frame = getattr(self, 'current_frame', None)
            if frame is not None:
                result = self.yolo_detector.model(frame)[0]
                self.initial_key_positions.clear()
                self.reference_initial.clear()
                for box in result.boxes:
                    cls_id = int(box.cls[0])
                    label = result.names[cls_id]
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    w, h = x2 - x1, y2 - y1
                    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
                    self.initial_key_positions.append({
                        "label": label, "x": x1, "y": y1, "width": w, "height": h,
                        "center_x": cx, "center_y": cy
                    })
                    self.reference_initial[label] = (cx, cy)
                self.captured_initial = True
                print("✅ 초기 키보드 배열 저장 완료.")

        elif event.key() == Qt.Key_Q:
            print("🛑 프로그램 종료 요청")
            self.close()

from pynput.keyboard import Controller
from utils.label_mapping import get_label_mapping


class KeyInputManager:
    def __init__(self):
        self.keyboard = Controller()
        self.label_mapping = get_label_mapping()

    def process_click(self, click_pos, key_boxes):
        cx, cy = click_pos
        for key in key_boxes:
            x1, y1 = key["x"], key["y"]
            x2, y2 = x1 + key["width"], y1 + key["height"]
            if x1 <= cx <= x2 and y1 <= cy <= y2:
                key_label = key["label"]
                print(f"🖱️ Click detected on key: {key_label}")
                key_input = self.label_mapping.get(key["label"])
                # key_input = self.label_mapping.get(key_label)
                if key_input:
                    self.keyboard.press(key_input)
                    self.keyboard.release(key_input)
                break
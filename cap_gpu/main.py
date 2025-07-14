import torch
import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    # --- 프로그램 시작 전 GPU 확인 코드 ---
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("="*40)
    print(f"PyTorch using device: {device}")
    print("="*40)
    # --- 여기까지 ---

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
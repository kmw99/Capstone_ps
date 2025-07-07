import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    import traceback
    print("🟢 프로그램 시작됨")  # 로그 추가
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print("❌ 예외 발생:")
        traceback.print_exc()


if __name__ == "__main__":
    main()
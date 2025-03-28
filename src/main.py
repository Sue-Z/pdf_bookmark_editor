import sys
from PySide6.QtWidgets import QApplication
from pdf_selector import PDFSelector

def main():
    app = QApplication(sys.argv)
    with open("style.qss", "r") as style:
        app.setStyleSheet(style.read())
    window = PDFSelector()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
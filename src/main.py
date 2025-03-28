import sys
from PySide6.QtWidgets import QApplication
from pdf_selector import PDFSelector, PDFBookmarker

def main():
    app = QApplication(sys.argv)
    window = PDFSelector()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
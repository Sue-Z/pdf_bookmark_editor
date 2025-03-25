import sys
from PySide6.QtWidgets import QApplication
from pdf_bookmarker import PDFBookmarker

def main():
    app = QApplication(sys.argv)
    window = PDFBookmarker("test.pdf")
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
from PySide6.QtWidgets import (QWidget, QGridLayout, QFileDialog, QPushButton, 
                               QLabel)
from pdf_bookmarker import PDFBookmarker

class PDFSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.grid = QGridLayout()
        self.setWindowTitle("PDF Bookmark Editor")
        self.setLayout(self.grid)

        label = QLabel("To begin editing PDF bookmarks, please select a PDF")
        self.grid.addWidget(label, 0, 0)

        self.pdf_path = None
        self.pdf_bookmarker = None
        self.choose_pdf()

        self.setMinimumSize(200, 100)

    def choose_pdf(self):
        file_button = QPushButton("Select PDF")
        file_button.clicked.connect(self.choose_pdf_clicked)
        self.grid.addWidget(file_button, 1, 0)

    def choose_pdf_clicked(self):
        self.pdf_path = QFileDialog.getOpenFileName(self, "Select PDF to edit", 
                                                    ".", "PDF Files (*.pdf)")[0]
        if self.pdf_path:
            # If pdf_file was chosen, open PDFBookmarker
            self.pdf_bookmarker = PDFBookmarker(self.pdf_path)
            self.pdf_bookmarker.show()
            self.close()
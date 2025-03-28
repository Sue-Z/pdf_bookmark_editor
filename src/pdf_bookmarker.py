from PySide6.QtWidgets import (QWidget, QGridLayout, QTreeView, QSplitter, 
                               QFileDialog, QPushButton, QMessageBox, 
                               QInputDialog)
from PySide6.QtPdf import QPdfDocument, QPdfBookmarkModel
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtCore import QPointF
import pymupdf

class PDFBookmarker(QWidget):
    def __init__(self, pdf_path):
        super().__init__()
        self.pdf_path = pdf_path
        self.setWindowTitle("PDF Bookmark Editor")
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.setLayout(self.grid)

        self.pdf = None
        self.pdf_view = None
        self.pdf_navigator = None
        self.page_viewer()

        self.bookmarks = None
        self.bookmarks_view = None
        self.bookmarks_viewer()

        self.pdf_viewer()

        self.bookmarks_from_file()
        self.bookmarks_from_file_append()
        self.bookmarks_to_file()

    # Combines the PDF viewer and bookmark viewer widgets and adds them to grid
    def pdf_viewer(self):
        # Splitter makes it so we can resize between the widgets
        splitter = QSplitter(self)
        splitter.addWidget(self.bookmarks_view)
        splitter.addWidget(self.pdf_view)

        self.grid.addWidget(splitter, 0, 0)

    # Creates the PDF viewer
    def page_viewer(self):
        self.pdf = QPdfDocument(self)
        self.pdf.load(self.pdf_path)

        self.pdf_view = QPdfView(self)
        self.pdf_view.setDocument(self.pdf)
        self.pdf_view.setPageMode(QPdfView.PageMode.MultiPage)
        # Set minimum size so the GUI doesn't collapse and make the PDF tiny
        self.pdf_view.setMinimumSize(800, 700) 

        self.pdf_navigator = self.pdf_view.pageNavigator()

    # Creates the bookmark viewer
    def bookmarks_viewer(self):
        self.bookmarks = QPdfBookmarkModel(self)
        self.bookmarks.setDocument(self.pdf)

        self.bookmarks_view = QTreeView(self)
        self.bookmarks_view.setModel(self.bookmarks)
        self.bookmarks_view.setHeaderHidden(True)
        self.bookmarks_view.setMinimumSize(250, 700)

        '''
        clicked is not a regular Python function. It emits a signal which is 
        passed to a slot when connected, so the function called should also 
        accept an "index" argument (if you don't, it still works, which is
        confusing, but this handling might be specific to PySide6, so it 
        may not necessarily work in C++ Qt if you left out the index argument)
        '''
        # The "clicked" emits a signal that's a QModelIndex we can use within 
        # the bookmark_clicked function
        self.bookmarks_view.clicked.connect(self.bookmark_clicked) 

    # Jumps to a page when a particular bookmark is clicked
    def bookmark_clicked(self, index):
        page_num = self.bookmarks.data(index, QPdfBookmarkModel.Role.Page)
        self.pdf_navigator.update(page_num, QPointF(0.0, 0.0), 
                                  self.pdf_navigator.currentZoom())
    
    # Creates button for replacing bookmarks in a PDF from a text file
    def bookmarks_from_file(self):
        file_button = QPushButton("Replace PDF bookmarks from file")
        file_button.clicked.connect(self.from_file_clicked)
        self.grid.addWidget(file_button, 1, 0)

    # Parses the file and adds bookmarks when button to do so is clicked
    def from_file_clicked(self):
        bookmarks_file = QFileDialog.getOpenFileName(self, 
                                                     "Replace PDF bookmarks "
                                                     "from file", ".", 
                                                     "Text Files (*.txt)")[0]
        if not bookmarks_file:
            return

        bookmarks = []
        # Document should be in format: level, page, title
        with open(bookmarks_file, "r") as file:
            for line in file:
                parts = line.split(",", maxsplit=2) # We want 2 splits at most
                if len(parts) < 3:
                    self.error_popup("Invalid file formatting")
                    return
                
                try: 
                    level = int(parts[0].strip())
                    page = int(parts[1].strip())
                    if page < 1 or page > self.pdf.pageCount():
                        # Page number invalid
                        self.error_popup("Invalid page number")
                        return
                    title = parts[2].strip()
                except ValueError: # At least 1 part wasn't int
                    self.error_popup("Invalid level or page")
                    return

                bookmarks.append([level, title, page])

        pdf = pymupdf.open(self.pdf_path)
        pdf.set_toc(bookmarks)
        # Save changes bc changes are only in memory right now
        pdf.save(self.pdf_path, incremental=True, encryption=0) 
        pdf.close()

        # Reinitialize pdf and bookmark viewer
        self.pdf.load(self.pdf_path)
        self.pdf_view.setDocument(self.pdf)
        self.pdf_navigator = self.pdf_view.pageNavigator()

        self.bookmarks.setDocument(self.pdf)
        self.bookmarks_view.setModel(self.bookmarks)

    # Creates button for adding more bookmarks in a PDF from a text file
    def bookmarks_from_file_append(self):
        file_button = QPushButton("Append PDF bookmarks from file")
        file_button.clicked.connect(self.append_file_clicked)
        self.grid.addWidget(file_button, 2, 0)

    # Parses the file and appends bookmarks when button to do so is clicked
    def append_file_clicked(self):
        bookmarks_file = QFileDialog.getOpenFileName(self, 
                                                     "Append PDF bookmarks "
                                                     "from file", ".", 
                                                     "Text Files (*.txt)")[0]
        if not bookmarks_file:
            return
        
        pdf = pymupdf.open(self.pdf_path)
        bookmarks = pdf.get_toc()
        with open(bookmarks_file, "r") as file:
            for line in file:
                parts = line.split(",", maxsplit=2) # We want 2 splits at most
                if len(parts) < 3:
                    self.error_popup("Invalid file formatting")
                    return
                
                try: 
                    level = int(parts[0].strip())
                    page = int(parts[1].strip())
                    if page < 1 or page > self.pdf.pageCount():
                        # Page number invalid
                        self.error_popup("Invalid page number")
                        return
                    title = parts[2].strip()
                except ValueError: # At least 1 part wasn't int
                    self.error_popup("Invalid level or page")
                    return

                bookmarks.append([level, title, page])

        pdf.set_toc(bookmarks)
        # Save changes bc changes are only in memory right now
        pdf.save(self.pdf_path, incremental=True, encryption=0) 
        pdf.close()

        # Reinitialize pdf and bookmark viewer
        self.pdf.load(self.pdf_path)
        self.pdf_view.setDocument(self.pdf)
        self.pdf_navigator = self.pdf_view.pageNavigator()

        self.bookmarks.setDocument(self.pdf)
        self.bookmarks_view.setModel(self.bookmarks)

    # Creates button for extracting bookmarks in a PDF to a text file
    def bookmarks_to_file(self):
        file_button = QPushButton("Extract PDF bookmarks to file")
        file_button.clicked.connect(self.to_file_clicked)
        self.grid.addWidget(file_button, 3, 0)

    # Extracts bookmarks to a text file when button to do so is clicked
    def to_file_clicked(self):
        input, ok = QInputDialog.getText(self, "File name entry", "Enter file "
                                         "name to extract bookmarks to")
        if not ok:
            # User chose cancel, so exit function
            return
        if not input:
            self.error_popup("Invalid file name")
            return

        if ok:
            with open(input, "w") as file:
                pdf = pymupdf.open(self.pdf_path)
                bookmarks = pdf.get_toc()
                for bookmark in bookmarks:
                    file.write(f"{bookmark[0]}, {bookmark[2]}, {bookmark[1]}\n")
                pdf.close()

    # Creates error popup with specified message
    def error_popup(self, msg):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(msg)
        msg_box.setStandardButtons(QMessageBox.Close)
        msg_box.exec()

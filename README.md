# PDF Bookmark Editor
A simple PDF bookmark editor I made after being frustrated by moving bookmarks around and applying bookmarks from one PDF to another. Now made easy with a graphical user interface!

You know that convenient outline that pops up on the left hand side of the PDF
viewer when opening PDFs in a browser? By clicking on each item, you are brought
immediately to that section in the document. That's what PDF bookmarks are.

This program allows you to edit those bookmarks, whether you wish the change the name of the bookmark, the page you want it linked to, or the level of the bookmark.

## Dependencies
You will need to have ```PySide6``` (for the GUI) and ```pymupdf``` (for the bookmark editing) installed:
```
pip install PySide6
pip install pymupdf
```
Or you can install from the ```requirements.txt``` file:
```
pip install -r requirements.txt
```

## Features
### Replacing current bookmarks
With the "Replace PDF bookmarks from file" button, you can replace the current bookmarks with new ones from a text file you provide. Please make sure your text file is in "level, page number, title" format.

For example:
```
1, 1, My PDF Title Page
1, 3, Table of Contents
1, 5, Chapter 1: Introduction
```

### Adding more bookmarks
If you don't want to completely replace the bookmarks in your file and only wish to add new bookmarks, use the "Append PDF bookmarks from file" button. Again, please make sure your text file is in "level, page number, title" format.

### Extracting current bookmarks
With the "Extract PDF bookmarks to file" button, you can send the current bookmarks to a text file. The text file will be in "level, page number, title" format.

You can edit the content of the extracted text file and use the "Replace PDF bookmarks from file" button to apply the changes to the PDF.

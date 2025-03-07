from PyQt5.QtWidgets import QApplication
from gui.gui import MainWindow
import sys

"""Simple Autocorrection app with bigrams"""
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
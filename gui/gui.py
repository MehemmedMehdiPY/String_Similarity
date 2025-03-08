from .constants import SPECIAL_CHARS, DICTIONARY_PATH, BIGRAM_PATH, Customization
from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QMessageBox, QVBoxLayout, QHBoxLayout, 
    QWidget, QListWidget, QListWidgetItem, QAbstractItemView, QLineEdit)
import sys
sys.path.append("../")
from utils.auto_correction import AutoCorrection

class MainWindow(QMainWindow, Customization):
    dict_path = DICTIONARY_PATH
    bigram_path = BIGRAM_PATH
    algorithm_selected = False
    is_last_char_space = False
    
    def __init__(self):
        super().__init__()
        
        # Initiailizing autocorrection method as a corrector
        self.corrector = AutoCorrection(
            dict_path=self.dict_path,
            bigram_path=self.bigram_path,

            # Initializing Levenshtein algorithm
            solver=self.features[0].\
                        algorithms[1]()
            )
        
        self.setWindowTitle("Auto Correction")
        self.setGeometry(700, 200, 400, 600)

        # Input box for the user to write down
        self.input_line = QLineEdit()
        self.input_line.textEdited.connect(self.text_update)
        
        #  Choosing solver (edit distance) algorithm
        self.edit_distance_label = QLabel("Choose an edit distance")
        self.algorithm = self.__create_selection(0)
        self.algorithm.currentRowChanged.connect(lambda: self.algorithm_triggered())

        # Printing the input sentence after typos fixed.
        self.output_text = QLabel()

        # Constructing layouts of the app interface.
        left_layout = self.__construct_layout(self.algorithm)
        right_layout = self.__construct_layout(self.input_line, self.output_text)
        widget = self.__construct_widget(left_layout, right_layout)
        
        self.setCentralWidget(widget)

    def __construct_layout(self, *args):
        layout_right = QVBoxLayout()
        for arg in args:
            layout_right.addWidget(arg)
        return layout_right
    
    def __construct_widget(self, *args):
        layout_final = QHBoxLayout()
        for arg in args:
            layout_final.addLayout(arg)
        widget = QWidget()
        widget.setLayout(layout_final)
        return widget

    def __upload_items(self, selection, idx):
        """
            Uploading algorithm names, such as Levenshtein and DamerauLevenshtein
            to selection section.
        """
        for choice in self.features[idx].choices:
            item = QListWidgetItem(str(choice))
            selection.addItem(item)

    def __create_selection(self, idx):
        """
            Creating selection section for algorithms.
        """
        selection = QListWidget()
        selection.setSelectionMode(QAbstractItemView.NoSelection)
        selection.setGeometry(700, 900, 100, 200)
        self.__upload_items(selection, idx)
        return selection

    def algorithm_triggered(self):
        idx = self.algorithm.currentRow()
        if idx != -1:
            self.algorithm_selected = True
        
        solver = self.features[0].algorithms[idx]()
        self.corrector = AutoCorrection(
            dict_path=self.dict_path,
            bigram_path=self.bigram_path,
            solver=solver)
    
    def detect_typo(self, word: str, word_prev: str = None):
        """Detecting typos and returning alternative word."""
        if word_prev is None:
            word_fixed, _ = self.corrector(word)
        else:
            word_fixed, _ = self.corrector(word_prev, word)
        return word_fixed, word==word_fixed
    
    def fix_typo_if_necessary(self, word):
        word_fixed, flag =  self.detect_typo(word)
        if flag:
            return word
        else:
            return word_fixed 

    def remove_special_chars(self, word):
        return word.translate({ord(char): None for char in SPECIAL_CHARS})

    def text_update(self):
        """
            Updating the input text by removing special characters, 
            fixing typos, and showing it as output text.
        """
        input_text = self.input_line.text()
        if len(input_text) == 0: return
        if input_text[-1] != " ":
            self.is_last_char_space = False
            return 
        if self.is_last_char_space and input_text[-1] == " ": return
        
        input_text_spliit = input_text.split()
        if len(input_text_spliit) == 0: return
        
        input_text = input_text_spliit[-1]
        input_text = self.remove_special_chars(input_text)
        input_text = self.fix_typo_if_necessary(word=input_text)

        input_text_spliit[-1] = input_text
        input_text = " ".join(input_text_spliit)
        
        self.output_text.setText(
            input_text
        )
        
        self.is_last_char_space = True
        
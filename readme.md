# Introduction

The repository integrates edit distance algorithms, namely [Hamming](https://en.wikipedia.org/wiki/Hamming_distance), [Levenshtein](https://en.wikipedia.org/wiki/Levenshtein_distance), [Damerau-Levenshtein](https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance), [Needleman-Wunsch](https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm), [Jaro](https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance) to identify similarities between string sequences. There is a small-scaled project to implement autocorrection that employs any of the afore-mentioned metrics. The project also refers to bigrams to improve the decision-making for selecting the most optimal words.

I have never studied bigrams and tried to do my own intuitive approach to the problem - typos. No AI used for brainstorming or documentation.

# Installation

```bash
pip install -r requirements.txt
```

# Data

The ./data folder contains two files - **dictionary.json** and **bigrams_dictionary.json**:

- ./data/dictionary.json hosts 40,000+ English words and is a post-processed subset set data from [Dictionary of English Words and Definitions](https://www.kaggle.com/datasets/anthonytherrien/dictionary-of-english-words-and-definitions). It contains a structured dictionary with the letters paired with the list of words that have the first character of the same letter.  
- ./data/bigram_dictionary.json is a post-processed data from the books, such as
A High Wind in Jamaica, Deirdre Wed and Other Poems, Essays Towards the History of Painting, The Victim and The Worm, and Poems available in [Gutenberg](https://www.gutenberg.org/). It was structured as a dictionary of dictionaries that show the frequencies of all possible bigrams.


# Usage
Use the code written in app.py to launch user-friendly app.

```python
from PyQt5.QtWidgets import QApplication
from gui.gui import MainWindow
import sys

"""Simple Autocorrection app with bigrams"""
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
```

# License
Copyright free!
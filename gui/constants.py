
SPECIAL_CHARS = []
for i in range(33, 48):
    SPECIAL_CHARS.append(chr(i))

for i in range(58, 65):
    SPECIAL_CHARS.append(chr(i))
    
for i in range(91, 97):
    SPECIAL_CHARS.append(chr(i))

for i in range(123, 127):
    SPECIAL_CHARS.append(chr(i))

SPECIAL_CHARS.remove("'")

DICTIONARY_PATH = "./data/dictionary.json"
BIGRAM_PATH = "./data/bigram_dictionary.json"


import sys
sys.path.append("../")
from utils.edit_distance import DamerauLevenshtein, Levenshtein

class EditDistance:
    choices = ["DamerauLevenshtein", "Levenshtein"]
    algorithms = [DamerauLevenshtein, Levenshtein]
    
class Customization:
    features = [EditDistance]
import json
from .constants import REPLACE
from typing import Tuple
import sys

class AutoCorrection:
    def __init__(self, dict_path: str, bigram_path: str, solver):
        self.dict_path = dict_path
        self.bigram_path = bigram_path

        dictionary = self.load_dictionary()
        bigram = self.load_bigram()

        self.dictionary = dictionary
        self.bigram = bigram

        self.solver = solver

    def __call__(self, *args):
        if len(args) > 2:
            ValueError("Expected one or two inputs but received {} inputs".format(len(args)))
        if len(args) == 2:
            word_1 = args[0].lower()
            word_2 = args[1].lower()
        else:
            word_1 = None
            word_2 = args[0].lower()
        return self.get_fixed_word(word_2, word_1)

    def load_bigram(self):
        with open(self.bigram_path) as f:
            bigram = json.load(f)
        return bigram
    
    def load_dictionary(self):
        with open(self.dict_path) as f:
            dictionary = json.load(f)
        return dictionary
    
    def search_bigrams(self, word_1: str, word_2: str):
        key_1 = word_1[0] + word_2[0]
        if key_1 in self.bigram:
            key_2 = "{} {}".format(word_1, word_2)
            if key_2 in self.bigram[key_1]:
                bigram_frequency = self.bigram[key_1][key_2]
                return bigram_frequency
            else:
                return 1
        else:
            return 1

    def get_fixed_word(self, word_2: str, word_1: str = None):
        if word_1 is not None:
            return self.__get_fixed_word_with_bigram(word_1=word_1, word_2=word_2)
        else:
            return self.__get_fixed_word_without_bigram(word=word_2)
        
    def __get_fixed_word_with_bigram(self, word_2: str, word_1: str):
            chars = self.narrow_down(word_2)
            word_found = ""
            score_min = 1e10
            for char in chars:
                for word_dict in self.dictionary[char]:
                    distance = self.solver(word_2, word_dict)
                    score = distance / self.search_bigrams(word_1, word_dict)
                    if score_min > score:
                        score_min = score
                        word_found = word_dict
            if word_found == "":
                return word_2
            else:
                return word_found, score_min
    
    def __get_fixed_word_without_bigram(self, word: str):
            chars = self.narrow_down(word)
            word_found = ""
            score_min = 1e10
            for char in chars:
                for word_dict in self.dictionary[char]:
                    distance = self.solver(word, word_dict)
                    score = distance
                    if score_min > score:
                        score_min = score
                        word_found = word_dict
            if word_found == "":
                return word
            else:
                return word_found, score_min
            
    def narrow_down(self, word):
        if len(word) == 1:
            return word
        
        char_0 = word[0]
        char_1 = word[1]
        chars = (
            [char_0, char_1] + 
            REPLACE[char_0] + 
            REPLACE[char_1]
            )
        return tuple(set(chars))

if __name__ == "__main__":
    corrector = AutoCorrection(
        dict_path="../../data/dictionary.json",
        bigram_path="../../data/bigram_dictionary.json",
        )
    out = corrector("good", "prson")
    print(out[0])
    print(out[1])
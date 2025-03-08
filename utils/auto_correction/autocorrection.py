import json
from .constants import REPLACE
from typing import Tuple, List, Dict, Union
import sys

class AutoCorrection:
    def __init__(self, dict_path: str, bigram_path: str, solver) -> None:
        """Simplest autocorrection application combined with bigrams
        When initiailized, the function expects one or two inputs as words 
        in order.

        Args:
            dict_path:              the filepath to json file of 40,000 English words dictionary (str)
            bigram_path:            the filepath to json file of bigram dictionary (str)
            solver:                 any edit distance algorithm from utils.edit_distance (Levenshtein, Dumbest, DamerauLevenshtein)
        
        A sentence: I liek playing video games.

        Using the method with one or two words

        ```python3
        # to fix the typo "liek"
        corrector = Autocorrection()
        
        # Only one word
        print(corrector("liek"))

        # Two words used. The first word "I" help the 
        # the corrector to provide correction better.
        print(corrector("I", "liek"))
        ``` 
        """
        self.bigram_path = bigram_path
        self.dict_path = dict_path

        bigram = self.load_bigram()
        dictionary = self.load_dictionary()

        self.bigram = bigram
        self.dictionary = dictionary
        self.solver = solver

    def __call__(self, *args) -> Tuple[str, float]:
        """Running autocorrection with one or two words only."""
        if len(args) > 2:
            ValueError("Expected one or two inputs but received {} inputs".format(len(args)))
        if len(args) == 0:
            ValueError("Expected at least one or two inputs but received none.")

        if len(args) == 2:
            word_1 = args[0].lower()
            word_2 = args[1].lower()
        else:
            word_1 = None
            word_2 = args[0].lower()
        return self.get_fixed_word(word_2, word_1)

    def load_bigram(self) -> Dict[
                            str, 
                            Dict[str, int]
                            ]:
        """Loading bigrams"""
        with open(self.bigram_path) as f:
            bigram = json.load(f)
        return bigram
    
    def load_dictionary(self) -> Dict[str, List[str]]:
        """Loading 40,000 English words dictionary"""
        with open(self.dict_path) as f:
            dictionary = json.load(f)
        return dictionary
    
    def search_bigrams(self, word_1: str, word_2: str) -> int:
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

    def get_fixed_word(self, word_2: str, word_1: str = None) -> Tuple[
                                                                    str, 
                                                                    Union[int, float]
                                                                    ]:
        """
        Args:
            word_1 (optional):         If input, there is a bigram sequence and this parameter
                                       indicates the first bigram word.
            word_2:                    Just a required word input, or 
                                       a second bigram word when word_1 is not None.
        Returns:
            A fixed word and a evaluated score.
        """
        if word_1 is not None:
            return self.__get_fixed_word_with_bigram(word_1=word_1, word_2=word_2)
        else:
            return self.__get_fixed_word_without_bigram(word=word_2)
        
    def __get_fixed_word_with_bigram(self, word_2: str, word_1: str) -> Tuple[str, float]:
            """
            When two input, bigrams are involved.
            Suppose a sentence - "I like"
            Args:
                word_1:         The first word in the bigram sequence, such as "I" (str)
                word_2:         The second word in the bigram sequence, such as "like" (str)
            Returns:
                                A fixed word (str) and a evaluated score (float) 
                                with edit distance and bigram frequency.
            """
            # Potential letters are chosen to search dictionary 
            # instead of iterating through whole.
            chars = self.narrow_down(word_2)
            
            # The best alternative word 
            word_found = ""

            # Score is measured as the division of 
            # edit distance by the frequency of respective bigram.
            # Because the algorithm search for lower distance
            # and higher frequency of bigrams.
            # and minimize the score.
            score_min = 1e10

            for char in chars:
                # (Not all of them) Words are compared with 
                # (potentially) mistyped word
                for word_dict in self.dictionary[char]:

                    # edit distance
                    distance = self.solver(word_2, word_dict)

                    # frequency of bigrams
                    frequency = self.search_bigrams(word_1, word_dict)
                    
                    score = distance / frequency
                    if score_min > score:
                        score_min = score
                        word_found = word_dict

            if word_found == "":
                # Return the input word, if no alternative found
                # -1 indicates no alternative word.
                return word_2, -1
            else:
                return word_found, score_min
    
    def __get_fixed_word_without_bigram(self, word: str) -> Tuple[str, int]:
            """
            When one word input, no bigram is involved into the play.

            Args:
                word:           a potentially mistyped word (str)
            Returns:
                                A fixed word (str) and 
                                a evaluated score (int) with edit distance.
            """
            # Potential letters are chosen to search dictionary 
            # instead of iterating through whole.
            chars = self.narrow_down(word)

            # The best alternative word 
            word_found = ""
            
            score_min = 1e10
            for char in chars:
                # (Not all of them) Words are compared with 
                # (potentially) mistyped word
                for word_dict in self.dictionary[char]:

                    # edit distance
                    distance = self.solver(word, word_dict)

                    score = distance
                    if score_min > score:
                        score_min = score
                        word_found = word_dict
                        
            if word_found == "":
                # Return the input word, if no alternative found
                # -1 indicates no alternative word.
                return word, -1
            else:
                return word_found, score_min
            
    def narrow_down(self, word):
        """
        Narrown down options to search the dictionary faster 
        and more effectively so that not all the words are iterated
        in order to reduce computational complexity. 
        
        The variable REPLACE provides the most common typos 
        as a dictionary of letters.
        """
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
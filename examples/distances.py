import sys
sys.path.append("../")
from utils.edit_distance import Dumbest, Levenshtein, DamerauLevenshtein

word_1 = "_potlte"
word_2 = "bottle"
print("Distances between {} and {}".format(word_1, word_2))

solver = Dumbest()
print("Dumbest distance:", solver(word_1, word_2))

solver = Levenshtein()
print("Levenshtein distance:", solver(word_1, word_2))

solver = DamerauLevenshtein()
print("Damerau-Levevenshtein distance:", solver(word_1, word_2))

import sys
sys.path.append("../")
from utils.edit_distance import Jaro

word_1 = "_potlte"
word_2 = "bottle"
solver = Jaro()
print("Distance between {} and {} is {} as a score".format(
    word_1, 
    word_2, 
    solver(word_1, word_2)
    )
)

print("Distance between {} and {} is {} as a score".format(
    word_2, 
    word_2, 
    solver(word_2, word_2)
    )
)
import sys
sys.path.append("../")
from utils.edit_distance import NeedlemanWunsch

sequence_1 = "ATGGTGCATCTGACTCCTGAGG"
sequence_2 = "ATGGTGCACCTGACTCCTGAGG"
solver = NeedlemanWunsch(match_score=1, mismatch_score=-1, gap_penalty=-1)

print(solver(sequence_1, sequence_2))
print(solver.subproblem_map)
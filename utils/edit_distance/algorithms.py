import numpy as np
from .frameworks import Distance, ScoredDistance
        
class Dumbest():
    def __init__(self):
        pass
    
    def __call__(self, word_1: str, word_2: str):
        self.update_words(word_1=word_1, word_2=word_2)
        count = 0
        for i in range(self.word_1_len):
            count += (self.word_1[i] != self.word_2[i])
        return count + (self.word_2_len - i - 1)
        
    def update_words(self, word_1: str, word_2: str):
        self.word_1 = word_1
        self.word_2 = word_2
        
        self.word_1_len = len(word_1)
        self.word_2_len = len(word_2)

        # Changing the longest word to word_2 variable if word_1 has higher length
        if self.word_1_len > self.word_2_len:
            self.word_1, self.word_2 = self.word_2, self.word_1
            self.word_1_len, self.word_2_len = self.word_2_len, self.word_1_len

class DamerauLevenshtein(Distance):
    def __init__(self):
        pass

    def run(self):
        for i in range(1, self.height):
            for j in range(1, self.width):
                self.step(i, j)

    def step(self, i, j):
        self.subproblem_map[i, j] = min(
            self.subproblem_map[i - 1, j] + 1,                          # delete
            self.subproblem_map[i, j - 1] + 1,                          # insert
            self.subproblem_map[i - 1, j - 1] 
                + (self.word_1[j - 1] != self.word_2[i - 1])            # replace
        )

        if i > 1 and j > 1 and (
                    self.word_1[j - 1] == self.word_2[i - 2]
                    and
                    self.word_1[j - 2] == self.word_2[i - 1]
            ):
            self.subproblem_map[i, j] = min(
                self.subproblem_map[i, j],
                self.subproblem_map[i - 2, j - 2] 
                    + (self.word_1[j - 1] != self.word_2[i - 1])        # transposition
            )

    def update_words(self, word_1: str, word_2: str):
        self.word_1 = word_1
        self.word_2 = word_2

        self.width = len(word_1) + 1
        self.height = len(word_2) + 1
        self.subproblem_map = np.zeros((self.height, self.width)).astype(np.uint8)

        self.subproblem_map[0, :] = np.arange(0, self.width)
        self.subproblem_map[:, 0] = np.arange(0, self.height)

class Hamming(Distance):
    def __init__(self):
        pass

    def check_lengths(self, word_1, word_2):
        if len(word_1) != len(word_2):
            raise ValueError("word_1 {} and word_2 {} have no equal lengths".format(word_1, word_2))

    def run(self):
        for i in range(1, self.dimension):
            self.step(i)

    def step(self, i):
        self.subproblem_map[0, i] = (
            self.subproblem_map[0, i - 1] + (self.word_1[i - 1] != self.word_2[i - 1])
        )
    
    def update_words(self, word_1, word_2):
        self.check_lengths(word_1, word_2)
        self.word_1 = word_1
        self.word_2 = word_2
        self.dimension = len(word_1) + 1
        self.subproblem_map = np.zeros((1, self.dimension)).astype(np.uint8)

class Jaro(ScoredDistance):
    """The following code may have some similarities with https://rosettacode.org/wiki/Jaro_similarity#Python
    I tried to implement my understanding.
    """
    def __init__(self):
        pass

    def get_matches(self):
        count_match = 0
        word_1_cond = [False] * self.word_1_len
        word_2_cond = [False] * self.word_2_len
        
        for i in range(self.word_1_len):
            start_idx = max(0, i - self.match_range)
            end_idx = min(i + self.match_range, self.word_2_len - 1)
            # print(start_idx, end_idx)
            for j in range(start_idx, end_idx + 1):
                if word_2_cond[j]:
                    continue
                if self.word_1[i] == self.word_2[j]:
                    count_match += 1
                    word_1_cond[i] = True
                    word_2_cond[j] = True
                    break
        return count_match, word_1_cond, word_2_cond

    def get_score(self):
        match, word_1_cond, word_2_cond = self.get_matches()
        transposition = self.get_transpositions(word_1_cond, word_2_cond)
        return (
            match / self.word_1_len + 
            match / self.word_2_len + 
            (match - transposition / 2) / match
        ) / 3
    
    def get_transpositions(self, word_1_cond, word_2_cond):
        count_transposition = 0
        j = 0
        for i in range(self.word_1_len):
            cond_1 = word_1_cond[i]
            if not cond_1:
                continue
            for cond_2 in word_2_cond[j:]:
                if cond_2:
                    break
                j += 1
            if self.word_1[i] != self.word_2[j]:
                count_transposition += 1
            j += 1
        return count_transposition

    def run(self):
        self.score = self.get_score()

    def update_words(self, word_1: str, word_2: str):
        self.word_1 = word_1
        self.word_2 = word_2
        
        self.word_1_len = len(word_1)
        self.word_2_len = len(word_2)

        # Changing the longest word to word_2 variable if word_1 has higher length
        if self.word_1_len > self.word_2_len:
            self.word_1, self.word_2 = self.word_2, self.word_1
            self.word_1_len, self.word_2_len = self.word_2_len, self.word_1_len

        self.match_range = self.word_2_len // 2 - 1
        
class NeedlemandWunsch(Distance):
    def __init__(self, match_score: int = 1, mismatch_score: int = -1, gap_penalty: int = -1):
        self.match_score = match_score
        self.mismatch_score = mismatch_score
        self.gap_penalty = gap_penalty

    def run(self):
        for i in range(1, self.height):
            for j in range(1, self.width):
                self.step(i, j)

    def step(self, i, j):
        self.subproblem_map[i, j] = max(
            self.subproblem_map[i - 1, j] + self.gap_penalty,
            self.subproblem_map[i, j - 1] + self.gap_penalty,
            self.subproblem_map[i - 1, j - 1] + (
                        self.match_score 
                                    if (self.word_1[j - 1] == self.word_2[i - 1]) 
                                    else self.mismatch_score
                )
        )

    def update_words(self, word_1, word_2):
        """Here words represent DNA/RNA"""

        self.word_1 = word_1
        self.word_2 = word_2

        self.width = len(word_1) + 1
        self.height = len(word_2) + 1
        self.subproblem_map = np.zeros((self.height, self.width)).astype(np.int8)

        self.subproblem_map[0, :] = -np.arange(0, self.width)
        self.subproblem_map[:, 0] = -np.arange(0, self.height)

class Levenshtein(Distance):
    def __init__(self):
        pass

    def run(self):
        for i in range(1, self.height):
            for j in range(1, self.width):
                self.step(i, j)

    def step(self, i, j):
        self.subproblem_map[i, j] = min(
            self.subproblem_map[i - 1, j] + 1,                          # delete
            self.subproblem_map[i, j - 1] + 1,                          # insert
            self.subproblem_map[i - 1, j - 1] 
                + (self.word_1[j - 1] != self.word_2[i - 1])            # replace
        )

    def update_words(self, word_1: str, word_2: str):
        self.word_1 = word_1
        self.word_2 = word_2

        self.width = len(word_1) + 1
        self.height = len(word_2) + 1
        self.subproblem_map = np.zeros((self.height, self.width)).astype(np.uint8)

        self.subproblem_map[0, :] = np.arange(0, self.width)
        self.subproblem_map[:, 0] = np.arange(0, self.height)

if __name__ == "__main__":
    word_1 = "potlte"
    word_2 = "bottle"
    solver = Levenshtein()
    # solver = DamerauLevenshtein()
    print(solver(word_1, word_2))
    print(solver.subproblem_map)

    sequence_1 = "ATGGTGCATCTGACTCCTGAGG"
    sequence_2 = "ATGGTGCACCTGACTCCTGAGG"
    solver = NeedlemandWunsch()
    print(solver(sequence_1, sequence_2))
    print(solver.subproblem_map)
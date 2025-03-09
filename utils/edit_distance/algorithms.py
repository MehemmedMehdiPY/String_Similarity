import numpy as np
from .frameworks import Distance, ScoredDistance
        
class Dumbest():
    """
    An algorithm proposed by the author of this repo to use as an explanation 
    of distance measurements in a dumbest way possible. Later, issues with the algorithm
    can be analyzed, combined with the potential solutions to mitigate them.

    No more details as a reference since it is just the production of the author.
    """
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
    """
    Damerau-Levenshtein algorithm employs 4 operations - insert, delete, replace, and transpose
    to determine the edit distance between two strings.

    The recursive matrix approach is used by self.step method.

    For more details --> https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance
    """
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
    """
    Hamming distance is the simplest approach that employs only replace operations
    to determine similarity between two strings of the equal lengths. 

    For more details --> https://en.wikipedia.org/wiki/Hamming_distance
    """
    def __init__(self):
        pass

    def check_lengths(self, word_1: str, word_2: str) -> None:
        """
        If not equal lengths, 
        no further computation will be issued.
        """
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
        # Checking lengths of words.
        self.check_lengths(word_1, word_2)

        self.word_1 = word_1
        self.word_2 = word_2
        self.dimension = len(word_1) + 1
        self.subproblem_map = np.zeros((1, self.dimension)).astype(np.uint8)

class Jaro(ScoredDistance):
    """
    Jaro is a scoring technique to evaluate the similarity between two strings between 0 and 1, 
    where 0 indicates absolute no similarity, while 1 is a perfect match.

    The algorithm counts common characters of two strings, combined with the number of transpositions 
    needed to fix the character position in a word for matching.
    
    For more details --> https://rosettacode.org/wiki/Jaro_similarity
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
    """
    Needleman-Wunsch algorithm is a scoring technique to determine
    if two sequences have similarities. Most commonly used in bioinformatics
    as a global alignment technique between DNA sequences.
    Unlike traditional edit distance measurements, the algorithm finds the path 
    that maximisizes the score, instead of minimizing the distance.

    The recursive matrix approach is used by self.step method.

    For more details --> https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm
    """
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
    """
    Levenshtein algorithm employs 3 operations - insert, delete, and replace
    to determine the edit distance between two strings.

    The recursive matrix approach is used by self.step method.

    For more details --> https://en.wikipedia.org/wiki/Levenshtein_distance
    """
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
    solver = Hamming()
    # solver = DamerauLevenshtein()
    print(solver(word_1, word_2))
    print(solver.subproblem_map)

    sequence_1 = "ATGGTGCATCTGACTCCTGAGG"
    sequence_2 = "ATGGTGCACCTGACTCCTGAGG"
    solver = NeedlemandWunsch()
    print(solver(sequence_1, sequence_2))
    print(solver.subproblem_map)

class Distance():
    def __call__(self, word_1: str, word_2: str):
        self.update_words(word_1=word_1, word_2=word_2)
        self.run()
        return self.subproblem_map[-1, -1]

    def update_words(self, word_1: str, word_2: str):
        raise NotImplementedError()

    def run(self):
        raise NotImplementedError()
        
class ScoredDistance():
    def __call__(self, word_1: str, word_2: str):
        self.update_words(word_1=word_1, word_2=word_2)
        self.run()
        return self.score

    def update_words(self, word_1: str, word_2: str):
        raise NotImplementedError()

    def run(self):
        raise NotImplementedError()
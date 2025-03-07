import sys
sys.path.append("../")
from utils.edit_distance import Levenshtein

def wer(reference, hypothesis):
    words_reference = reference.split(" ")
    words_hypothesis = hypothesis.split(" ")
    solver = Levenshtein()
    solver(
        word_1=words_reference,
        word_2=words_hypothesis
    )
    solver.run()
    distance = solver.subproblem_map[-1, -1]
    score = distance / len(words_reference)
    return score
        
def cer(reference, hypothesis):
    solver = Levenshtein()
    solver(
        word_1=reference, 
        word_2=hypothesis
        )
    solver.run()
    distance = solver.subproblem_map[-1, -1]
    score = distance / len(reference)
    return score

if __name__ == "__main__":
    reference_sentence = "I like playing football games."
    hypothesis_sentence = "I liek playing fotball games"

    score_wer = wer(reference=reference_sentence, hypothesis=hypothesis_sentence)    
    score_cer = cer(reference=reference_sentence, hypothesis=hypothesis_sentence)    
    print("Custom cer: {}".format(score_cer))
    print("Custom wer: {}".format(score_wer))
    
    try:
        """Compare it with the existing cer function from jiwer library"""
        from jiwer import cer, wer

        score_cer = cer(reference_sentence, hypothesis_sentence)
        score_wer = wer(reference_sentence, hypothesis_sentence)
        
        print("jiwer cer: {}".format(score_cer))
        print("jiwer wer: {}".format(score_wer))

    except ModuleNotFoundError:
        pass
    
from manim import *
import json
from collections import OrderedDict
import sys
sys.path.append("../../")
from utils.edit_distance import Levenshtein

class ShowEditSteps(Scene):
    def construct(self):
        self.side_length = 0.5
        self.font_size = 25
        
        (word_1, word_2), (width, height) = self.load_log()
        
        self.word_1 = " " + word_1
        self.word_2 = " " + word_2
        self.width = width + 1
        self.height = height + 1
        
        self.start_coord = self.get_start_position()

        self.solver = Levenshtein()
        self.solver(word_1=self.word_1[1:], word_2=self.word_2[1:])

        group_squares, coords = self.get_squares()
        self.coords = coords

        group_words = self.put_words()

        group_row = self.put_row()
        group_column = self.put_column()

        self.play(group_squares, run_time=2)
        self.wait()

        self.play(group_words, run_time=1)
        self.wait()

        self.play(group_row, run_time=1)
        self.wait()

        self.play(group_column, run_time=1)
        self.wait()

        self.remove(group_squares)
        self.wait()

        self.play_steps()

    def explanatory_guideline(self, i, j, initialization=True):
        """Under the development"""
        if initialization:
            msg = ""
            pass
        else:
            left = self.solver.subproblem_map[i, j - 1]
            top = self.solver.subproblem_map[i - 1, j]
            diagonal = self.solver.subproblem_map[i - 1, j - 1]
            
            combined_arr = np.array([left, top, diagonal])
            min_idx = combined_arr.argmin()

            if self.word_1[j] != self.word_2[i]:
                msg_1 = "{} != {}\nTake the minimum of left {} diagonal {} and top {}".format(
                    self.word_1[j], self.word_2[i],
                    left, diagonal, top,
                    )
                msg_2 = "The new value becomes {} + 1 = {}".format(
                    combined_arr[min_idx], combined_arr[min_idx] + 1
                )
            else:
                msg_1 = "{} == {}\nTake the previous diagonal value of {}".format(
                    self.word_1[j], self.word_2[i],
                    self.solver.subproblem_map[i - 1, j - 1]
                )
                msg_2 = "The new value becomes {}".format(self.solver.subproblem_map[i - 1, j - 1])
                
    def get_squares(self):
        coords = OrderedDict()
        squares = []
        for i in range(self.height):
            for j in range(self.width):
                new_coord = [self.start_coord[0] - i / 2, self.start_coord[1] + j / 2]

                square = Square(side_length=self.side_length)
                square.set_coord(new_coord[0], 1)
                square.set_coord(new_coord[1], 0)
                squares.append(Create(square))

                coords["coord_{}_{}".format(i, j)] = new_coord
        group = AnimationGroup(*squares)
        return group, coords
    
    def get_start_position(self):
        upper = self.height / 2
        left = self.width / 2
        return [upper, -left]

    def load_log(self):
        with open("../logs/words.json") as f:
            words = json.load(f)
            word_1 = words["words"]["word_1"]
            word_2 = words["words"]["word_2"]
            width = len(word_1)
            height = len(word_2)        
        return (word_1, word_2), (width, height)

    def put_words(self):
        chars_1 = list(self.word_1)
        chars_2 = list(self.word_2)
        
        texts = []

        for j, char in enumerate(chars_1):
            if char == " ": continue

            coord = self.coords["coord_{}_{}".format(0, str(j))]
            text = Text(char, font_size=int(self.font_size * 1.5))
            text.set_coord(coord[0] + 1/2, 1)
            text.set_coord(coord[1], 0)
            texts.append(Create(text))
        
        for i, char in enumerate(chars_2):
            if char == " ": continue
            
            coord = self.coords["coord_{}_{}".format(str(i), 0)]
            text = Text(char, font_size=int(self.font_size * 1.5))
            text.set_coord(coord[0], 1)
            text.set_coord(coord[1] - 1/2, 0)
            text.rotate(angle=(np.pi / 2))
            texts.append(Create(text))
            
        group = AnimationGroup(texts)
        return group

    def put_row(self):
        integers = self.solver.subproblem_map[0, :].tolist()
        texts = []
        for j, integer in enumerate(integers):
            text = Text(str(integer), font_size=self.font_size)
            text.set_coord(self.coords["coord_{}_{}".format(0, j)][0], 1)
            text.set_coord(self.coords["coord_{}_{}".format(0, j)][1], 0)
            texts.append(Create(text))
        return texts

    def put_column(self):
        integers = self.solver.subproblem_map[:, 0].tolist()
        texts = []
        for i, integer in enumerate(integers):
            text = Text(str(integer), font_size=self.font_size)
            text.set_coord(self.coords["coord_{}_{}".format(i, 0)][0], 1)
            text.set_coord(self.coords["coord_{}_{}".format(i, 0)][1], 0)
            texts.append(Create(text))
        return texts[1:]

    def put_integer(self, i, j):
        integer = self.solver.subproblem_map[i][j]
        text = Text(str(integer), font_size=self.font_size)
        text.set_coord(self.coords["coord_{}_{}".format(i, j)][0], 1)
        text.set_coord(self.coords["coord_{}_{}".format(i, j)][1], 0)
        return text

    def play_steps(self):
        for i in range(1, self.height):
            for j in range(1, self.width):
                self.step(i, j)
                text = self.put_integer(i, j)
                self.play(Create(text), run_time=1)
                
            self.wait()

    def step(self, i, j):
        self.solver.step(i, j)
        # self.explanatory_guideline(i, j, initialization=False)

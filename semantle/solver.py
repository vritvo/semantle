#!/usr/bin/env python3

from semantle import Semantle
from gensim.models import KeyedVectors

class Solver:

    def __init__(self, semantle: Semantle):
        self.semantle = semantle
        self.wv = semantle.model.wv
        self.guesses = {'elementary': {}, 'green': {}, 'volume': {}}
        self.rounding_value = '.2f'
        
    def get_similarity_score(self, guessed_word):
        _, self.similarity_score = self.semantle.check_guess(guessed_word)
    
    def generate_vocab_distance_table(self, guessed_word):
        vocab = self.wv.key_to_index
        distances = self.wv.distances(guessed_word)
        vocab_distances = {v: format(d, self.rounding_value) for v, d in zip(vocab, distances)}

        return vocab_distances

    def collect_potential_answers(self, guessed_word, vocab_distances):
        target_similarity_score = format(1 - self.similarity_score, '.2f')
        print(target_similarity_score)
        potential_answers = []
        for key in vocab_distances:
            if vocab_distances[key] == target_similarity_score:
                potential_answers.append(key)
        return potential_answers

    def triangulate(self):
        for guess in self.guesses.keys():
            similarity_score = self.get_similarity_score(guess)
            vocab_distances = self.generate_vocab_distance_table(guess)
            potential_answers = self.collect_potential_answers(guess, vocab_distances)
            for potential_answer in potential_answers:
                self.guesses[guess][potential_answer] = True

    def identify_solution(self):
        keys = list(self.guesses.keys())
        for word in list(self.guesses[keys[0]].keys()):
            if self.guesses[keys[1]].get(word) and self.guesses[keys[2]].get(word):
                return word

if __name__ == "__main__":
    s = Solver(Semantle())
    s.triangulate()
    solution = s.identify_solution()
    print(f"{solution} is the solution to today's Semantle")


from semantle.semantle import Semantle
from gensim.models import KeyedVectors


class Solver:
    def __init__(self, semantle: Semantle):
        self.semantle = semantle
        self.wv: KeyedVectors = (
            semantle.model
        )  # Google News model is already a KeyedVectors object
        self.guesses: dict[str, dict[str, bool]] = {
            "elementary": {},
            "green": {},
            "volume": {},
        }
        self.rounding_value = ".2f"
        self.similarity_score: float  # Will be set by get_similarity_score

    def get_similarity_score(self, guessed_word: str) -> None:
        """
        Assigns the similarity score of a given guess to a variable.
        """
        score = self.semantle.check_guess(guessed_word)
        if score is None:
            raise ValueError(f"Word '{guessed_word}' not found in vocabulary")
        self.similarity_score = score

    def generate_vocab_distance_table(self, guessed_word: str) -> dict[str, str]:
        """
        Calculates the distances of a given word to every other word in the model vocabulary.
        """
        vocab_keys = list(self.wv.key_to_index.keys())
        # Ensure all keys are strings (they should be in Word2Vec models)
        vocab: list[str] = [str(key) for key in vocab_keys]
        distances = self.wv.distances(guessed_word)
        assert len(vocab) == len(distances), (
            "vocab and vocab distances should be of equal length"
        )
        vocab_distances = {
            v: format(d, self.rounding_value) for v, d in zip(vocab, distances)
        }

        return vocab_distances

    def collect_potential_answers(
        self, guessed_word: str, vocab_distances: dict[str, str]
    ) -> list[str]:
        """
        Calculates the similarity score of the word of the day two a two point precision
        and filters the vocab_distances table down to words with that value
        """
        target_similarity_score = format(1 - self.similarity_score, ".2f")
        print(target_similarity_score)
        potential_answers = []
        for key in vocab_distances:
            if vocab_distances[key] == target_similarity_score:
                potential_answers.append(key)
        return potential_answers

    def create_answer_table(self) -> None:
        """
        Creates the table of potential answers for each guess.
        """
        for guess in self.guesses:
            self.get_similarity_score(guess)
            vocab_distances = self.generate_vocab_distance_table(guess)
            potential_answers = self.collect_potential_answers(guess, vocab_distances)
            for potential_answer in potential_answers:
                self.guesses[guess][potential_answer] = True

    def identify_solution(self) -> str:
        """
        Identifies the one word shared between all of the potential_answers tables for each guess
        """
        keys = list(self.guesses.keys())
        for word in list(self.guesses[keys[0]]):
            if self.guesses[keys[1]].get(word) and self.guesses[keys[2]].get(word):
                return word

        # If no solution is found in the intersection, raise an error
        raise ValueError("No solution found in the intersection of potential answers")

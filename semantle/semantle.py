import time
import os
import gensim
import csv

ROOT_DIR = os.path.abspath(".")

class MyCorpus:
    """An iterator that yields sentences (lists of str)."""

    def __iter__(self):
        corpus_path = ROOT_DIR + "/semantle/data/simpsons_script_lines.csv"
        with open(corpus_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
            for row in reader:
                yield (row["normalized_text"].split())


class Semantle:

    def __init__(self):
        # TODO: Figure out how to use GoogleNews300 model
        # When loaded using gensim.downloader.load('word2vec-google-news-300') the model we get out is a KeyedVectors object, which doesn't work the same as a Word2Vec object
        if not os.path.exists(ROOT_DIR + "/semantle/data/simpsons.model"):
            self.sentences = MyCorpus()
            self.model = gensim.models.Word2Vec(
                sentences=self.sentences, vector_size=300, min_count=5
            )
            self.model.save(ROOT_DIR + "/semantle/data/simpsons.model")
        else:
            self.model = gensim.models.Word2Vec.load(
                ROOT_DIR + "/semantle/data/simpsons.model"
            )

        self.common_word_list = self.get_common_word_list()
        self.word_of_the_day = "bart"
        self.guesses_dict = {}
        self.guesses_in_order = []
        self.endgame = False

    def get_common_word_list(self) -> list[str]:
        """
        Reads in a list of the 5000 most popular words in the English
        language to select for the word of the day.
        """
        path = "semantle/data/popular.txt"  # initially sourced from https://github.com/dolph/dictionary
        common_word_list = []
        with open(path, "r") as file:
            for line in file:
                line = line.strip()
                common_word_list.append(line)
        return common_word_list

    def player_guess(self) -> str:
        """
        Handles the user input for a guess.
        """
        guess = input("Guess: ")
        cleaned_guess = guess.lower()
        return cleaned_guess

    def take_turn(self) -> None:
        """
        Takes in the user's guess, updates the game log, and gives the
        player feedback on their guess.
        """
        similarity_of_current_guess = None

        while similarity_of_current_guess is None:
            current_guess = self.player_guess()
            similarity_of_current_guess = self.check_guess(current_guess)

        self.guesses_dict[current_guess] = similarity_of_current_guess
        self.guesses_in_order.append(current_guess)
        print(f"{current_guess}: {similarity_of_current_guess}")
        self.update_game_state(current_guess)

    def check_guess(self, guess) -> float | None:
        """
        Calculates the similarity of the current guess if the guessed word
        is in the vocabulary of the game model.
        """
        try:
            similarity_of_current_guess = self.model.wv.similarity(
                guess, self.word_of_the_day
            )
            return similarity_of_current_guess
        except Exception as _:
            return None

    def update_game_state(self, current_guess) -> None:
        """
        Sets the game state to end if the user guesses the correct word.
        """
        self.endgame = current_guess == self.word_of_the_day


if __name__ == "__main__":
    print("loading...")
    ct = time.time()
    semantle = Semantle()
    ft = time.time()
    print(f"Loaded in {ft - ct}")
    while not semantle.endgame:
        semantle.take_turn()

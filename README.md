# Semantle

This is a recreation of the game [Semantle](semantle.com) in Python and an accompanying solver. Semantle is a word guessing game where the user attempts to guess a word using the [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity) of their most recent guess to the target word.

This implementation uses the Google News Word2Vec model with 300-dimensional vectors trained on billions of words, providing comprehensive semantic similarity calculations.

## The Solver

The original Semantle game provides information on the Word2Vec model used to power the game in its [FAQ](https://semantle.com/faq). With this information and the Google News Word2Vec model, it's possible to create a solver that filters down to the answer in 3 guesses or fewer. `solver.py` implements this approach by hard-coding three guesses ("elementary", "green", "volume") and generating the vector distance table between those words and every other word in the model vocabulary. Once the cosine similarity distances are given for those three words, the solver filters the tables down to only words with that same distance. The one word shared between those three tables is the solution.

## Running the Application

The project uses the pre-trained Google News Word2Vec model, so no custom dataset is required. The model will be automatically downloaded on first run.

Set up your dependencies with `uv sync` and run the application with `uv run python main.py`.
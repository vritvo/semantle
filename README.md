# Semantle

This is a recreation of the game [Semantle](semantle.com) in Python and an accompanying solver. Semantle is a word guessing game where the user attempts to guess a word using the [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity) of their most recent guess to the target word. 

## The Solver

The original Semantle game provides information on the Word2Vec model used to power the game in its [FAQ](https://semantle.com/faq). With this information and a rough guess at the potential word list used, it's possible to create a solver that filters down to the answer in 3 guesses or fewer. `solver.py` implements this approach by hard-coding three guesses and generating the vector distance table between those words and every other word in the corpus of data. Once the cosine similarity distances are given for those three words the solver filters the tables down to only words with that same distance. The one word shared between those three tables is the solution. 

## Running the Files

A small test dataset is included in the project to test the method. If you want to run this project on the original Semantle dataset you can run ... [TODO]

Set up your dependencies with `uv sync` and run the solver with `uv run semantle/solver.py`. 
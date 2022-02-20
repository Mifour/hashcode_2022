from collections import Counter
from challenge import challenge
import random
import itertools


def solver(problem):
    ingredients = list(set(itertools.chain.from_iterable(itertools.chain.from_iterable(problem))))

    # Initial hype
    likes = Counter()
    dislikes = Counter()
    for like, dislike in problem:
        likes.update(like)
        dislikes.update(dislike)

    average = {
        key: likes.get(key, 0) - dislikes.get(key, 0)
        for key in ingredients
    }
    initial_solution = [ingredient for ingredient, hype in average.items() if hype > 0]
    initial_solution = [int(ingredient in initial_solution) for ingredient in ingredients]

    # Genetic algorithm
    def score(matrix):
        solution = [ingredients[i] for i, x in enumerate(matrix) if x]
        return challenge.score(solution, problem)

    n_pop = 100
    n_top = 50
    gens = 1000
    mutation = 20/100
    pop = [[random.randint(0, 1) for _ in range(len(ingredients))] for _ in range(n_pop)]
    # pop = [initial_solution.copy() for _ in range(n_pop)]

    for gen in range(gens):
        scores = [score(p) for p in pop]
        top_range = sorted(scores, reverse=True)[:n_top]
        min_score, max_score = min(top_range), max(top_range)
        print("TOP SCORE", max_score)
        pop = [pop[i] for i, score in enumerate(scores) if score >= min_score]
        for _ in range(n_pop-len(pop)):
            # Best solutions make babies
            baby = random.choice(pop).copy()

            # Mutation
            for _ in range(int(len(ingredients)*mutation)):
                baby[random.randint(0, len(ingredients))-1] = random.randint(0, 1)
            pop.append(baby)


problem = challenge.problems["d.txt"]
solver(problem)

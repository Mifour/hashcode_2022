from collections import Counter
from random import random, choice


def score(solution):
    solution = set(solution)

    return sum(
        set(like).issubset(solution) and set(dislike).isdisjoint(solution)
        for like, dislike in problem
    )


def load(file):
    with open(f"./problems/{file}", "r") as file:
        data = file.readlines()

    return [
        [
            like.strip().split()[1:],
            dislike.strip().split()[1:],
        ] for like, dislike in zip(data[1::2], data[2::2])]


def save(solution):
    with open(f"./solutions/{file}", "w") as f:
        f.write(str(len(solution)) + " "+" ".join(solution))


def solver(problem):
    likes = Counter([ingredient for like, dislike in problem for ingredient in like])
    dislikes = Counter([ingredient for like, dislike in problem for ingredient in dislike])
    ingredients = set(likes) | set(dislikes)
    average = {
        key: likes.get(key, 0) - dislikes.get(key, 0)
        for key in ingredients
    }
    best_solution = [ingredient for ingredient, hype in average.items() if hype > 0]
    best_score = score(best_solution)

    for _ in range(100000):
        solution = best_solution.copy()

        if random() > .5:
            solution.remove(choice(solution))
        else:
            missing_ingredients = list(ingredients-set(solution))
            solution.append(choice(missing_ingredients))

        new_score = score(solution)

        if new_score > best_score:
            print("HIGHSCORE", new_score)
            best_solution = solution
            best_score = new_score
            if best_score > 1778:
                save(best_solution)

    return solution


file = "d.txt"
problem = load(file)
solution = solver(problem)

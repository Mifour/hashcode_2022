from collections import Counter
from challenge import challenge

def score(solution, problem):
    solution = set(solution)

    return sum(
        set(like).issubset(solution) and set(dislike).isdisjoint(solution)
        for like, dislike in problem
    )

def load_problem(path):
    with open(path, "r") as file:
        data = file.readlines()
    return [[like.strip().split()[1:],dislike.strip().split()[1:],] for like, dislike in zip(data[1::2], data[2::2])]

def solver_generator(problem):
    likes = Counter()
    dislikes = Counter()
    for like, dislike in problem:
        likes.update(like)
        dislikes.update(dislike)

    ingredients = tuple(list(set(likes) | set(dislikes)))

    number = 0
    while number < 2**len(ingredients):
        binary =  bin(number)[2:]
        mask = "0" * (len(ingredients) - len(binary) ) + binary
        mask = [int(c) for c in mask]
        to_keep = [ingr for ingr, keep in zip(ingredients, mask) if keep]
        yield to_keep
        number += 1

problem = load_problem("problems/d.txt")

best_score = float("-inf")
for sol in solver_generator(problem):
    current_score = score(sol, problem)
    if current_score > best_score:
        best_score = current_score
        best_sol = sol
    print(".", end="", flush=True)

print(f"\nbest score: {best_score}\nsolution: {best_sol}")


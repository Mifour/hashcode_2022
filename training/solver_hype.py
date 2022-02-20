from collections import Counter
from problem import problem


def solver(problem):
    likes = Counter()
    dislikes = Counter()
    for like, dislike in problem:
        likes.update(like)
        dislikes.update(dislike)

    ingredients = set(likes) | set(dislikes)
    average = {
        key: likes.get(key, 0) - dislikes.get(key, 0)
        for key in ingredients
    }
    to_keep = [ingredient for ingredient, hype in average.items() if hype > 0]
    return to_keep


problem.test(solver)
print(problem)
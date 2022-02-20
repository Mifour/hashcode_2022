from collections import Counter
from challenge import challenge
from random import random


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
    to_keep = [ingredient for ingredient, hype in average.items() if hype+random() > 0]
    return to_keep


challenge.test(solver, 50)
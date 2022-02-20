from collections import Counter
import sys


def load(filepath):
    with open(filepath, "r") as file:
        data = file.readlines()

    return [
        [
            like.strip().split()[1:],
            dislike.strip().split()[1:],
        ] for like, dislike in zip(data[1::2], data[2::2])]


def write_answer(answer):
    buffer = str(len(answer)) + " "+" ".join(answer)
    sys.stdout.buffer.write(buffer.encode())


def solve(inputs):
    likes = Counter()
    dislikes = Counter()
    for like, dislike in inputs:
        likes.update(like)
        dislikes.update(dislike)

    ingredients = set(likes) | set(dislikes)
    average = {
        key: likes.get(key, 0) - dislikes.get(key, 0)
        for key in ingredients
    }
    to_keep = [ingredient for ingredient, hype in average.items() if hype > 0]
    return to_keep


def scoring(inputs, answer):
    answer = set(answer)

    return sum(
        set(like).issubset(answer) and set(dislike).isdisjoint(answer)
        for like, dislike in inputs
    )


inputs = load("./a_an_example.in.txt")
answer = solve(inputs)
print("Answer", answer)
print("Score", scoring(inputs, answer))

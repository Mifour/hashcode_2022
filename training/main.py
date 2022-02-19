import argparse
from collections import Counter
import sys

def main(number, inputs):
	answer = (0, [])
	likes = Counter()
	dislikes = Counter()
	for like, dislike in inputs:
		likes.update(like.split()[1:])
		dislikes.update(dislike.split()[1:])
	all_ingredients = set(likes.keys()) | set(dislikes.keys())
	average = {
		key: likes.get(key, 0) - dislikes.get(key, 0)
		for key in all_ingredients
	}
	to_keep = []
	for ingredient, hype in average.items():
		if hype > 0:
			to_keep.append(ingredient)
	answer = (len(to_keep), to_keep)
	return answer


def initialize(filepath):
	with open(filepath, "r") as file:
		data = file.readlines()
	number = data[0]
	inputs = []
	for i in range(1, len(data)-1, 2):
		inputs.append((data[i], data[i+1]))
	return number, inputs


def format_answer(answer):
	buffer = str(answer[0])
	for ingredient in answer[1]:
		buffer += " " + ingredient
	return buffer


parser = argparse.ArgumentParser()
parser.add_argument("filepath", type=str)
args = parser.parse_args()
filepath = args.filepath

number, inputs = initialize(filepath)
answer = main(number, inputs)
buffer = format_answer(answer)
sys.stdout.buffer.write(buffer.encode())

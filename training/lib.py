from pathlib import Path
from lib import *
from abc import ABC, abstractmethod


class Problem(ABC):
    def __init__(self, path="./") -> None:
        self.path = Path(path)

        # Load problems
        self.problems = {file.name: self.load_problem(file) for file in (self.path/"problems").iterdir()}

        # Load best solutions
        self.high_scores = {}
        for problem_name, problem in self.problems.items():
            solution_file = self.path/"solutions"/problem_name

            if solution_file.exists():
                with open(solution_file, 'r') as f:
                    solution = self.decode_solution(f.read())
                high_score = self.score(solution, problem)
            else:
                high_score = 0
            self.high_scores[problem_name] = high_score

    def test(self, solver, rounds=1):
        # Test solver on every problem
        for problem_name, problem in self.problems.items():
            for round in range(rounds):
                solution = solver(problem)
                score = self.score(solution, problem)

                # Save highscores
                if score > self.high_scores.get(problem_name, 0):
                    self.high_scores[problem_name] = score
                    print(f"🎉 NEW HIGHSCORE FOR {problem_name}: {score}")
                    with open(self.path/"solutions"/problem_name, 'w') as f:
                        f.write(self.encode_solution(solution))

    @abstractmethod
    def load_problem():
        pass

    @abstractmethod
    def score():
        pass

    @abstractmethod
    def encode_solution():
        pass

    @abstractmethod
    def decode_solution():
        pass

    @abstractmethod
    def decode_solution():
        pass

from pathlib import Path
from abc import ABC, abstractmethod
import importlib.util


class Problem(ABC):
    def __init__(self, path="./") -> None:
        self.path = Path(path)
        self.load_problems()
        self.load_highscores()

    def __repr__(self):
        txt = "\nHIGHSCORES\n"
        for problem in sorted(self.problems):
            txt += f"{problem.ljust(15)} {self.high_scores.get(problem)}\n"
        return txt

    def load_problems(self):
        self.problems = {file.name: self.load_problem(file) for file in (self.path/"problems").iterdir()}

    def load_highscores(self):
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

    def load_solvers(self):
        self.solvers = {}
        for file in (self.path/"solvers").iterdir():
            if file.suffix != ".py":
                continue
            spec = importlib.util.spec_from_file_location(file.stem, file)
            modulevar = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulevar)
            solver = modulevar.solver
            self.solvers[file.stem] = solver

    def test(self, solver, rounds=1):
        # Test solver on every problem
        for problem_name, problem in self.problems.items():
            round_highscore = 0
            problem_highscore = self.high_scores.get(problem_name, 0)

            for round in range(rounds):
                solution = solver(problem)
                score = self.score(solution, problem)

                if score > round_highscore:
                    round_highscore = score

                if score > problem_highscore:
                    self.high_scores[problem_name] = score
                    with open(self.path/"solutions"/problem_name, 'w') as f:
                        f.write(self.encode_solution(solution))

            print(problem_name.ljust(20), end="")
            print(str(round_highscore).ljust(5), end="")

            if round_highscore == 0:
                print("❌  ZERO")
            else:
                difference = (round_highscore/problem_highscore-1)*100
                if difference == 0:
                    print("🆗  SAME")
                elif difference < 0:
                    print(f"❌ {difference:.1f}%")
                else:
                    print(f"🎉 +{difference:.1f}%")

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

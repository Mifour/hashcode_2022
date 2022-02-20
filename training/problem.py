from lib import Problem


class TrainingProblem(Problem):
    def load_problem(self, path):
        with open(path, "r") as file:
            data = file.readlines()

        return [
            [
                like.strip().split()[1:],
                dislike.strip().split()[1:],
            ] for like, dislike in zip(data[1::2], data[2::2])]

    def score(self, solution, problem):
        solution = set(solution)

        return sum(
            set(like).issubset(solution) and set(dislike).isdisjoint(solution)
            for like, dislike in problem
        )

    def encode_solution(self, solution):
        return str(len(solution)) + " "+" ".join(solution)

    def decode_solution(self, raw):
        return raw.strip().split()[1:]

problem = TrainingProblem()
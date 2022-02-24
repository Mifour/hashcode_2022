from lib import Challenge


class Round1Challenge(Challenge):
    def load_problem(self, path):
        with open(path, "r") as file:
            data = file.readlines()

        return [
            [
                like.strip().split()[1:],
                dislike.strip().split()[1:],
            ] for like, dislike in zip(data[1::2], data[2::2])]

    def score(self, solution, problem):
        return 0

    def encode_solution(self, solution):
        return str(len(solution))+"\n"+'\n'.join([project+'\n'+' '.join(workers) for project, workers in solution])

    def decode_solution(self, raw):
        projects = []
        for project, workers in zip(raw[1::2], raw[2::2]):
            workers = workers.split()
            projects.append([project, workers])
        return projects


challenge = Round1Challenge()


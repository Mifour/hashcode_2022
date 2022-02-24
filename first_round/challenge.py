from lib import Challenge


class TrainingChallenge(Challenge):
    def load_problem(self, path):
        with open(path, "r") as file:
            data = file.readlines()
        people = {}
        projects = {}
        line = 0
        n_people, n_projects = [int(n) for n in data[line].split()]
        line += 1
        for _ in range(n_people):
            name, n_comp = data[line].split()
            people[name] = {}
            n_comp = int(n_comp)
            for n in range(1, n_comp+1):
                comp, level = data[line + n].split()
                people[name][comp] = int(level)
            line += n + 1
        for _ in range(n_projects):
            project_name, duration, max_score, best_before, n_roles = data[line].split()
            projects[project_name] = {
                "duration": int(duration),
                "max_score": int(max_score),
                "best_before": best_before, 
                "roles":{}
            }
            for n in range(1, int(n_roles)+1):
                role, level = data[line+n].split()
                projects[project_name]["roles"][role] = int(level)
            line += n + 1
        return people, projects


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

challenge = TrainingChallenge()
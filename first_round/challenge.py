from lib import Challenge


class Round1Challenge(Challenge):
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


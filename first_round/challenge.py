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
                "best_before": int(best_before),
                "roles": []  # this is a list to keep order of roles
            }
            for n in range(1, int(n_roles)+1):
                role, level = data[line+n].split()
                projects[project_name]["roles"].append({"name": role, "level": int(level)})
            line += n + 1
        return people, projects

    def score(self, solution, problem):
        return 0

    def encode_solution(self, solution):
        return str(len(solution))+"\n"+'\n'.join([project+'\n'+' '.join(workers) for project, workers in solution])

    def decode_solution(self, raw):
        raw = raw.split('\n')
        projects = []
        for project, workers in zip(raw[1::2], raw[2::2]):
            workers = workers.split()
            projects.append([project, workers])
        return projects


challenge = Round1Challenge()

# Debug
problem = challenge.problems['a.txt']
with open('./solutions/a.txt', 'r') as f:
    solution = challenge.decode_solution(f.read())


people, projects = problem
print(people)


def scoring(problem, solution):
    total_score = 0
    available = {p: [] for p in people}
    # we can determine if project are run in parallele if they are different set of people

    for project_name, workers in solution:
        project = projects[project_name]
        print(workers)
        print(project)
        score = 0
        project_start = 0
        initial_award = project["max_score"]
        best_before = project["best_before"]
        duration = project["duration"]
        print(available)
        while len([
            people
            for people, list_ranges in available.items()
            for period in list_ranges
            if people in workers and period.start <= project_start < period.stop
        ]) == len(workers):
            # need to wait until all liste people are available
            project_start += 1

        max_skill = {}
        for worker in workers:
            available[worker].append(range(project_start, project_start+duration))
            for skill, score in people[worker].items():
                if skill not in max_skill or max_skill[skill] < score:
                    max_skill[skill] = score
        for i, role in enumerate(project["roles"]):
            role_name, requirement = role["name"], role["level"]
            people_name = workers[i]
            worker = people[people_name]
            worker_level = worker.get(role_name, 0)
            if worker_level < requirement - 1:
                return 0
                # too junior
            elif worker_level == requirement - 1:
                # need a mentor
                if max_skill[role_name] < requirement:
                    return 0
            else:
                people[people_name][role_name] += 1
        score = max(initial_award - max((project_start + duration) - best_before, 0), 0)
        total_score += score
    return total_score



# print(scoring(problem, solution))

def solver(problem):
    def update_max_skills(max_skills, people):
        for name, skills in people.items():
            for skill, level in skills.items():
                if max_skills.get(skill, 0) < level:
                    max_skills[skill] = level

    def can_do_project(max_skills, project):
        for role in project["roles"]:
            role_name = role["name"]
            requirement = role["level"]
            if max_skills.get(role_name, 0) < requirement:
                return False
        return True

    def update_people_skills(assignments, people):
        for skill, mate in assignments.items():
            people[mate][skill] += 1

    def get_most_junior(candidates):
        min_skill = float("inf")
        most_junior = None
        for candidate in candidates:
            if candidate[1] < min_skill:
                most_junior = candidate[0]
                min_skill = candidate[1]
        return most_junior

    def assigning(assignments, people, roles):
        """
        assign unique competences first
        then assign roles in desc order of requirements
        to the least experienced people that meet the requirements
        beware for mentoring
        Return True if all roles were assigned else False (impossible to address the project)
        """
        experienced = {}
        for mate, skills in people.items():
            for skill in skills:
                experienced.setdefault(skill, []).append(mate)
        unique_ressources = {
            skill: mates[0] for skill, mates in experienced.items() if len(mates) == 1
        }
        for role in roles:
            role_name = role["name"]
            requirement = role["level"]
            if expert := unique_ressources.get(role_name):
                assignments[role_name] = expert
        ordered_roles = sorted(
            filter(lambda role: role["name"] not in assignments.keys(), roles),
            key=lambda role: role["level"],
            reverse=True,
        )
        for role in ordered_roles:
            role_name = role["name"]
            requirement = role["level"]
            candidates = [
                (name, skills.get(role_name, 0))
                for name, skills in people.items()
                if name not in assignments.values()
                and skills.get(role_name, 0) >= requirement - 1
            ]
            if not any([skill >= requirement for _, skill in candidates]):
                # need to check if there is a mentor in the project
                if not any(
                    people[name].get(role_name, 0) >= requirement
                    for name in experienced[role_name]
                ):
                    return False  # no one meet the requirements, no mentoring possible
            candidate = get_most_junior(candidates)  # ESN mentality >:(
            assignments[role_name] = candidate
        return True

    people, projects = problem
    answer = []
    ordered_projects = sorted(projects.items(), key=lambda p: p[1]["best_before"])
    to_do = list(projects.keys())
    max_skills = {}
    previous = None
    skip = 0
    while to_do:
        update_max_skills(max_skills, people)
        remaining_projects = [
            (name, specs)
            for name, specs in ordered_projects
            if name in to_do and can_do_project(max_skills, specs)
        ]
        if not remaining_projects or skip >= len(remaining_projects):
            break
        project = remaining_projects[skip]
        if previous == project:
            break  # there is nothing to do!
        project_name = project[0]
        previous = project_name
        project = project[1]
        roles = []
        assignments = {}
        possible = assigning(assignments, people, project["roles"])
        if not possible:
            skip += 1  # let's try the same project later
            continue
        skip = max(skip -1, 0)
        update_people_skills(assignments, people)
        to_do.remove(project_name)
        for role in project["roles"]:
            roles.append(assignments[role["name"]])
        answer.append((project_name, roles))
    return answer

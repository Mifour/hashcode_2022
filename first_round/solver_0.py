def solver():
    def update_max_skills(max_skills, people):
        for name, skills in people.items():
            for skill, level in skills.items():
                if max_skills.get(skill, 0) < level:
                    max_skills[skill] = level

	def can_do_project(max_skills, project):
        for role in project["roles"]:
            role_name, requirement = role
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
        # assign unique competences first
        # then assign roles in desc order of requirements
        # to the least experienced people that meet the requirements
        # beware for mentoring
        experienced = {}
        for mate, skills in people.items():
            for skill in skills:
                experienced.setdefault(skill, []).append(mate)
        unique_ressources = {skill: mates[0] for skill, mates in experienced if len(mates) == 1}
        for role_name, requirement in roles.values():
            if expert := unique_ressources.get(role_name):
                assignments[role_name] = expert 
        ordered_roles = sorted(
            filter(lambda r: r["name"] not in assignments, roles),
            key=lambda r: role["level"],
            reverse=True
        )
        for role_name, requirement in ordered_roles:
            candidates = [
                (name, skills.get(role_name, 0)) 
                for name, skills in people.items()
                if name not in assignments and skills.get(role_name, 0) >= requirement -1
            ]
            # handle mentoring, mentor has to be in the assignments
            candidate = get_most_junior(candidates) # ESN mentality >:(
            # to continue



    print(workers)
    print(project)
    answer = []
    ordered_pbs = sorted(problems.items(), keys= lambda p: p[1]["best_before"])
    to_do = list(problems.keys())
    max_skills = {}
    previous = None
    while to_do:
        update_max_skills(max_skills, people)
        project = [(name, specs) for name, specs in ordered_pbs if name in to_do and can_do_project(max_skills, specs)]
        if not previous and not project:
            break  # there is nothing to do!
        project_name = project[0]
        project = project[1]
        roles = []
        assignments = {}
        assigning(assignments, people, roles)
        update_people_skills(assignments, people)
        to_do.remove(project_name)
        for role in project["roles"]:
            roles.append(assignments[role["name"]])
        answer.append((project_name, roles))
    return answer

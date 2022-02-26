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
        ... # magically assign roles to people
        update_people_skills(assignments, people)
        to_do.remove(project_name)
        answer.append((project_name, roles))
    return answer

def solver():
	project = projects[project_name]
    print(workers)
    print(project)
    sorted(problems, keys= lambda p: p["best_before"])

    max_skill = {}
    for worker in workers:
        for skill, score in people[worker].items():
            if skill not in max_skill or max_skill[skill] < score:
                max_skill[skill] = score
    team_skills = {}
    skill_prevalence = {}
    for worker in workers:
        team_skills[worker] = {}
        skills = people[worker].copy()
        for skill, score in skills.items():
            if skill in max_skill and max_skill[skill] > score:
                score += 1
                max_skill[skill] = score


            team_skills[worker][skill] = score
            skill_prevalence[skill] = skill_prevalence.get(skill, 0)+1
    print(skill_prevalence)

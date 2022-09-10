import argparse
import os

from parl_annotations.pyperplan_planner import PyperplanPlanner
from parl_annotations import generate_pyperplan_task


if __name__ =="__main__":
    planner = PyperplanPlanner(search_alg="astar2")

    cur_dir = os.path.dirname(__file__)
    domain_dir = os.path.abspath(os.path.join(cur_dir, "..") )+ "/annotations/strips"
    problem_dir = domain_dir + "/problems"
    domain_file = os.path.join(domain_dir, "maze_rooms.pddl")

    problem_files = [f for f in os.listdir(problem_dir) if f.endswith(".pddl")]

    for f in problem_files:
        problem_file = os.path.join(problem_dir, f)

        task = generate_pyperplan_task(domain_file, problem_file)
        plan_policy = planner.solve(task)

        with open(problem_file +".plan", "w") as fp:
            for ind, (s, o) in enumerate(plan_policy):
                print("state:{}".format(ind), file=fp)
                state_str = "\n".join([pred.strip() for pred in s])
                print(state_str, file=fp)
                print("\naction:{}".format(ind), file=fp)
                print(str(o), file=fp)


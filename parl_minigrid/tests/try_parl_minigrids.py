import argparse
import gym
import gym_minigrid
import pprint
pp = pprint.PrettyPrinter(indent=4)

from parl_minigrid.envs import MazeRoom_env_dict
from parl_minigrid.annotations.strips.annotated_task import MazeRoomsAnnotatedTask
from parl_minigrid.envs.maze_rooms import MazeRooms
from gym_minigrid.minigrid import MiniGridEnv

all_env_names = "\n".join([k for k in MazeRoom_env_dict.keys()])

parser = argparse.ArgumentParser()
parser.add_argument("--env", default="MazeRooms-2by2-v0", help=all_env_names)
parser.add_argument(
    "--seed", type=int, help="random seed to generate the environment with", default=42)
args = parser.parse_args()

env = gym.make(args.env)
env = gym_minigrid.wrappers.FullyObsWrapper(env)
env.seed(args.seed)

unwrapped_env = env
while not isinstance(unwrapped_env, MazeRooms) and not isinstance(unwrapped_env, MiniGridEnv):
    unwrapped_env = unwrapped_env.env
task = MazeRoomsAnnotatedTask(unwrapped_env)


obs = env.reset()
env.render(mode='human', highlight=False)
# pp.pprint("----" * 10)
# pp.pprint("obs:\n{}".format(obs))
pp.pprint("----" * 10)
pp.pprint("pl:\n{}".format(task.rl_obs_to_pl_state(None)))
pp.pprint("----" * 10)


while True:
    cmd = input("(0:left, 1:right, 2:fwd, 3:pick, 4:drop, 5:toggle, 6:reset, 7:break)$")
    if cmd == '7':
        print("break!")
        break
    if cmd in ['0', '1', '2', '3', '4', '5', '6']:
        obs, reward, done, info = env.step(int(cmd))
        env.render(mode='human', highlight=False)
        # pp.pprint("----"*10)
        # pp.pprint("obs:\n{}".format(obs))
        pp.pprint("----" * 10)
        pp.pprint("pl:\n{}".format(task.rl_obs_to_pl_state(None)))
        # pp.pprint("----" * 10)
        # pp.pprint("info:\n{}".format(info))
        pp.pprint("----" * 10)
        if done or cmd == '6':
            pp.pprint("----" * 10)
            pp.pprint("reset!")
            obs = env.reset()
            env.render(mode='human', highlight=False)
            # pp.pprint("----" * 10)
            # pp.pprint("obs:\n{}".format(obs))
            pp.pprint("----" * 10)
            pp.pprint("pl:\n{}".format(task.rl_obs_to_pl_state(None)))
            pp.pprint("----" * 10)



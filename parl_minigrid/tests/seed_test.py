"""
check how seeds are changing per input params
"""
import argparse
import gym
import gym_minigrid
import pprint
pp = pprint.PrettyPrinter(indent=4)

from parl_minigrid.envs import MazeRoom_env_dict
from parl_minigrid.annotations.strips.maze_rooms.annotated_task import MazeRoomsAnnotatedTask
from parl_minigrid.envs.maze_rooms import MazeRooms
from gym_minigrid.minigrid import MiniGridEnv

all_env_names = "\n".join([k for k in MazeRoom_env_dict.keys()])

parser = argparse.ArgumentParser()
parser.add_argument("--env", default="MazeRooms-2by2-TwoKeysSmall-v0", help=all_env_names)
args = parser.parse_args()

assert args.env in ["MazeRooms-8by8-DoorKey-v0", "MazeRooms-2by2-TwoKeysSmall-v0"], "debug envs"

# make an env for training
train_env = gym.make(args.env, train_mode=True, num_train_seeds=5, num_test_seeds=3)
train_env = gym_minigrid.wrappers.FullyObsWrapper(train_env)

# parl train task
unwrapped_train_env = train_env
while not isinstance(unwrapped_train_env, MazeRooms) and not isinstance(unwrapped_train_env, MiniGridEnv):
    unwrapped_train_env = unwrapped_train_env.env
train_task = MazeRoomsAnnotatedTask(unwrapped_train_env)

ind = 1
while True:
    obs = train_env.reset()
    train_env.render(mode='human', highlight=False)
    input("iter:{}".format(ind))
    ind += 1





import argparse
import gym
import gym_minigrid
import parl_minigrid

import time
import numpy as np
from gym_minigrid.wrappers import *
from gym_minigrid.window import Window


def redraw(img):
    if not args.agent_view:
        img = env.render('rgb_array', highlight=args.highlight, tile_size=args.tile_size)

    window.show_img(img)

def reset():
    # if args.seed != -1:
    #     env.seed(args.seed)

    obs = env.reset()

    if hasattr(env, 'mission'):
        print('Mission: %s' % env.mission)
        window.set_caption(env.mission)

    redraw(obs)

def step(action):
    obs, reward, done, info = env.step(action)
    print('step=%s, reward=%.2f' % (env.step_count, reward))

    if done:
        print('done!')
        reset()
    else:
        redraw(obs)

def key_handler(event):
    print('pressed', event.key)

    if event.key == 'escape':
        window.close()
        return

    if event.key == 'backspace':
        reset()
        return

    if event.key == 'left':
        step(env.actions.left)
        return
    if event.key == 'right':
        step(env.actions.right)
        return
    if event.key == 'up':
        step(env.actions.forward)
        return

    # Spacebar
    if event.key == ' ':
        step(env.actions.toggle)
        return
    if event.key == 'pageup':
        step(env.actions.pickup)
        return
    if event.key == 'pagedown':
        step(env.actions.drop)
        return

    if event.key == 'enter':
        step(env.actions.done)
        return


parser = argparse.ArgumentParser()

from parl_minigrid.envs import MazeRoom_env_dict
all_env_names = "\n".join([k for k in MazeRoom_env_dict.keys()])
parser.add_argument("--env", default="MazeRooms-8by8-DoorKey-v0", help=all_env_names)

parser.add_argument(
    "--seed",
    type=int,
    help="random seed to generate the environment with",
    default=-1
)

parser.add_argument(
    "--tile_size",
    type=int,
    help="size at which to render tiles",
    default=32
)

parser.add_argument(
    '--agent_view',
    default=False,
    help="draw the agent sees (partially observable view)",
    action='store_true'
)

parser.add_argument(
    '--highlight',
    default=False,
    help="don't show agent FOV",
    action='store_true'
)

parser.add_argument(
    "--standard",
    type=int,
    help="if it is wrapping gym_minigrid",
    default=1
)


args = parser.parse_args()
args.seed = np.random.randint(1000)

if args.standard == 1:
    env = gym.make(args.env)
else:
    parl_minigrid_kwargs = {
        "train_mode": True,
        "num_train_seeds": 5,
        "num_test_seeds": 3
    }
    env = gym.make(args.env, **parl_minigrid_kwargs)

env = gym_minigrid.wrappers.FullyObsWrapper(env)
window = Window('gym_minigrid - ' + args.env)
window.reg_key_handler(key_handler)
reset()

# Blocking event loop
window.show(block=True)

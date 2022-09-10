import argparse
import gym
import gym_minigrid
import pprint
pp = pprint.PrettyPrinter(indent=4)


parser = argparse.ArgumentParser()
parser.add_argument("--env", default="MiniGrid-DoorKey-8x8-v0")
parser.add_argument(
    "--seed", type=int, help="random seed to generate the environment with", default=42)
args = parser.parse_args()

env = gym.make(args.env)
env = gym_minigrid.wrappers.FullyObsWrapper(env)
env.seed(args.seed)

obs = env.reset()
env.render(mode='human', highlight=False)
# pp.pprint("----" * 10)
# pp.pprint("obs:\n{}".format(obs))


while True:
    cmd = input("(0:left, 1:right, 2:fwd, 3:pick, 4:drop, 5:toggle, 6:reset, 7:break)$")
    if cmd == '7':
        print("break!")
        break
    if cmd in ['0', '1', '2', '3', '4', '5', '6']:
        obs, reward, done, info = env.step(int(cmd))
        env.render(mode='human', highlight=False)
        pp.pprint("----"*10)
        pp.pprint("obs:\n{}".format(obs))
        pp.pprint("----" * 10)
        pp.pprint("info:\n{}".format(info))
        pp.pprint("----" * 10)
        if done or cmd == '6':
            pp.pprint("----" * 10)
            pp.pprint("reset!")
            obs = env.reset()
            env.render(mode='human', highlight=False)
            pp.pprint("----" * 10)
            pp.pprint("obs:\n{}".format(obs))
            pp.pprint("----" * 10)




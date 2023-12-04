from parl_minigrid.envs.maze_examples import *
from parl_minigrid.envs.maze_curriculum import *
from parl_minigrid.envs.standard_envs import *
from parl_minigrid.envs.maze_navigations import *
from parl_minigrid.envs.register import MazeRoom_env_dict, register_examples


register_examples(__name__, globals())

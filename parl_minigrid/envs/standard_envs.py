import random
from gym_minigrid.minigrid import *


class DoorKey(MiniGridEnv):
    """
    from gym_minigrid.envs import DoorKeyEnv
    wrap standard gym_minigrid env with new name and additional parameters
    This is MiniGridEnv, not RoomGrid
    """
    def __init__(self,
                 size=8,
                 max_steps=1024,
                 train_mode=True,
                 num_train_seeds=1000,
                 num_test_seeds=100,
                 seed=0
                 ):
        # RoomGrid
        self.room_size = size
        self.num_cols = 2
        self.num_rows = 1

        # give the same information as MazeRooms
        self.init_room = (0, 0)
        self.goal_room = (1, 0)
        self.init_cell = None
        self.goal_cell = None
        self.maze_layout = (((0, 0), (1, 0)),)      # two rooms are connected
        self.key_rooms = ((0, 0), )                # only at left
        self.key_colors = ('yellow', )
        self.locked_rooms_and_doors = None
        self.total_num_rooms = 2

        self.mission_type = "locked-room"
        self.one_ball_per_room = False
        self.one_key_per_room = False

        self.all_doors_open = False
        self.num_balls = 0
        self.num_keys = 1  # pass proper number; env won't check it for you
        self.num_locked_rooms = 1       # proper name would be locked_doors

        self.balls = []         # from ball get cur_pos, from pos get room by room_from_pos
        self.keys = []
        self.previous_pos = None

        self.wall_splitIdx = None
        self.doors = {Door('yellow', is_locked=True)}

        self.train_mode = train_mode
        self.num_train_seeds = num_train_seeds
        self.num_test_seeds = num_test_seeds
        self.default_seed = seed
        print("{} env".format(str(self.__class__)))
        print("train_mode:{}".format(train_mode))
        print("num_train_seeds:{}".format(num_train_seeds))
        print("num_test_seeds:{}".format(num_test_seeds))

        super().__init__(grid_size=size, max_steps=max_steps,
                         see_through_walls=True, seed=self.default_seed)

    def _get_train_test_seed(self, default_seed):
        if self.train_mode is None:
            random_seed = default_seed
        else:
            if self.train_mode:
                random_seed = random.choice(range(self.num_test_seeds, self.num_test_seeds + self.num_train_seeds))
            else:
                random_seed = random.choice(range(self.num_test_seeds))
        return random_seed

    def reset(self):
        random_seed = self._get_train_test_seed(self.default_seed)
        self.seed(random_seed)

        obs = super().reset()
        self.previous_pos = self.agent_pos
        return obs

    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Place a goal in the bottom-right corner
        self.put_obj(Goal(), width - 2, height - 2)
        self.goal_cell = (width-2, height-2)

        # Create a vertical splitting wall
        splitIdx = self._rand_int(2, width-2)
        self.grid.vert_wall(splitIdx, 0)
        self.wall_splitIdx = splitIdx

        # Place the agent at a random position and orientation
        # on the left side of the splitting wall
        self.init_cell = self.place_agent(size=(splitIdx, height))

        # Place a door in the wall
        doorIdx = self._rand_int(1, width-2)
        door = Door('yellow', is_locked=True)
        self.put_obj(door, splitIdx, doorIdx)
        self.doors = {door}

        # Place a yellow key on the left side
        self.keys = [Key('yellow')]
        self.place_obj(
            obj=self.keys[0],
            top=(0, 0),
            size=(splitIdx, height)
        )
        self.mission = "use the key to open the door and then get to the goal"

    def get_room_coord_from_pos(self, x, y):
        # needed for _at_agent and _at
        assert x >= 0
        assert y >= 0

        # coord is determined by x
        if x < self.wall_splitIdx:      # TODO < or <=
            return 0, 0
        else:
            return 1, 0


class MazeRooms_7by7_DoorKey(DoorKey):
    def __init__(self,
                 size=7,
                 max_steps=1024,
                 train_mode=True,
                 num_train_seeds=1000,
                 num_test_seeds=100,
                 seed=0
                 ):
        super().__init__(size=size,
                         max_steps=max_steps,
                         train_mode=train_mode,
                         num_train_seeds=num_train_seeds,
                         num_test_seeds=num_test_seeds,
                         seed=seed)


class MazeRooms_8by8_DoorKey(DoorKey):
    def __init__(self,
                 size=8,
                 max_steps=1024,
                 train_mode=True,
                 num_train_seeds=1000,
                 num_test_seeds=100,
                 seed=0
                 ):
        super().__init__(size=size,
                         max_steps=max_steps,
                         train_mode=train_mode,
                         num_train_seeds=num_train_seeds,
                         num_test_seeds=num_test_seeds,
                         seed=seed)


class MazeRooms_15by15_DoorKey(DoorKey):
    def __init__(self,
                 size=15,
                 max_steps=1024,
                 train_mode=True,
                 num_train_seeds=1000,
                 num_test_seeds=100,
                 seed=0
                 ):
        super().__init__(size=size,
                         max_steps=max_steps,
                         train_mode=train_mode,
                         num_train_seeds=num_train_seeds,
                         num_test_seeds=num_test_seeds,
                         seed=seed)
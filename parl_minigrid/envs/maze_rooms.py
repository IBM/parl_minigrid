import random

import gym
from gym_minigrid.roomgrid import RoomGrid
from gym_minigrid.minigrid import Goal
from gym_minigrid.minigrid import (
    COLORS, COLOR_NAMES, COLOR_TO_IDX, IDX_TO_COLOR,
    OBJECT_TO_IDX, IDX_TO_OBJECT,STATE_TO_IDX, DIR_TO_VEC,
)

DIR_TO_IDX = {'right': 0, 'down': 1, 'left': 2, 'up': 3}


class MazeRooms(RoomGrid):
    """
    room_size x room_size room
    num_rows x num_cols rooms
    balls at most 1 per room. all balls are blue
    keys at most 1 per room. all keys and doors are green

    ensure that the given maze_layout connects all rooms so key distribution is easy.
    """

    mission_types = ["simple", "closed-doors", "distracting-balls", "locked-room", "two-keys-locked"]
    ball_colors = ('blue',)
    door_colors = ('yellow',)       # they are also key colors
    obj_types = ('key', 'ball')
    env_name = ""
    gym_id = ""

    def __init__(
        self,
        # RoomGrid
        room_size=8,
        num_rows=3,
        num_cols=3,
        max_steps=1000,
        seed=0,
        agent_view_size=7,
        train_mode=None,
        num_train_seeds=1000,
        num_test_seeds=100,
        # MazeRooms
        mission_type="simple",
        init_room = (0, 0),
        goal_room = None,
        num_balls=0,     # randomly generate balls
        num_keys=0,      # keys are all same color
        num_locked_rooms=0,     # currently, only lock goal room
        maze_layout=None,       # pass maze layout
        key_rooms=None,          # pass the location of the key
        key_colors=None,
        locked_rooms_and_doors=None,       # [(room_i, room_j, 0, 'purple'), ]
    ):
        self.init_room = init_room
        if goal_room is None:
            self.goal_room = (num_cols - 1, num_rows - 1)
        else:
            self.goal_room= goal_room
        self.init_cell = None
        self.goal_cell = None
        self.maze_layout = maze_layout      # passing None makes 1 by 1 RoomGrid
        self.key_rooms = key_rooms
        self.key_colors = key_colors
        self.locked_rooms_and_doors = locked_rooms_and_doors
        self.total_num_rooms = num_rows * num_cols

        self.mission_type = mission_type
        self.one_ball_per_room = True
        self.one_key_per_room = True

        if self.mission_type == MazeRooms.mission_types[0]:
            self.mission = "navigate a simple maze to the goal location."       # this doesn't play any role here
            self.all_doors_open = True
            self.num_balls = 0
            self.num_keys = 0
            self.num_locked_rooms = 0
        elif self.mission_type == MazeRooms.mission_types[1]:
            self.mission = "open closed doors while navigate maze."
            self.all_doors_open = False
            self.num_balls = 0
            self.num_keys = 0
            self.num_locked_rooms = 0
        elif self.mission_type == MazeRooms.mission_types[2]:
            self.mission = "open closed doors and interact with balls while navigate maze."
            self.all_doors_open = False
            self.num_balls = num_balls
            self.num_keys = 0
            self.num_locked_rooms = 0
        elif self.mission_type == MazeRooms.mission_types[3]:
            self.mission = "open closed doors, interactive with balls, and unlock locked rooms while navigate maze."
            self.all_doors_open = False
            self.num_balls = num_balls
            self.num_keys = num_keys        # pass proper number; env won't check it for you
            self.num_locked_rooms = min(num_locked_rooms, self.total_num_rooms)
        elif self.mission_type == MazeRooms.mission_types[4]:
            self.mission = "two keys must be obtained in a sequence to secure the path to goal."
            self.all_doors_open = True
            self.num_balls = 0
            self.num_keys = 2
            self.num_locked_rooms = 2
        else:
            self.mission = "navigate a simple maze to the goal location."
            self.all_doors_open = True
            self.num_balls = 0
            self.num_keys = 0
            self.num_locked_rooms = 0
        if self.num_balls > self.total_num_rooms:  # currently all balls are of the same color
            self.one_ball_per_room = False
        if self.num_keys > self.total_num_rooms:  # currently all balls are of the same color
            self.one_key_per_room = False

        self.balls = []         # from ball get cur_pos, from pos get room by room_from_pos
        self.keys = []
        self.previous_pos = None

        self.train_mode = train_mode
        self.num_train_seeds = num_train_seeds
        self.num_test_seeds = num_test_seeds
        self.default_seed = seed
        print("num_train_seeds:{}".format(num_train_seeds))
        print("num_test_seeds:{}".format(num_test_seeds))

        # does this seed make reset behavior deterministic?
        random_seed = self._get_train_test_seed(self.default_seed)
        super().__init__(room_size, num_rows, num_cols, max_steps, random_seed, agent_view_size)

    def _get_train_test_seed(self, default_seed):
        if self.train_mode is None:
            random_seed = default_seed
        else:
            if self.train_mode:
                random_seed = random.choice(range(self.num_train_seeds))        # 0 ~ 99 training seed
            else:
                random_seed = random.choice(range(self.num_train_seeds, self.num_train_seeds + self.num_test_seeds))  # 1000~1019 evaluation seed
        return random_seed

    def reset(self):
        random_seed = self._get_train_test_seed(self.default_seed)
        self.seed(random_seed)

        obs = super().reset()
        self.previous_pos = self.agent_pos
        return obs

    def step(self, action):
        obs, reward, done, info = super().step(action)

        # update state information
        return obs, reward, done, info

    def _gen_grid(self, width, height):
        super()._gen_grid(width, height)    # _gen_grid called during reset()

        # should update annotation after reset
        self.gen_mission()

    def gen_mission(self):
        """
        customize Grid and RoomGrid configurations generated by RoomGrid._gen_grid()
        it only creates a grid and place the agent in the middle of the Grid.

        we should add doors (door position is determined in RoomGrid._gen_grid()), balls, and keys.
        """

        # place agent at the room (0,0)
        self.init_cell = self.place_agent(i=self.init_room[0], j=self.init_room[1], rand_dir=True)

        # add goal locations
        self.goal_cell = self.add_goal_tile(col=self.goal_room[0], row=self.goal_room[1])

        # add doors according to maze_layout
        if self.maze_layout:
            self.connect_rooms_from_layout()
            # by default doors were closed, open them all and randomly close doors
            self.open_all_doors()
            if not self.all_doors_open:
                self.close_random_doors()

        self.balls = []
        self.add_balls()
        self.doors = set()

        if self.num_locked_rooms > 0:
            # lock only goal room and distribute key other than the goal room
            self.keys = []
            self.add_keys()
            self.lock_rooms()

    def add_goal_tile(self, col, row):
        assert 0 <= col < self.num_cols
        assert 0 <= row < self.num_rows
        goal_room = self.room_grid[row][col]

        while True:
            goal_x, goal_y = self._rand_pos(
                goal_room.top[0] + 1,
                goal_room.top[0] + goal_room.size[0] - 1,
                goal_room.top[1] + 1,
                goal_room.top[1] + goal_room.size[1] - 1
            )
            if goal_x != self.agent_pos[0] and goal_y != self.agent_pos[1]:
                break
        self.put_obj(Goal(), goal_x, goal_y)        # green tile, reward will recognize this object
        return goal_x, goal_y

    def connect_rooms_from_layout(self):
        """
        layout is a list of pairs of room coordinates
            [ ((0,0), (0,1)), ((0,0), (1,0)), ... ]
        room at (0, 0) is connected to room on its right, (0, 1)
        """
        doors_added = set()
        for room1, room2 in self.maze_layout:
            if (room1, room2) in doors_added:
                continue

            room2_dir = self.relative_room_dir(room1, room2)

            if room2_dir is not None:
                self.add_door(room1[0], room1[1],
                              door_idx=DIR_TO_IDX[room2_dir],
                              color=self._rand_elem(MazeRooms.door_colors),
                              locked=False)
                doors_added.add((room1, room2))
                doors_added.add((room2, room1))
        self.doors = doors_added

    def close_random_doors(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                for door in self.room_grid[row][col].doors:
                    if door:
                        door.is_open = self._rand_bool()

    def add_balls(self):
        for i in range(self.num_balls):
            while True:
                room_i, room_j = self.sample_room()
                balls = self.get_typed_objects_in_room(room_i, room_j, 'ball')
                if not self.one_ball_per_room:
                    break
                if len(balls) == 0:
                    break
            ball, pos = self.add_object(room_i, room_j, kind='ball', color=self._rand_elem(MazeRooms.ball_colors))
            self.balls.append(ball)

    def lock_rooms(self):
        """
        if we don't know what rooms to lock, lock the goal room
        otherwise, use provided list of rooms to lock the doors in the room (room_i, room_j, door_ind, door_color)
            this will change the color  or the room
            TwoKeys_LockedRooms = ((1, 0, 1, 'yellow'), (0, 1, 3, 'purple'))
        """
        if self.locked_rooms_and_doors is None:
            room = self.room_grid[self.goal_room[1]][self.goal_room[0]]     # room (col, row); grid (row, col)
            for door in room.doors:
                if door:
                    door.is_open = False
                    door.is_locked = True
        else:
            for ind, locked_room in enumerate(self.locked_rooms_and_doors):
                room = self.room_grid[locked_room[1]][locked_room[0]]       # row, col
                door = room.doors[locked_room[2]]
                if door:
                    door.color = locked_room[3]
                    door.is_open = False
                    door.is_locked = True

    def add_keys(self):
        key_rooms, key_colors = [], []
        for i in range(self.num_keys):
            if self.key_rooms:
                room_i, room_j = self.key_rooms[i]
            else:
                while True:
                    room_i, room_j = self.sample_room()
                    if (room_i, room_j) == self.goal_room or (room_i, room_j) == self.init_room:
                        continue
                    if not self.one_key_per_room:
                        break
                    keys = self.get_typed_objects_in_room(room_i, room_j, 'key')
                    if len(keys) == 0:
                        break
            if self.key_colors:
                key_color = self.key_colors[i]
            else:
                key_color = self._rand_elem(MazeRooms.door_colors)
            key, pos = self.add_object(room_i, room_j, kind='key', color=key_color)
            key_rooms.append((room_i, room_j))
            key_colors.append(key_color)
            self.keys.append(key)       # from this list we can access all information!; get obj-get pos-get room, etc

        if self.key_rooms is None:
            self.key_rooms = key_rooms
        if self.key_colors is None:
            self.key_colors = key_colors

    def open_all_doors(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                room = self.get_room(i, j)
                for door in room.doors:
                    if door:
                        door.is_open = True

    def sample_room(self, i=None, j=None):
        room_i, room_j = i, j
        if room_i is None:
            room_i = self._rand_int(0, self.num_cols)
        if room_j is None:
            room_j = self._rand_int(0, self.num_rows)
        return room_i, room_j

    def get_typed_objects_in_room(self, i, j, obj_type):
        assert 0 <= i < self.num_cols
        assert 0 <= j < self.num_rows
        assert obj_type in MazeRooms.obj_types

        room = self.get_room(i, j)
        objs = [obj for obj in room.objs if obj_type == obj.type]
        return objs

    def reward_absolute_grid_distance(self):
        dist = self.grid_distance(self.agent_pos, self.goal_cell)
        dist = min(self.max_steps, dist)
        reward = - dist/self.max_steps
        return reward

    def reward_relative_grid_distance(self):
        if self.previous_pos is None:
            return 0
        dist_prev = self.grid_distance(self.previous_pos, self.goal_cell)
        dist_now = self.grid_distance(self.agent_pos, self.goal_cell)

        if dist_now < dist_prev:
            return 1.0
        else:
            return -1.0

    def reward_step_cost(self):
        return - 1.0/self.max_steps

    @staticmethod
    def grid_distance(pos_from, pos_to):
        a_x, a_y = pos_from       # (col, row)
        g_x, g_y = pos_to
        dist = abs(g_x - a_x) + abs(g_y - a_y)
        return dist

    def get_room_coord_from_pos(self, x, y):
        assert x >= 0
        assert y >= 0

        i = x // (self.room_size-1)
        j = y // (self.room_size-1)

        assert i < self.num_cols
        assert j < self.num_rows

        return i, j

    def relative_room_dir(self, room1, room2):
        r1col, r1row = room1
        r2col, r2row = room2
        room2_dir = None

        if r1col == r2col:
            if r1row - 1 == r2row:
                room2_dir = 'up'
            elif r1row + 1 == r2row:
                room2_dir = 'down'
        if r1row == r2row:
            if r1col - 1 == r2col:
                room2_dir = 'left'
            elif r1col + 1 == r2col:
                room2_dir = 'right'
        return room2_dir

from gym.envs.registration import register
from parl_minigrid.envs.maze_rooms import MazeRooms
from parl_minigrid.envs.register import register_examples

# (col, row) --  pairs are connected rooms
Default_2by2_layout = (
    ((0, 0), (1, 0)), ((1, 0), (1, 1)), ((0, 0), (0, 1))
)

Default_2by2_all_layout = (
    ((0, 0), (1, 0)), ((1, 0), (1, 1)), ((0, 0), (0, 1)), ((0, 1), (1, 1))
)

OneKey_Key_Rooms = ((1, 0), )

TwoKeys_Key_Rooms = ((1, 0), (0, 1))        # column, row in grid

TwoKeys_Key_Colors = ('purple', 'yellow')

TWoKeys_Key_Rooms_3by3 = ((1, 2), (1, 0))

# In room (1, 0) yellow door at down (1), etc
TwoKeys_LockedRooms = ((1, 0, 1, 'yellow'), (0, 1, 3, 'purple'))

Default_3by3_layout = (
    ((0, 0), (0, 1)), ((0, 1), (0, 2)),
    ((0, 0), (1, 0)), ((0, 2), (1, 2)),
    ((1, 0), (1, 1)), ((1, 1), (1, 2)),
    ((1, 0), (2, 0)), ((1, 1), (2, 1)),
    ((2, 1), (2, 2))
)

Default_4by4_layout = (
    ((0, 0), (0, 1)), ((0, 1), (0, 2)), ((0, 2), (0, 3)),
    ((0, 2), (1, 2)), ((0, 3), (1, 3)),
    ((1, 0), (1, 1)), ((1, 1), (1, 2)),
    ((1, 0), (2, 0)),
    ((2, 0), (2, 1)), ((2, 1), (2, 2)), ((2, 2), (2, 3)),
    ((2, 0), (3, 0)), ((2, 1), (3, 1)), ((2, 2), (3, 2)),
    ((3, 2), (3, 3)),
)

Default_3by3_layout2 = (
    ((0, 0), (1, 0)), ((1, 0), (2, 0)),
    ((0, 1), (1, 1)), ((1, 1), (2, 1)),
    ((0, 2), (1, 2)), ((1, 2), (2, 2)),
    ((0, 0), (0, 1)), ((0, 1), (0, 2)),
    ((1, 0), (1, 1)), ((1, 1), (1, 2)),
    ((2, 0), (2, 1)), ((2, 1), (2, 2))
)

OneKey_3by3_DoorLocked = ((1, 1, 3, 'yellow'), (1, 1, 2, 'yellow'),
                          (2, 2, 3, 'yellow'), (2, 2, 2, 'yellow'),
                          )

RoomSize8 = 8
RoomSize5 = 5

class MazeRooms_2by2_TwoKeys(MazeRooms):
    def __init__(self,
                 room_size=RoomSize8,
                 num_rows=2,
                 num_cols=2,
                 max_steps=1000,
                 num_keys=2,
                 train_mode=True,
                 num_train_seeds=1000,
                 num_test_seeds=100,
                 mission_type="two-keys-locked",
                 maze_layout=Default_2by2_layout,
                 key_rooms=TwoKeys_Key_Rooms,
                 key_colors=TwoKeys_Key_Colors,
                 locked_rooms_and_doors=TwoKeys_LockedRooms,
                 seed=0
                 ):
        super().__init__(room_size=room_size, num_rows=num_rows, num_cols=num_cols, max_steps=max_steps,
                         train_mode=train_mode, num_train_seeds=num_train_seeds,num_test_seeds=num_test_seeds,
                         num_keys=num_keys, mission_type=mission_type, maze_layout=maze_layout,
                         key_rooms=key_rooms, key_colors=key_colors, locked_rooms_and_doors=locked_rooms_and_doors,
                         seed=seed)


class MazeRooms_2by2_TwoKeysSmall(MazeRooms):
    def __init__(self,
                 room_size=RoomSize5,
                 num_rows=2,
                 num_cols=2,
                 max_steps=1000,
                 num_keys=2,
                 train_mode=True,
                 num_train_seeds=1000,
                 num_test_seeds=100,
                 mission_type="two-keys-locked",
                 maze_layout=Default_2by2_layout,
                 key_rooms=TwoKeys_Key_Rooms,
                 key_colors=TwoKeys_Key_Colors,
                 locked_rooms_and_doors=TwoKeys_LockedRooms,
                 seed=0
                 ):
        super().__init__(room_size=room_size, num_rows=num_rows, num_cols=num_cols, max_steps=max_steps,
                         train_mode=train_mode, num_train_seeds=num_train_seeds,num_test_seeds=num_test_seeds,
                         num_keys=num_keys, mission_type=mission_type, maze_layout=maze_layout,
                         key_rooms=key_rooms, key_colors=key_colors, locked_rooms_and_doors=locked_rooms_and_doors,
                         seed=seed)



class MazeRooms_2by2(MazeRooms):
    def __init__(self,
                 room_size=RoomSize8,
                 num_rows=2,
                 num_cols=2,
                 max_steps=1000,
                 train_mode=True,
                 num_train_seeds=1000,
                 num_test_seeds=100,
                 mission_type="simple",
                 maze_layout=Default_2by2_layout,
                 seed=0
                 ):
        super().__init__(room_size=room_size, num_rows=num_rows, num_cols=num_cols, max_steps=max_steps,
                         train_mode=train_mode, num_train_seeds=num_train_seeds, num_test_seeds=num_test_seeds,
                         mission_type=mission_type, maze_layout=maze_layout, seed=seed)


class MazeRooms_2by2_Doors(MazeRooms):
    def __init__(self,
                 room_size=RoomSize8,
                 num_rows=2,
                 num_cols=2,
                 max_steps=1000,
                 train_mode=True,
                 num_train_seeds=1000,
                 num_test_seeds=100,
                 mission_type="closed-doors",
                 maze_layout=Default_2by2_layout,
                 seed=0
                 ):
        super().__init__(room_size=room_size, num_rows=num_rows, num_cols=num_cols, max_steps=max_steps,
                         train_mode=train_mode, num_train_seeds=num_train_seeds, num_test_seeds=num_test_seeds,
                         mission_type=mission_type, maze_layout=maze_layout, seed=seed)


class MazeRooms_2by2_Balls(MazeRooms):
    def __init__(self,
                 room_size=RoomSize8,
                 num_rows=2,
                 num_cols=2,
                 max_steps=1000,
                 train_mode=True,
                 num_train_seeds=1000,
                 num_test_seeds=100,
                 mission_type="distracting-balls",
                 num_balls=4,
                 maze_layout=Default_2by2_layout,
                 seed=0
                 ):
        super().__init__(room_size=room_size, num_rows=num_rows, num_cols=num_cols, max_steps=max_steps,
                         train_mode=train_mode, num_train_seeds=num_train_seeds, num_test_seeds=num_test_seeds,
                         mission_type=mission_type, num_balls=num_balls, maze_layout=maze_layout, seed=seed)


class MazeRooms_2by2_Locked(MazeRooms):
    def __init__(self,
                 room_size=RoomSize8,
                 num_rows=2,
                 num_cols=2,
                 max_steps=1000,
                 train_mode=True,
                 num_train_seeds=1000,
                 num_test_seeds=100,
                 mission_type="locked-room",
                 num_balls=4,
                 num_keys=1,
                 key_colors=('yellow',),
                 key_rooms=OneKey_Key_Rooms,
                 num_locked_rooms=1,
                 maze_layout=Default_2by2_layout,
                 seed=0
                 ):
        super().__init__(room_size=room_size, num_rows=num_rows, num_cols=num_cols, max_steps=max_steps,
                         train_mode=train_mode, num_train_seeds=num_train_seeds, num_test_seeds=num_test_seeds,
                         mission_type=mission_type,
                         num_balls=num_balls, num_keys=num_keys, key_colors=key_colors, key_rooms=key_rooms,
                         num_locked_rooms=num_locked_rooms, maze_layout=maze_layout, seed=seed)


class MazeRooms_2by2_LockedSmall(MazeRooms):
    def __init__(self,
                 room_size=RoomSize5,
                 num_rows=2,
                 num_cols=2,
                 max_steps=1000,
                 train_mode=True,
                 num_train_seeds=1000,
                 num_test_seeds=100,
                 mission_type="locked-room",
                 num_balls=4,
                 num_keys=1,
                 key_colors=('yellow',),
                 key_rooms=OneKey_Key_Rooms,
                 num_locked_rooms=1,
                 maze_layout=Default_2by2_layout,
                 multiple_init_rooms=((0, 0), (0, 1)),
                 seed=0
                 ):
        super().__init__(room_size=room_size, num_rows=num_rows, num_cols=num_cols, max_steps=max_steps,
                         train_mode=train_mode, num_train_seeds=num_train_seeds, num_test_seeds=num_test_seeds,
                         mission_type=mission_type,
                         num_balls=num_balls, num_keys=num_keys, key_colors=key_colors, key_rooms=key_rooms,
                         num_locked_rooms=num_locked_rooms, maze_layout=maze_layout,
                         multiple_init_rooms=multiple_init_rooms, seed=seed)


class MazeRooms_3by3_LockedDoors(MazeRooms):
    def __init__(self,
                 room_size=5,
                 num_rows=3,
                 num_cols=3,
                 max_steps=1000,
                 train_mode=True,
                 num_train_seeds=1000,
                 num_test_seeds=100,
                 mission_type="locked-room",
                 num_balls=0,
                 num_keys=1,
                 key_colors=('yellow',),
                 key_rooms=((2, 1), ),
                 num_locked_rooms=2,
                 maze_layout=Default_3by3_layout2,
                 locked_rooms_and_doors=OneKey_3by3_DoorLocked,
                 seed=0
                 ):
        super().__init__(room_size=room_size, num_rows=num_rows, num_cols=num_cols, max_steps=max_steps,
                         train_mode=train_mode, num_train_seeds=num_train_seeds, num_test_seeds=num_test_seeds,
                         mission_type=mission_type,
                         num_balls=num_balls, num_keys=num_keys, key_colors=key_colors, key_rooms=key_rooms,
                         num_locked_rooms=num_locked_rooms, maze_layout=maze_layout,
                         locked_rooms_and_doors=locked_rooms_and_doors, seed=seed)


class MazeRooms_3by3(MazeRooms):
    def __init__(self,
                 room_size=RoomSize8,
                 num_rows=3,
                 num_cols=3,
                 max_steps=1000,
                 train_mode=True,
                 num_train_seeds=1000,
                 num_test_seeds=100,
                 mission_type="simple",
                 maze_layout=Default_3by3_layout,
                 seed=0
                 ):
        super().__init__(room_size=room_size, num_rows=num_rows, num_cols=num_cols, max_steps=max_steps,
                         train_mode=train_mode, num_train_seeds=num_train_seeds, num_test_seeds=num_test_seeds,
                         mission_type=mission_type, maze_layout=maze_layout, seed=seed)


class MazeRooms_3by3_Doors(MazeRooms):
    def __init__(self,
                 room_size=RoomSize8,
                 num_rows=3,
                 num_cols=3,
                 max_steps=1000,
                 train_mode=True,
                 num_train_seeds=1000,
                 num_test_seeds=100,
                 mission_type="closed-doors",
                 maze_layout=Default_3by3_layout,
                 seed=0
                 ):
        super().__init__(room_size=room_size, num_rows=num_rows, num_cols=num_cols, max_steps=max_steps,
                         train_mode=train_mode, num_train_seeds=num_train_seeds, num_test_seeds=num_test_seeds,
                         mission_type=mission_type, maze_layout=maze_layout, seed=seed)


class MazeRooms_3by3_Balls(MazeRooms):
    def __init__(self,
                 room_size=RoomSize8,
                 num_rows=3,
                 num_cols=3,
                 max_steps=1000,
                 train_mode=True,
                 num_train_seeds=1000,
                 num_test_seeds=100,
                 mission_type="distracting-balls",
                 num_balls=9,
                 maze_layout=Default_3by3_layout,
                 seed=0
                 ):
        super().__init__(room_size=room_size, num_rows=num_rows, num_cols=num_cols, max_steps=max_steps,
                         train_mode=train_mode, num_train_seeds=num_train_seeds, num_test_seeds=num_test_seeds,
                         mission_type=mission_type, num_balls=num_balls, maze_layout=maze_layout, seed=seed)


class MazeRooms_3by3_Locked(MazeRooms):
    def __init__(self,
                 room_size=RoomSize8,
                 num_rows=3,
                 num_cols=3,
                 max_steps=1000,
                 train_mode=True,
                 num_train_seeds=1000,
                 num_test_seeds=100,
                 mission_type="locked-room",
                 num_balls=9,
                 num_keys=2,
                 key_colors=('yellow', 'yellow'),
                 key_rooms=TWoKeys_Key_Rooms_3by3,
                 num_locked_rooms=1,
                 maze_layout=Default_3by3_layout,
                 seed=0
                 ):
        super().__init__(room_size=room_size, num_rows=num_rows, num_cols=num_cols, max_steps=max_steps,
                         train_mode=train_mode, num_train_seeds=num_train_seeds, num_test_seeds=num_test_seeds,
                         mission_type=mission_type,
                         num_balls=num_balls, num_keys=num_keys, key_colors=key_colors, key_rooms=key_rooms,
                         num_locked_rooms=num_locked_rooms, maze_layout=maze_layout, seed=seed)


class MazeRooms_4by4(MazeRooms):
    def __init__(self,
                 room_size=RoomSize8,
                 num_rows=4,
                 num_cols=4,
                 max_steps=1000,
                 train_mode=True,
                 num_train_seeds=1000,
                 num_test_seeds=100,
                 mission_type="simple",
                 maze_layout=Default_4by4_layout,
                 seed=0
                 ):
        super().__init__(room_size=room_size, num_rows=num_rows, num_cols=num_cols, max_steps=max_steps,
                         train_mode=train_mode, num_train_seeds=num_train_seeds, num_test_seeds=num_test_seeds,
                         mission_type=mission_type, maze_layout=maze_layout, seed=seed)


class MazeRooms_4by4_Doors(MazeRooms):
    def __init__(self,
                 room_size=RoomSize8,
                 num_rows=4,
                 num_cols=4,
                 max_steps=1000,
                 train_mode=True,
                 num_train_seeds=1000,
                 num_test_seeds=100,
                 mission_type="closed-doors",
                 maze_layout=Default_4by4_layout,
                 seed=0
                 ):
        super().__init__(room_size=room_size, num_rows=num_rows, num_cols=num_cols, max_steps=max_steps,
                         train_mode=train_mode, num_train_seeds=num_train_seeds, num_test_seeds=num_test_seeds,
                         mission_type=mission_type, maze_layout=maze_layout, seed=seed)


class MazeRooms_4by4_Balls(MazeRooms):
    def __init__(self,
                 room_size=RoomSize8,
                 num_rows=4,
                 num_cols=4,
                 max_steps=1000,
                 train_mode=True,
                 num_train_seeds=1000,
                 num_test_seeds=100,
                 mission_type="distracting-balls",
                 num_balls=16,
                 maze_layout=Default_4by4_layout,
                 seed=0
                 ):
        super().__init__(room_size=room_size, num_rows=num_rows, num_cols=num_cols, max_steps=max_steps,
                         train_mode=train_mode, num_train_seeds=num_train_seeds, num_test_seeds=num_test_seeds,
                         mission_type=mission_type, num_balls=num_balls, maze_layout=maze_layout,
                         seed=seed)


class MazeRooms_4by4_Locked(MazeRooms):
    def __init__(self,
                 room_size=RoomSize8,
                 num_rows=4,
                 num_cols=4,
                 max_steps=1000,
                 train_mode=True,
                 num_train_seeds=1000,
                 num_test_seeds=100,
                 mission_type="locked-room",
                 num_balls=16,
                 num_keys=4,
                 key_colors=('yellow', 'yellow', 'yellow', 'yellow'),
                 num_locked_rooms=1,
                 maze_layout=Default_4by4_layout,
                 seed=0
                 ):
        super().__init__(room_size=room_size, num_rows=num_rows, num_cols=num_cols, max_steps=max_steps,
                         train_mode=train_mode, num_train_seeds=num_train_seeds, num_test_seeds=num_test_seeds,
                         mission_type=mission_type,
                         num_balls=num_balls, num_keys=num_keys, key_colors=key_colors,
                         num_locked_rooms=num_locked_rooms, maze_layout=maze_layout, seed=seed)


# register_examples(__name__, globals())

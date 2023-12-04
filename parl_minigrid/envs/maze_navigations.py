from gym.envs.registration import register
from parl_minigrid.envs.maze_rooms import MazeRooms


# (col, row) --  pairs are connected rooms
Default_2by2_layout = (
    ((0, 0), (1, 0)), ((1, 0), (1, 1)), ((0, 0), (0, 1))
)

ThreeKeys_2by2_Key_Rooms = ((0,0), (1,0), (0,1))

ThreeKeys_2by2_Colors = ("yellow", "yellow", "purple")

# room (0, 0, Right is yellow), (0, 0, Down is yellow), (1, 0, Down is purple)
ThreeKeys_2by2_DoorLocked = ((0, 0, 0, "yellow"), (0, 0, 1, "yellow"), (1, 0, 1, "purple"))


# (col, row) --  pairs are connected rooms
ThreeKeys_layout = (
    ((0, 0), (1, 0)), ((1, 0), (2, 0)),
    ((0, 0), (0, 1)), ((1, 0), (1, 1)),
    ((2, 0), (2, 1)), ((0, 1), (1, 1)),
    ((1, 1), (2, 1)), ((1, 1), (1, 2)),
    ((1, 1), (1, 2)), ((0, 2), (1, 2)),
    ((1, 2), (2, 2))
)

ThreeKeys_Key_Rooms = ((0, 0), (2, 0), (0, 2))

# (col, row, door, color)
# Order is right, down, left, up
ThreeKeys_DoorLocked = (
    (0, 0, 1, 'yellow'),
    (2, 0, 1, 'green'),
    (1, 1, 0, 'green'),
    (1, 1, 1, 'yellow'),
    (1, 1, 2, 'yellow'),
    (2, 2, 2, 'blue'),
    (0, 2, 0, 'green')
)

RoomSize4 = 4       # 2 X 2; assigning balls may fail since this is too small room
RoomSize5 = 5       # 3 X 3;


class MazeRooms_3by3_NoKey(MazeRooms):
    def __init__(self,
                 room_size=RoomSize4,
                 num_rows=3,
                 num_cols=3,
                 max_steps=1000,
                 train_mode=True,
                 num_train_seeds=int(1e9),
                 num_test_seeds=100,
                 mission_type="distracting-balls",
                 num_balls=9,
                 num_keys=0,
                 key_colors=None,
                 key_rooms=None,
                 num_locked_rooms=0,
                 maze_layout=ThreeKeys_layout,
                 locked_rooms_and_doors=None,
                 multiple_init_rooms=((0,0), (1,0), (2,0)),
                 seed=0
                 ):
        super().__init__(room_size=room_size, num_rows=num_rows, num_cols=num_cols, max_steps=max_steps,
                         train_mode=train_mode, num_train_seeds=num_train_seeds, num_test_seeds=num_test_seeds,
                         mission_type=mission_type,
                         num_balls=num_balls, num_keys=num_keys, key_colors=key_colors, key_rooms=key_rooms,
                         num_locked_rooms=num_locked_rooms, maze_layout=maze_layout,
                         locked_rooms_and_doors=locked_rooms_and_doors,
                         multiple_init_rooms=multiple_init_rooms, seed=seed)


class MazeRooms_3by3_ThreeKeys(MazeRooms):
    def __init__(self,
                 room_size=RoomSize4,
                 num_rows=3,
                 num_cols=3,
                 max_steps=1000,
                 train_mode=True,
                 num_train_seeds=int(1e9),
                 num_test_seeds=100,
                 mission_type="locked-room",
                 num_balls=0,
                 num_keys=3,
                 key_colors=('yellow', 'green', 'blue'),
                 key_rooms=ThreeKeys_Key_Rooms,
                 num_locked_rooms=len(ThreeKeys_DoorLocked),
                 maze_layout=ThreeKeys_layout,
                 locked_rooms_and_doors=ThreeKeys_DoorLocked,
                 multiple_init_rooms=((0, 0), (1, 0), (2, 0)),
                 seed=0
                 ):
        super().__init__(room_size=room_size, num_rows=num_rows, num_cols=num_cols, max_steps=max_steps,
                         train_mode=train_mode, num_train_seeds=num_train_seeds, num_test_seeds=num_test_seeds,
                         mission_type=mission_type,
                         num_balls=num_balls, num_keys=num_keys, key_colors=key_colors, key_rooms=key_rooms,
                         num_locked_rooms=num_locked_rooms, maze_layout=maze_layout,
                         locked_rooms_and_doors=locked_rooms_and_doors,
                         multiple_init_rooms=multiple_init_rooms, seed=seed)


class MazeRooms_3by3_ThreeDisposableKeys(MazeRooms):
    def __init__(self,
                 room_size=RoomSize4,
                 num_rows=3,
                 num_cols=3,
                 max_steps=1000,
                 train_mode=True,
                 num_train_seeds=int(1e9),
                 num_test_seeds=100,
                 mission_type="locked-room",
                 num_balls=0,
                 num_keys=3,
                 key_colors=('yellow', 'green', 'blue'),
                 key_rooms=ThreeKeys_Key_Rooms,
                 key_states=(1, 1, 1),
                 num_locked_rooms=len(ThreeKeys_DoorLocked),
                 maze_layout=ThreeKeys_layout,
                 locked_rooms_and_doors=ThreeKeys_DoorLocked,
                 multiple_init_rooms=((0, 0), (1, 0), (2, 0)),
                 seed=0
                 ):
        super().__init__(room_size=room_size, num_rows=num_rows, num_cols=num_cols, max_steps=max_steps,
                         train_mode=train_mode, num_train_seeds=num_train_seeds, num_test_seeds=num_test_seeds,
                         mission_type=mission_type,
                         num_balls=num_balls,
                         num_keys=num_keys, key_colors=key_colors, key_rooms=key_rooms, key_states=key_states,
                         num_locked_rooms=num_locked_rooms, maze_layout=maze_layout,
                         locked_rooms_and_doors=locked_rooms_and_doors,
                         multiple_init_rooms=multiple_init_rooms, seed=seed)


class MazeRooms_3by3_ThreeKeysBalls(MazeRooms):
    def __init__(self,
                 room_size=RoomSize5,
                 num_rows=3,
                 num_cols=3,
                 max_steps=1000,
                 train_mode=True,
                 num_train_seeds=int(1e9),
                 num_test_seeds=100,
                 mission_type="locked-room",
                 num_balls=9,
                 num_keys=3,
                 key_colors=('yellow', 'green', 'blue'),
                 key_rooms=ThreeKeys_Key_Rooms,
                 num_locked_rooms=len(ThreeKeys_DoorLocked),
                 maze_layout=ThreeKeys_layout,
                 locked_rooms_and_doors=ThreeKeys_DoorLocked,
                 multiple_init_rooms=((0, 0), (1, 0), (2, 0)),
                 seed=0
                 ):
        super().__init__(room_size=room_size, num_rows=num_rows, num_cols=num_cols, max_steps=max_steps,
                         train_mode=train_mode, num_train_seeds=num_train_seeds, num_test_seeds=num_test_seeds,
                         mission_type=mission_type,
                         num_balls=num_balls, num_keys=num_keys, key_colors=key_colors, key_rooms=key_rooms,
                         num_locked_rooms=num_locked_rooms, maze_layout=maze_layout,
                         locked_rooms_and_doors=locked_rooms_and_doors,
                         multiple_init_rooms=multiple_init_rooms, seed=seed)


class MazeRooms_3by3_ThreeDisposableKeysBalls(MazeRooms):
    def __init__(self,
                 room_size=RoomSize5,
                 num_rows=3,
                 num_cols=3,
                 max_steps=1000,
                 train_mode=True,
                 num_train_seeds=int(1e9),
                 num_test_seeds=100,
                 mission_type="locked-room",
                 num_balls=9,
                 num_keys=3,
                 key_colors=('yellow', 'green', 'blue'),
                 key_rooms=ThreeKeys_Key_Rooms,
                 key_states=(1,1,1),
                 num_locked_rooms=len(ThreeKeys_DoorLocked),
                 maze_layout=ThreeKeys_layout,
                 locked_rooms_and_doors=ThreeKeys_DoorLocked,
                 multiple_init_rooms=((0, 0), (1, 0), (2, 0)),
                 seed=0
                 ):
        super().__init__(room_size=room_size, num_rows=num_rows, num_cols=num_cols, max_steps=max_steps,
                         train_mode=train_mode, num_train_seeds=num_train_seeds, num_test_seeds=num_test_seeds,
                         mission_type=mission_type,
                         num_balls=num_balls,
                         num_keys=num_keys, key_colors=key_colors, key_rooms=key_rooms, key_states=key_states,
                         num_locked_rooms=num_locked_rooms, maze_layout=maze_layout,
                         locked_rooms_and_doors=locked_rooms_and_doors,
                         multiple_init_rooms=multiple_init_rooms, seed=seed)


class MazeRooms_2by2_ThreeDisposableKeys(MazeRooms):
    def __init__(self,
                 room_size=RoomSize5,
                 num_rows=2,
                 num_cols=2,
                 max_steps=1000,
                 train_mode=True,
                 num_train_seeds=int(1e9),
                 num_test_seeds=100,
                 mission_type="locked-room",
                 num_balls=0,
                 num_keys=3,
                 key_colors=ThreeKeys_2by2_Colors,
                 key_rooms=ThreeKeys_2by2_Key_Rooms,
                 key_states=(1, 1, 1),
                 num_locked_rooms=len(ThreeKeys_2by2_DoorLocked),
                 maze_layout=Default_2by2_layout,
                 locked_rooms_and_doors=ThreeKeys_2by2_DoorLocked,
                 seed=0
                 ):
        super().__init__(room_size=room_size, num_rows=num_rows, num_cols=num_cols, max_steps=max_steps,
                         train_mode=train_mode, num_train_seeds=num_train_seeds, num_test_seeds=num_test_seeds,
                         mission_type=mission_type,
                         num_balls=num_balls,
                         num_keys=num_keys, key_colors=key_colors, key_rooms=key_rooms, key_states=key_states,
                         num_locked_rooms=num_locked_rooms, maze_layout=maze_layout,
                         locked_rooms_and_doors=locked_rooms_and_doors, seed=seed)


class MazeRooms_2by2_OneDisposableKey(MazeRooms):
    def __init__(self,
                 room_size=RoomSize5,
                 num_rows=2,
                 num_cols=2,
                 max_steps=1000,
                 train_mode=True,
                 num_train_seeds=int(1e9),
                 num_test_seeds=100,
                 mission_type="locked-room",
                 num_balls=0,
                 num_keys=1,
                 key_colors=("yellow", ),
                 key_rooms=((0, 0),),
                 key_states=(1, ),
                 num_locked_rooms=2,
                 maze_layout=Default_2by2_layout,
                 locked_rooms_and_doors=((0, 0, 0, "yellow"), (0, 0, 1, "yellow")),
                 seed=0
                 ):
        super().__init__(room_size=room_size, num_rows=num_rows, num_cols=num_cols, max_steps=max_steps,
                         train_mode=train_mode, num_train_seeds=num_train_seeds, num_test_seeds=num_test_seeds,
                         mission_type=mission_type,
                         num_balls=num_balls,
                         num_keys=num_keys, key_colors=key_colors, key_rooms=key_rooms, key_states=key_states,
                         num_locked_rooms=num_locked_rooms, maze_layout=maze_layout,
                         locked_rooms_and_doors=locked_rooms_and_doors, seed=seed)


class MazeRooms_2by2_TwoDisposableKeys(MazeRooms):
    def __init__(self,
                 room_size=RoomSize5,
                 num_rows=2,
                 num_cols=2,
                 max_steps=1000,
                 train_mode=True,
                 num_train_seeds=int(1e9),
                 num_test_seeds=100,
                 mission_type="locked-room",
                 num_balls=0,
                 num_keys=2,
                 key_colors=("yellow", "yellow"),
                 key_rooms=((0, 0), (1, 0)),
                 key_states=(1, 1),
                 num_locked_rooms=3,
                 maze_layout=Default_2by2_layout,
                 locked_rooms_and_doors=((0, 0, 0, "yellow"), (0, 0, 1, "yellow"), (1, 0, 1, "yellow")),
                 seed=0
                 ):
        super().__init__(room_size=room_size, num_rows=num_rows, num_cols=num_cols, max_steps=max_steps,
                         train_mode=train_mode, num_train_seeds=num_train_seeds, num_test_seeds=num_test_seeds,
                         mission_type=mission_type,
                         num_balls=num_balls,
                         num_keys=num_keys, key_colors=key_colors, key_rooms=key_rooms, key_states=key_states,
                         num_locked_rooms=num_locked_rooms, maze_layout=maze_layout,
                         locked_rooms_and_doors=locked_rooms_and_doors, seed=seed)

from parl_minigrid.envs.maze_examples import *


All_connected_2by2_layout = (
    ((0, 0), (1, 0)),
    ((1, 0), (1, 1)),
    #
    ((0, 0), (0, 1)),
    ((0, 1), (1, 1))
)


All_connected_3by3_layout = (
    ((0, 0), (1, 0)), ((1, 0), (2, 0)),
    ((0, 1), (1, 1)), ((1, 1), (2, 1)),
    ((0, 2), (1, 2)), ((1, 2), (2, 2)),
    #
    ((0, 0), (0, 1)), ((0, 1), (0, 2)),
    ((1, 0), (1, 1)), ((1, 1), (1, 2)),
    ((2, 0), (2, 1)), ((2, 1), (2, 2))
)

All_connected_4by4_layout = (
    ((0, 0), (1, 0)), ((1, 0), (2, 0)), ((2, 0), (3, 0)),
    ((0, 1), (1, 1)), ((1, 1), (2, 1)), ((2, 1), (3, 1)),
    ((0, 2), (1, 2)), ((1, 2), (2, 2)), ((2, 2), (3, 2)),
    ((0, 3), (1, 3)), ((1, 3), (2, 3)), ((2, 3), (3, 3)),
    #
    ((0, 0), (0, 1)), ((0, 1), (0, 2)), ((0, 2), (0, 3)),
    ((1, 0), (1, 1)), ((1, 1), (1, 2)), ((1, 2), (1, 3)),
    ((2, 0), (2, 1)), ((2, 1), (2, 2)), ((2, 2), (2, 3)),
    ((3, 0), (3, 1)), ((3, 1), (3, 2)), ((3, 2), (3, 3)),
)

reward_shaping_option = "absolute"      # reward_relative_grid_distance vs. reward_absolute_grid_distance


class MazeRooms_1by1_Curriculum(MazeRooms):
    def __init__(self,
                 room_size=RoomSize8,
                 num_rows=1,
                 num_cols=1,
                 max_steps=1000,
                 train_mode=True,
                 num_train_seeds=1000,
                 num_test_seeds=100,
                 num_balls=1,
                 mission_type="distracting-balls",
                 maze_layout=None,
                 key_rooms=None,
                 key_colors=None,
                 locked_rooms_and_doors=None,
                 reward_shaping=reward_shaping_option
                 ):
        super().__init__(room_size=room_size, num_rows=num_rows, num_cols=num_cols, max_steps=max_steps,
                         train_mode=train_mode, num_train_seeds=num_train_seeds, num_test_seeds=num_test_seeds,
                         num_balls= num_balls,
                         mission_type=mission_type, maze_layout=maze_layout,
                         key_rooms=key_rooms, key_colors=key_colors,
                         locked_rooms_and_doors=locked_rooms_and_doors)
        self.all_doors_open = True
        self.reward_fn = self.reward_step_cost
        # if reward_shaping == "relative":
        #     self.reward_fn = self.reward_relative_grid_distance
        # else:
        #     self.reward_fn = self.reward_absolute_grid_distance

    def step(self, action):
        obs, reward, done, info = super().step(action)
        if reward == 0:
            reward = self.reward_fn()
        else:
            reward = 1
        self.previous_pos = self.agent_pos  # update after computing reward
        return obs, reward, done, info


class MazeRooms_2by2_Curriculum(MazeRooms):
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
                 maze_layout=All_connected_2by2_layout,
                 key_rooms=None,
                 key_colors=None,
                 locked_rooms_and_doors=None,
                 reward_shaping=reward_shaping_option
                 ):
        super().__init__(room_size=room_size, num_rows=num_rows, num_cols=num_cols, max_steps=max_steps,
                         train_mode=train_mode, num_train_seeds=num_train_seeds, num_test_seeds=num_test_seeds,
                         num_balls=num_balls,
                         mission_type=mission_type, maze_layout=maze_layout,
                         key_rooms=key_rooms, key_colors=key_colors,
                         locked_rooms_and_doors=locked_rooms_and_doors)
        self.all_doors_open = True

        self.reward_fn = self.reward_step_cost
        # if reward_shaping == "relative":
        #     self.reward_fn = self.reward_relative_grid_distance
        # else:
        #     self.reward_fn = self.reward_absolute_grid_distance

    def step(self, action):
        obs, reward, done, info = super().step(action)
        if reward == 0:
            reward = self.reward_fn()
        else:
            reward = 1
        self.previous_pos = self.agent_pos      # update after computing reward
        return obs, reward, done, info


class MazeRooms_3by3_Curriculum(MazeRooms):
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
                 maze_layout=All_connected_3by3_layout,
                 key_rooms=None,
                 key_colors=None,
                 locked_rooms_and_doors=None,
                 reward_shaping=reward_shaping_option
                 ):
        super().__init__(room_size=room_size, num_rows=num_rows, num_cols=num_cols, max_steps=max_steps,
                         train_mode=train_mode, num_train_seeds=num_train_seeds, num_test_seeds=num_test_seeds,
                         num_balls=num_balls,
                         mission_type=mission_type, maze_layout=maze_layout,
                         key_rooms=key_rooms, key_colors=key_colors,
                         locked_rooms_and_doors=locked_rooms_and_doors)
        self.all_doors_open = True
        self.reward_fn = self.reward_step_cost
        # if reward_shaping == "relative":
        #     self.reward_fn = self.reward_relative_grid_distance
        # else:
        #     self.reward_fn = self.reward_absolute_grid_distance

    def step(self, action):
        obs, reward, done, info = super().step(action)
        if reward == 0:
            reward = self.reward_fn()
        self.previous_pos = self.agent_pos  # update after computing reward
        return obs, reward, done, info


class MazeRooms_4by4_Curriculum(MazeRooms):
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
                 maze_layout=All_connected_4by4_layout,
                 key_rooms=None,
                 key_colors=None,
                 locked_rooms_and_doors=None,
                 reward_shaping=reward_shaping_option
                 ):
        super().__init__(room_size=room_size, num_rows=num_rows, num_cols=num_cols, max_steps=max_steps,
                         train_mode=train_mode, num_train_seeds=num_train_seeds, num_test_seeds=num_test_seeds,
                         num_balls=num_balls,
                         mission_type=mission_type, maze_layout=maze_layout,
                         key_rooms=key_rooms, key_colors=key_colors,
                         locked_rooms_and_doors=locked_rooms_and_doors)
        self.all_doors_open = True
        self.reward_fn = self.reward_step_cost
        # if reward_shaping == "relative":
        #     self.reward_fn = self.reward_relative_grid_distance
        # else:
        #     self.reward_fn = self.reward_absolute_grid_distance

    def step(self, action):
        obs, reward, done, info = super().step(action)
        if reward == 0:
            reward = self.reward_fn()
        self.previous_pos = self.agent_pos  # update after computing reward
        return obs, reward, done, info


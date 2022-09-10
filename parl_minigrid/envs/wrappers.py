import gym
import numpy as np
from gym import spaces
import numpy as np
from gym_minigrid.minigrid import OBJECT_TO_IDX


class ImgObsTransposeWrapper(gym.core.ObservationWrapper):
    """
    Use the image as the only observation output, no language/mission.
    Convert shape from N x C x H x W to N x H x W x C
    """
    def __init__(self, env):
        super().__init__(env)
        # self.observation_space = env.observation_space.spaces['image']
        img_space = env.observation_space.spaces['image']
        self.observation_space = gym.spaces.Box(
            low=0,
            high=255,
            shape=(img_space.shape[2], img_space.shape[0], img_space.shape[1]),
            dtype='uint8'
        )

    def observation(self, obs):
        img = obs['image']
        return np.transpose(img, (2, 0, 1))


class FullyRGBImgObsWrapper(gym.core.ObservationWrapper):
    """
    Fully observable gridworld using pixel observations - assumes env is wrapped with FullyObsWrapper
    """
    def __init__(self, env, tile_size=8):
        super().__init__(env)

        self.tile_size = tile_size

        obs_shape = env.observation_space.spaces['image'].shape
        self.observation_space.spaces['image'] = spaces.Box(
            low=0,
            high=255,
            shape=(obs_shape[0] * tile_size, obs_shape[1] * tile_size, 3),
            dtype='uint8'
        )

    def observation(self, obs):
        env = self.unwrapped

        # Render the whole grid
        if self.egocentric:
            grid, _ = env.grid.decode(obs['image'])
            rgb_img = grid.render(
                self.tile_size,
                agent_pos=(obs['image'].shape[0] // 2, obs['image'].shape[1] - 1),
                agent_dir=3
            )
        else:
            rgb_img = env.render(
                mode='rgb_array',
                highlight=False,
                tile_size=self.tile_size
            )

        return {
            'mission': obs['mission'],
            'image': rgb_img
        }


class EpisodeTerminationWrapper(gym.core.Wrapper):
    def __init__(self, env):
        super().__init__(env)
        # the other way is call gym.make(max_episode_steps) and let it use TimeLimit
        # then wrapper will add _max_episode_steps
        self.step_count = 0

    def step(self, action):

        obs, reward, done, info = self.env.step(action)
        self.step_count += 1

        if done:
            info['is_success'] = True if reward > 0 else False
            info['TimeLimit.truncated'] = True if self.step_count >= self.max_steps else False

        return obs, reward, done, info

    def reset(self, **kwargs):
        self.step_count = 0
        return self.env.reset(**kwargs)

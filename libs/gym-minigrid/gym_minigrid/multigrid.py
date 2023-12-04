# TODO modify multigrid to be multigrid env?
# let's use strips gym instead to illustrate the situation

from minigrid import *


class Agent(WorldObj):
    def __init__(self, index=0, view_size=7):
        super(Agent, self).__init__('agent', IDX_TO_COLOR[index])
        self.pos = None
        self.dir = None
        self.index = index
        self.view_size = view_size
        self.carrying = None
        self.terminated = False
        self.started = True
        self.paused = False

    def encode(self):
        # TODO 3 tuple encoding to 6 tuple with carrying type, carrying color, current???
        # agent needs encoding???
        return (OBJECT_TO_IDX[self.type], COLOR_TO_IDX[self.color], self.dir)

    def render(self, img):
        c = COLORS[self.color]
        tri_fn = point_in_triangle(
            (0.12, 0.19),
            (0.87, 0.50),
            (0.12, 0.81),
        )
        # Rotate the agent based on its direction
        tri_fn = rotate_fn(tri_fn, cx=0.5, cy=0.5, theta=0.5 * math.pi * self.dir)
        fill_coords(img, tri_fn, c)

    @property
    def dir_vec(self):
        """
        Get the direction vector for the agent, pointing in the direction
        of forward movement.
        """

        assert self.dir >= 0 and self.dir < 4
        return DIR_TO_VEC[self.dir]

    @property
    def right_vec(self):
        """
        Get the vector pointing to the right of the agent.
        """

        dx, dy = self.dir_vec
        return np.array((-dy, dx))

    @property
    def front_pos(self):
        """
        Get the position of the cell that is right in front of the agent
        """

        return self.pos + self.dir_vec

    def get_view_coords(self, i, j):
        """
        Translate and rotate absolute grid coordinates (i, j) into the
        agent's partially observable view (sub-grid). Note that the resulting
        coordinates may be negative or outside of the agent's view size.
        """

        ax, ay = self.pos
        dx, dy = self.dir_vec
        rx, ry = self.right_vec

        # Compute the absolute coordinates of the top-left view corner
        sz = self.view_size
        hs = self.view_size // 2
        tx = ax + (dx * (sz - 1)) - (rx * hs)
        ty = ay + (dy * (sz - 1)) - (ry * hs)

        lx = i - tx
        ly = j - ty

        # Project the coordinates of the object relative to the top-left
        # corner onto the agent's own coordinate system
        vx = (rx * lx + ry * ly)
        vy = -(dx * lx + dy * ly)

        return vx, vy

    def get_view_exts(self):
        """
        Get the extents of the square set of tiles visible to the agent
        Note: the bottom extent indices are not included in the set
        """

        # Facing right
        if self.dir == 0:
            topX = self.pos[0]
            topY = self.pos[1] - self.view_size // 2
        # Facing down
        elif self.dir == 1:
            topX = self.pos[0] - self.view_size // 2
            topY = self.pos[1]
        # Facing left
        elif self.dir == 2:
            topX = self.pos[0] - self.view_size + 1
            topY = self.pos[1] - self.view_size // 2
        # Facing up
        elif self.dir == 3:
            topX = self.pos[0] - self.view_size // 2
            topY = self.pos[1] - self.view_size + 1
        else:
            assert False, "invalid agent direction"

        botX = topX + self.view_size
        botY = topY + self.view_size

        return (topX, topY, botX, botY)

    def relative_coords(self, x, y):
        """
        Check if a grid position belongs to the agent's field of view, and returns the corresponding coordinates
        """

        vx, vy = self.get_view_coords(x, y)

        if vx < 0 or vy < 0 or vx >= self.view_size or vy >= self.view_size:
            return None

        return vx, vy

    def in_view(self, x, y):
        """
        check if a grid position is visible to the agent
        """

        return self.relative_coords(x, y) is not None


class MultiGridEnv(gym.Env):
    """
    0 agent is primary need agent.pos
    the rest are treated as objects
    """

    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second' : 10
    }

    # Enumeration of possible actions
    class Actions(IntEnum):
        # Turn left, turn right, move forward
        left = 0
        right = 1
        forward = 2
        # Pick up an object
        pickup = 3
        # Drop an object
        drop = 4
        # Toggle/activate an object
        toggle = 5

    def __init__(
        self,
        grid_size=None,
        width=None,
        height=None,
        max_steps=100,
        see_through_walls=True,
        seed=1337,
        agent_view_size=None,
        agents=None
    ):
        self.agents = agents
        self.agent_pos = None
        self.agent_dir = None

        # Can't set both grid_size and width/height
        if grid_size:
            assert width == None and height == None
            width = grid_size
            height = grid_size

        # Action enumeration for this environment
        self.actions = MultiGridEnv.Actions
        self.max_actions_per_agent = 6

        # Actions are discrete integer values; only use 1 agent at 1 step
        self.action_space = spaces.Discrete(len(self.actions) * len(self.agents))

        # Number of cells (width and height) in the agent view
        # assert agent_view_size % 2 == 1
        # assert agent_view_size >= 3
        # self.agent_view_size = agent_view_size
        self.agent_view_size = grid_size

        # Observations are dictionaries containing an
        # encoding of the grid and a textual 'mission' string
        self.observation_space = spaces.Box(
            low=0,
            high=255,
            shape=(width, height, 3),       # TODO ecoding uses 3 tuple? Fully obs
            # shape=(agent_view_size, agent_view_size, 3),
            dtype='uint8'
        )
        self.observation_space = spaces.Dict({
            'image': self.observation_space
        })

        # Range of possible rewards
        self.reward_range = (0, 1)

        # Window to use for human rendering mode
        self.window = None

        # Environment configuration
        self.width = width
        self.height = height
        self.max_steps = max_steps
        self.see_through_walls = see_through_walls

        # Initialize the RNG
        self.seed(seed=seed)

        # Initialize the state
        self.reset()

    def reset(self):
        # Current position and direction of the agent
        self.agent_pos = None
        self.agent_dir = None

        # Generate a new random grid at the start of each episode
        # To keep the same grid for each episode, call env.seed() with
        # the same seed before calling env.reset()
        self._gen_grid(self.width, self.height)     # TODO this makes self.grid

        # These fields should be defined by _gen_grid
        for a in self.agents:
            assert a.pos is not None
            assert a.dir is not None

        # Item picked up, being carried, initially nothing
        for a in self.agents:
            a.carrying = None

        # Step count since episode start
        self.step_count = 0

        self.agent_pos = self.agents[0].pos
        self.agent_dir = self.agents[0].dir

        # TODO fix view for agent 0 and treat others as objects???
        # multi grid returns list of obs per agent
        # Return first observation
        obs = self.gen_obs()        # TODO check what is returned
        return obs

    def seed(self, seed=1337):
        # Seed the random number generator
        self.np_random, _ = seeding.np_random(seed)
        return [seed]

    # TODO has needs to check encoding of grid -- needed? and then.. agent pos
    # def hash(self, size=16):
    #     """Compute a hash that uniquely identifies the current state of the environment.
    #     :param size: Size of the hashing
    #     """
    #     sample_hash = hashlib.sha256()
    #
    #     # TODO agent encoding -- agent object goes into grid.encode??? or separate???
    #     to_encode = [self.grid.encode().tolist(), self.agent_pos, self.agent_dir]
    #     for item in to_encode:
    #         sample_hash.update(str(item).encode('utf8'))
    #
    #     return sample_hash.hexdigest()[:size]

    @property
    def steps_remaining(self):
        return self.max_steps - self.step_count

    # TODO str doesn't show agent ?
    def __str__(self):
        """
        Produce a pretty string of the environment's grid along with the agent.
        A grid cell is represented by 2-character string, the first one for
        the object and the second one for the color.
        """

        # Map of object types to short string
        OBJECT_TO_STR = {
            'wall'          : 'W',
            'floor'         : 'F',
            'door'          : 'D',
            'key'           : 'K',
            'ball'          : 'A',
            'box'           : 'B',
            'goal'          : 'G',
            'lava'          : 'V',
        }

        # Short string for opened door
        OPENDED_DOOR_IDS = '_'

        # Map agent's direction to short string
        AGENT_DIR_TO_STR = {
            0: '>',
            1: 'V',
            2: '<',
            3: '^'
        }

        str = ''

        for j in range(self.grid.height):

            for i in range(self.grid.width):

                for a in self.agents:
                    if i == a.pos[0] and j == a.pos[1]:
                        str += AGENT_DIR_TO_STR[a.agent_dir] + a.color[0].upper()
                        continue
                # TODO check grid O.w. inherit it as MultiGrid
                c = self.grid.get(i, j)

                if c == None:
                    str += '  '
                    continue

                if c.type == 'door':
                    if c.is_open:
                        str += '__'
                    elif c.is_locked:
                        str += 'L' + c.color[0].upper()
                    else:
                        str += 'D' + c.color[0].upper()
                    continue

                if c.type == 'key':
                    if not c.is_disposable:
                        str += 'K' + c.color[0].upper()
                    else:
                        if not c.is_used:
                            str += 'k' + c.color[0].upper()
                        else:
                            str += '-' + c.color[0].upper()

                str += OBJECT_TO_STR[c.type] + c.color[0].upper()

            if j < self.grid.height - 1:
                str += '\n'

        return str

    def _gen_grid(self, width, height):
        assert False, "_gen_grid needs to be implemented by each environment"

    def _reward(self):
        """
        Compute the reward to be given upon success
        """

        return 1 - 0.9 * (self.step_count / self.max_steps)

    def _rand_int(self, low, high):
        """
        Generate random integer in [low,high[
        """
        # return self.np_random.integers(low, high)
        return self.np_random.randint(low, high)

    def _rand_float(self, low, high):
        """
        Generate random float in [low,high[
        """

        return self.np_random.uniform(low, high)

    def _rand_bool(self):
        """
        Generate random boolean value
        """

        return (self.np_random.randint(0, 2) == 0)

    def _rand_elem(self, iterable):
        """
        Pick a random element in a list
        """

        lst = list(iterable)
        idx = self._rand_int(0, len(lst))
        return lst[idx]

    def _rand_subset(self, iterable, num_elems):
        """
        Sample a random subset of distinct elements of a list
        """

        lst = list(iterable)
        assert num_elems <= len(lst)

        out = []

        while len(out) < num_elems:
            elem = self._rand_elem(lst)
            lst.remove(elem)
            out.append(elem)

        return out

    def _rand_color(self):
        """
        Generate a random color name (string)
        """

        return self._rand_elem(COLOR_NAMES)

    def _rand_pos(self, xLow, xHigh, yLow, yHigh):
        """
        Generate a random (x,y) position tuple
        """

        return (
            self.np_random.randint(xLow, xHigh),
            self.np_random.randint(yLow, yHigh)
        )

    def place_obj(self,
        obj,
        top=None,
        size=None,
        reject_fn=None,
        max_tries=math.inf
    ):
        """
        Place an object at an empty position in the grid

        :param top: top-left position of the rectangle where to place
        :param size: size of the rectangle where to place
        :param reject_fn: function to filter out potential positions
        """

        if top is None:
            top = (0, 0)
        else:
            top = (max(top[0], 0), max(top[1], 0))

        if size is None:
            size = (self.grid.width, self.grid.height)

        num_tries = 0

        while True:
            # This is to handle with rare cases where rejection sampling
            # gets stuck in an infinite loop
            if num_tries > max_tries:
                raise RecursionError('rejection sampling failed in place_obj')

            num_tries += 1

            pos = np.array((
                self._rand_int(top[0], min(top[0] + size[0], self.grid.width)),
                self._rand_int(top[1], min(top[1] + size[1], self.grid.height))
            ))

            # Don't place the object on top of another object
            if self.grid.get(*pos) != None:
                continue

            # Don't place the object where the agent is
            if np.array_equal(pos, self.agent_pos):
                continue

            # Check if there is a filtering criterion
            if reject_fn and reject_fn(self, pos):
                continue

            break

        self.grid.set(*pos, obj)

        if obj is not None:
            obj.init_pos = pos
            obj.cur_pos = pos

        return pos

    def put_obj(self, obj, i, j):
        """
        Put an object at a specific position in the grid
        """
        self.grid.set(i, j, obj)
        obj.init_pos = (i, j)
        obj.cur_pos = (i, j)

    # def place_agent(
    #     self,
    #     top=None,
    #     size=None,
    #     rand_dir=True,
    #     max_tries=math.inf
    # ):
    #     """
    #     Set the agent's starting point at an empty position in the grid
    #     """
    #
    #     self.agent_pos = None
    #     pos = self.place_obj(None, top, size, max_tries=max_tries)
    #     self.agent_pos = pos
    #
    #     if rand_dir:
    #         self.agent_dir = self._rand_int(0, 4)
    #
    #     return pos

    # TODO place agent by using place_object; placing agent type on board cause trouble?
    # grid can encode agent type?
    def place_agent(
        self,
        agent,
        top=None,
        size=None,
        rand_dir=True,
        max_tries=math.inf
    ):
        """
        Set the agent's starting point at an empty position in the grid
        """

        agent.pos = None
        pos = self.place_obj(agent, top, size, max_tries=max_tries)
        agent.pos = pos
        agent.init_pos = pos

        if rand_dir:
            agent.dir = self._rand_int(0, 4)

        agent.init_dir = agent.dir

        return pos

    # def agent_sees(self, agent, x, y):
    #     """
    #     Check if a non-empty grid position is visible to the agent
    #     """
    #
    #     coordinates = agent.relative_coords(x, y)
    #     if coordinates is None:
    #         return False
    #     vx, vy = coordinates
    #
    #     obs = self.gen_obs()
    #     obs_grid, _ = Grid.decode(obs['image'])
    #     obs_cell = obs_grid.get(vx, vy)
    #     world_cell = self.grid.get(x, y)
    #
    #     return obs_cell is not None and obs_cell.type == world_cell.type

    # TODO this action has to be... associated with agent
    # TODO action space then extends to agent * action space
    # or extend action space with 1 more variable select agent
    def step(self, action):
        self.step_count += 1

        active_agent_ind = int(action) // self.max_actions_per_agent
        active_agent = self.agents[active_agent_ind]
        active_action = int(action) % self.max_actions_per_agent

        reward = 0
        done = False

        fwd_pos = active_agent.front_pos
        fwd_cell = self.grid.get(*fwd_pos)

        # Rotate left
        if active_action == self.actions.left:
            active_agent.dir -= 1
            if active_agent.dir < 0:
                active_agent.dir += 4

        # Rotate right
        elif active_action == self.actions.right:
            active_agent.dir = (active_agent.dir + 1) % 4

        # Move forward
        elif active_action == self.actions.forward:
            if fwd_cell == None or fwd_cell.can_overlap():
                self.grid.set(*fwd_pos, active_agent)
                self.grid.set(*active_agent.pos, None)
                active_agent.pos = fwd_pos
            if fwd_cell != None and fwd_cell.type == 'goal':
                done = True
                reward = self._reward()
            if fwd_cell != None and fwd_cell.type == 'lava':
                done = True

        # Pick up an object
        elif active_action == self.actions.pickup:
            if fwd_cell and fwd_cell.can_pickup():
                if active_agent.carrying is None:
                    active_agent.carrying = fwd_cell
                    active_agent.carrying.cur_pos = np.array([-1, -1])
                    self.grid.set(*fwd_pos, None)

        # Drop an object
        elif active_action == self.actions.drop:
            if not fwd_cell and active_agent.carrying:
                self.grid.set(*fwd_pos, active_agent.carrying)
                active_agent.carrying.cur_pos = fwd_pos
                active_agent.carrying = None

        # Toggle/activate an object
        elif active_action == self.actions.toggle:
            if fwd_cell:
                fwd_cell.toggle(self, fwd_pos)      # toggle may not work in some objects like door
        else:
            assert False, "unknown action"

        self.agent_pos = self.agents[0].pos
        self.agent_dir = self.agents[0].dir

        if self.step_count >= self.max_steps:
            done = True

        obs = self.gen_obs()

        return obs, reward, done, {}

    def gen_obs(self):
        """
        Generate the agent's view (partially observable, low-resolution encoding)
        """

        # Encode the fully observable view into a numpy array
        image = self.grid.encode()

        assert hasattr(self, 'mission'), "environments must define a textual mission string"

        # Observations are dictionaries containing:
        # - an image (partially observable view of the environment)
        # - the agent's direction/orientation (acting as a compass)
        # - a textual mission string (instructions for the agent)
        obs = {
            'image': image,
            'direction': self.agent_dir,
            'mission': self.mission
        }

        return obs

    def get_obs_render(self, obs, tile_size=TILE_PIXELS//2):
        """
        Render an agent observation for visualization
        """

        grid, vis_mask = Grid.decode(obs)

        # Render the whole grid
        img = grid.render(
            tile_size,
            agent_pos=(self.agent_view_size // 2, self.agent_view_size - 1),
            agent_dir=3,
            highlight_mask=vis_mask
        )

        return img

    def render(self, mode='human', close=False, highlight=True, tile_size=TILE_PIXELS):
        """
        Render the whole-grid human view
        """

        if close:
            if self.window:
                self.window.close()
            return

        if mode == 'human' and not self.window:
            import gym_minigrid.window
            self.window = gym_minigrid.window.Window('gym_minigrid')
            self.window.show(block=False)

        # Compute which cells are visible to the agent
        _, vis_mask = self.gen_obs_grid()

        # Compute the world coordinates of the bottom-left corner
        # of the agent's view area
        f_vec = self.agents[0].dir_vec
        r_vec = self.agents[0].right_vec
        top_left = self.agent_pos + f_vec * (self.agent_view_size-1) - r_vec * (self.agent_view_size // 2)

        # Mask of which cells to highlight
        highlight_mask = np.zeros(shape=(self.width, self.height), dtype=bool)

        # For each cell in the visibility mask
        for vis_j in range(0, self.agent_view_size):
            for vis_i in range(0, self.agent_view_size):
                # If this cell is not visible, don't highlight it
                if not vis_mask[vis_i, vis_j]:
                    continue

                # Compute the world coordinates of this cell
                abs_i, abs_j = top_left - (f_vec * vis_j) + (r_vec * vis_i)

                if abs_i < 0 or abs_i >= self.width:
                    continue
                if abs_j < 0 or abs_j >= self.height:
                    continue

                # Mark this cell to be highlighted
                highlight_mask[abs_i, abs_j] = True

        # Render the whole grid
        img = self.grid.render(
            tile_size,
            self.agent_pos,
            self.agent_dir,
            highlight_mask=highlight_mask if highlight else None
        )

        if mode == 'human':
            self.window.set_caption(self.mission)
            self.window.show_img(img)

        return img

    def close(self):
        if self.window:
            self.window.close()
        return
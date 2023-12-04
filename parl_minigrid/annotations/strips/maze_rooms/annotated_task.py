import os
from typing import FrozenSet, Text, Dict, Tuple, List
from gym_minigrid.minigrid import Key
from parl_minigrid.envs.standard_envs import DoorKey

from parl_annotations import (
    AnnotatedTask,
    generate_pyperplan_task,
    StripsOption,
    generate_strips_option_pddl
)
from parl_annotations.pyperplan_planner import PyperplanPlanner


class MazeRoomsAnnotatedTask(AnnotatedTask):
    def __init__(self, env):
        super(AnnotatedTask, self).__init__()
        self.env = env

        # strips domain and problem file
        self.domain_file = os.path.join(os.path.dirname(__file__), "maze_rooms.pddl")
        problem_dir = os.path.join(os.path.dirname(__file__), "problems")
        self.problem_file = os.path.join(problem_dir, self.env.env_name + ".pddl")
        generate_problem_file(self.env.unwrapped, self.problem_file)

        # FD translator detects unlock predicates as static but pyperplan cannot;
        # so don't use FD translator for reducing the state predicates to reachable facts
        self.planning_task = generate_pyperplan_task(self.domain_file, self.problem_file, False)
        self.planner = PyperplanPlanner("astar2")
        # [state -> action] could be prec/action. there are many non-relevant predicates in the state
        # if a state satisfy precondition of two actions, which action should be applied?
        # from optimal plan we consider full states but there must be a set prec < sufficient < state ensures it.
        # this is one type of generalization to applicability of actions or plans to multiple instances (or states);
        self.optimal_policy = self.planner.solve(self.planning_task)

        self.planning_facts: List[Text] = sorted(list(self.planning_task.facts))
        self.strips_options: List[StripsOption] = generate_strips_option_pddl(self.domain_file, self.problem_file)
        self.pl_state_map = None

    def rl_obs_to_pl_state(self, obs, *args, **kwargs):
        # TODO how to maintain planning states?
        # Given a env, we have 1 pddl instance that covers all resets by design
        # we could use vec env but all agent will have the same optimal plan given instance
        # vector of task could also be passed to agent for parallel sampling
        # task has access to env by self.env; so it can access to all internal information
        # planning states = frozen set

        # states == lower case
        # from a set of facts in planning_task
        # we should determine its truth value
        check_fact_value_fn = {
            "at-agent": self._at_agent,
            "at": self._at,
            "carry": self._carry,
            "empty-hand": self._empty_hand,
            # "keymatch": self._keymatch,
            # "link": self._link,
            "locked": self._locked,
            "unlocked": self._unlocked,
            # "connected_rooms": self._connected_rooms
        }

        self.pl_state_map = dict()
        for fact in self.planning_task.facts:
            fact_str = fact[1:-1].split()       # remove ( and )
            pred_name = fact_str[0]
            assert fact_str[0] in check_fact_value_fn
            self.pl_state_map[fact] = check_fact_value_fn[pred_name](fact_str)
        pl_state = frozenset(k for k in self.pl_state_map if self.pl_state_map[k])
        return pl_state

    def _at_agent(self, fact_str):
        # the right and lower walls belong to the next room
        # therefore r1 - [d] - r2, the location of the door d is in r2
        room_str = fact_str[-1]
        room_str = room_str.split("-")
        room_col, room_row = int(room_str[1]), int(room_str[2])
        pos = self.env.agent_pos
        col, row = self.env.get_room_coord_from_pos(*pos)
        return room_col == col and room_row == row

    def _at(self, fact_str):
        key_str, room_str = fact_str[1], fact_str[2]
        key_str = key_str.split("-")
        key_color, key_ind = key_str[1], int(key_str[2])
        room_str = room_str.split("-")
        room_col, room_row = int(room_str[1]), int(room_str[2])

        key_obj = self.env.keys[key_ind]
        key_pos = key_obj.cur_pos
        if key_pos[0] == -1 and key_pos[1] == -1:
            return False
        col, row = self.env.get_room_coord_from_pos(*key_pos)
        return room_col == col and room_row == row and key_color == key_obj.color

    def _carry(self, fact_str):
        if self.env.carrying is None:
            return False
        # determine whether agent is carrying a key
        # carry k-yellow-1
        if isinstance(self.env.carrying, Key):
            # currently, key is unique up to color
            key_str = fact_str[1]
            key_str = key_str.split("-")
            key_color = key_str[1]
            return self.env.carrying.color == key_color

    def _empty_hand(self, fact_str):
        """
        (empty-hand) should check if agent is carrying a key or not
        other objects like balls are invisible object so
        checking if self.env.carrying is not enough!
        """
        # if self.env.carrying is None:
        #     return True
        # else:
        #     return False
        if not isinstance(self.env.carrying, Key):
            return True
        else:
            return False

    def _locked(self, fact_str):
        # if there is only 1 door then we can read its state directly
        if len(self.env.doors) == 1:
            door_obj = next(iter(self.env.doors))
            return door_obj.is_locked
        else:
            door_str = fact_str[1]
            door_str = door_str.split("-")
            door_color, c1, r1, c2, r2 = door_str[1:]
            c1, r1, c2, r2 = int(c1), int(r1), int(c2), int(r2)
            r2_dir = self.env.relative_room_dir((c1, r1), (c2, r2))
            # R, D, L, U index
            room1 = self.env.get_room(c1, r1)
            if r2_dir:
                if r2_dir == "right":
                    ind = 0
                elif r2_dir == "down":
                    ind = 1
                elif r2_dir == "left":
                    ind = 2
                elif r2_dir == "up":
                    ind = 3
                door = room1.doors[ind]
                return door.color == door_color and door.is_locked

    def _unlocked(self, fact_str):
        if self._locked(fact_str) == True:
            return False
        elif self._locked(fact_str) == False:
            return True

    def _keymatch(self, fact_str):
        # static predicate is ignored; this is a restriction from grounded task
        NotImplemented

    def _link(self, fact_str):
        # static predicate is ignored
        NotImplemented

    def _connected_rooms(self, fact_str):
        # static predicate is ignored
        NotImplemented

    def set_pl_initial_state_from_obs(self, obs):
        state = self.rl_obs_to_pl_state(obs)
        self.planning_task.initial_state = state

    def set_pl_goal_from_obs(self, obs):
        state = self.rl_obs_to_pl_state(obs)
        self.planning_task.goals = state

    def get_pl_initial_state(self):
        return self.planning_task.initial_state

    def get_pl_goal(self):
        return self.planning_task.goals

    def dist_states(self, state1, state2, ignored):
        return len((state1 - ignored) ^ (state2 - ignored))


def generate_problem_file(env, problem_file):
    """
    we can generate a problem file only after reset()
    reset won't change pddl problem instance

    rooms are always N x N grid, where each room is (col, row) starting from 0
    env.room_grid is a list of lists of Room objects
    num_rows, num_cols
    """
    from gym_minigrid.minigrid import COLOR_NAMES

    DIR_TO_IDX = {'right': 0, 'down': 1, 'left': 2, 'up': 3}

    def get_room2_dir(r1, r2):
        r1col, r1row = r1
        r2col, r2row = r2
        r2_dir = None

        if r1col == r2col:
            if r1row - 1 == r2row:
                r2_dir = 'up'
            elif r1row + 1 == r2row:
                r2_dir = 'down'

        if r1row == r2row:
            if r1col - 1 == r2col:
                r2_dir = 'left'
            elif r1col + 1 == r2col:
                r2_dir = 'right'
        return r2_dir

    if os.path.exists(problem_file):
        print("{} already exists".format(problem_file))
        return

    PDDL_PROBLEM_INSTANCE = """;;; auto-generated problem instance in parl_minigrid
;;; captital letters for static predicates
;;; R-c-r - room at column c and row r in a room grid
;;; D-color-c1-r1-c2-r2 - door with color linking R-c1-r1 and R-c2-r2 
;;; K-color-i - key with color with numeric index i
;;; (CONNECTED-ROOMS R-0-0 R-0-1) connected room at (0,0) and room at (0,1)
;;; (LINK D-yellow-0-0-0-1 R-0-0 R-0-1) yellow door links rooms at (0,0) and (0,1)
;;; (unlocked D-yellow-0-0-0-1) door D-yellow-0-0-0-1 is unlocked
;;; (KEYMATCH K-yellow-0 D-yellow-0-0-0-1) key k-yellow-0 matches door D-yellow-0-0-0-1
;
;   
;   
(define (problem {PROBLEM_ID})
        (:domain MazeRooms)
        (:objects
            {ROOOM_OBJS}
            {KEY_OBJS}
            {DOOR_OBJS}
        )
        (:init
{CONNECTED_ROOMS_NONFLUENTS}
{LINK_NONFLUENTS}
{KEYMATCH_NONFLUENTS}
{AGENT_FLUENTS}
{KEYAT_FLUENTS}
{LOCK_FLUENTS}
{UNLOCK_FLUENTS}
{CARRY_FLUENTS}
        )
        (:goal 
            (and
{GOAL_FLUENTS}
            )
        )
)"""

    with open(problem_file, 'w') as fp:
        PROBLEM_ID = problem_file.split('/')[-1].replace(".pddl", "")

        room_ids = []
        room_coord_to_id = {}
        room_id_to_tuple = {}
        for col in range(env.num_cols):
            for row in range(env.num_rows):
                room_id = "R-{}-{}".format(col, row)
                room_ids.append(room_id)
                room_coord_to_id[(col, row)] = room_id
                room_id_to_tuple[room_id] = (col, row)
        ROOOM_OBJS = " ".join(room_ids)
        if room_ids:
            ROOOM_OBJS = ROOOM_OBJS + " -  room"

        key_ids = []
        key_id_to_env_ind = {}
        for ind, key_obj in enumerate(env.keys):
            key_id = "K-{}-{}".format(key_obj.color, ind)
            assert key_id not in key_ids
            key_ids.append(key_id)
            key_id_to_env_ind[key_id] = ind
        KEY_OBJS = " ".join(key_ids)
        if key_ids:
            KEY_OBJS = KEY_OBJS + " - key"

        door_ids = set()
        connected_rooms, door_link_rooms, key_match, locked, unlocked = set(), set(), set(), set(), set()
        door_id_to_obj = {}

        if env.maze_layout is not None:
            for room1, room2 in env.maze_layout:
                room1_id, room2_id = room_coord_to_id[room1], room_coord_to_id[room2]
                if "(CONNECTED-ROOMS {} {})".format(room1_id, room2_id) in connected_rooms:
                    continue
                connected_rooms.add("(CONNECTED-ROOMS {} {})".format(room1_id, room2_id))
                connected_rooms.add("(CONNECTED-ROOMS {} {})".format(room2_id, room1_id))

                room2_dir = get_room2_dir(room1, room2)
                room1_col, room1_row = room1

                if isinstance(env, DoorKey) and len(env.doors) == 1:
                    door_obj = next(iter(env.doors))
                else:
                    room1_obj = env.room_grid[room1_row][room1_col]
                    door_obj = room1_obj.doors[DIR_TO_IDX[room2_dir]]

                assert door_obj.color in COLOR_NAMES
                door_id = "D-{}-{}-{}-{}-{}".format(door_obj.color, room1[0], room1[1], room2[0], room2[1])
                door_ids.add(door_id)
                door_id_to_obj[door_id] = door_obj

                door_link_rooms.add("(LINK {} {} {})".format(door_id, room1_id, room2_id))
                door_link_rooms.add("(LINK {} {} {})".format(door_id, room2_id, room1_id))

                if door_obj.is_locked:
                    locked.add("(locked {})".format(door_id))
                else:
                    unlocked.add("(unlocked {})".format(door_id))

                for key_id in key_ids:
                    key_color = key_id.split("-")[1]
                    assert key_color in COLOR_NAMES
                    if door_obj.color == key_color:
                        key_match.add("(KEYMATCH {} {})".format(key_id, door_id))
        DOOR_OBJS = " ".join(door_ids)
        if door_ids:
            DOOR_OBJS = DOOR_OBJS + " - door"

        CONNECTED_ROOMS_NONFLUENTS = "\n".join(sorted(["\t\t\t" + el for el in connected_rooms]))
        LINK_NONFLUENTS = "\n".join(sorted(["\t\t\t" + el for el in door_link_rooms]))
        KEYMATCH_NONFLUENTS = "\n".join(sorted(["\t\t\t" + el for el in key_match]))
        AGENT_FLUENTS = "\n".join(["\t\t\t" + "(at-agent {})".format(room_coord_to_id[env.init_room])])
        LOCK_FLUENTS = "\n".join(sorted(["\t\t\t" + el for el in locked]))
        UNLOCK_FLUENTS = "\n".join(sorted(["\t\t\t" + el for el in unlocked]))
        CARRY_FLUENTS = "\n".join(["\t\t\t" + "(empty-hand)"])
        GOAL_FLUENTS = "\n".join(["\t\t\t" + "(at-agent {})".format(room_coord_to_id[env.goal_room])])

        key_at = set()
        for key_id in key_ids:
            key_obj = env.keys[key_id_to_env_ind[key_id]]
            x, y = key_obj.init_pos
            room_coord = x // (env.room_size-1), y//(env.room_size-1)       # col, row
            key_at.add("(at {} {})".format(key_id, room_coord_to_id[(room_coord)]))
        KEYAT_FLUENTS = "\n".join(sorted(["\t\t\t" + el for el in key_at]))

        problem_txt = PDDL_PROBLEM_INSTANCE.format(
            PROBLEM_ID=PROBLEM_ID,
            ROOOM_OBJS=ROOOM_OBJS,
            KEY_OBJS=KEY_OBJS,
            DOOR_OBJS=DOOR_OBJS,
            CONNECTED_ROOMS_NONFLUENTS=CONNECTED_ROOMS_NONFLUENTS,
            LINK_NONFLUENTS=LINK_NONFLUENTS,
            AGENT_FLUENTS=AGENT_FLUENTS,
            KEYMATCH_NONFLUENTS=KEYMATCH_NONFLUENTS,
            KEYAT_FLUENTS=KEYAT_FLUENTS,
            LOCK_FLUENTS=LOCK_FLUENTS,
            UNLOCK_FLUENTS=UNLOCK_FLUENTS,
            CARRY_FLUENTS=CARRY_FLUENTS,
            GOAL_FLUENTS=GOAL_FLUENTS
        )
        cleanup = ""
        for each_line in problem_txt.split("\n"):
            if each_line.strip():
                cleanup += each_line + "\n"
        fp.write(cleanup)
        fp.flush()


if __name__ == "__main__":
    import gym
    import parl_minigrid.envs
    from parl_minigrid.envs import MazeRoom_env_dict
    import pprint
    pp = pprint.PrettyPrinter(indent=2)

    env = gym.make("MazeRooms-2by2-TwoKeys-v0")
    env = env.env  # unwrap
    task = MazeRoomsAnnotatedTask(env)

    for k in MazeRoom_env_dict:
        env = gym.make(MazeRoom_env_dict[k].gym_id)
        env = env.env   # unwrap
        task = MazeRoomsAnnotatedTask(env)
        print(k)
        pp.pprint(task.optimal_policy)







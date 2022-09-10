from collections import OrderedDict
import gym


MazeRoom_env_dict = OrderedDict()


def register_examples(module_name, globals):
    global MazeRoom_env_dict
    for global_name in sorted(list(globals.keys())):
        if global_name.startswith('MazeRooms_'):
            env_names = global_name.split("_")
            env_name = "-".join(env_names)
            gym_id = "-".join([env_name, "v0"])
            if env_name not in MazeRoom_env_dict:
                gym.envs.registration.register(id = gym_id, entry_point = "{}:{}".format(module_name, global_name))
                MazeRoom_env_dict[env_name] = globals[global_name]
                MazeRoom_env_dict[env_name].gym_id = gym_id
                MazeRoom_env_dict[env_name].env_name = env_name
                MazeRooms_class = globals[global_name]
                MazeRooms_class.env_name = env_name
                MazeRooms_class.gym_id = gym_id

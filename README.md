# parl_minigrid
This repository offers `minigrid`` gym environments for planning annotation reinforcement learning experiments
* We provide custom minigrid environments with desired task structures that are paired with gym environments with planning tasks in STRIPS

## Related Repos
we use `parl_agent`, `parl_benchmark`, `parl_annotations` together.
* [parl_agents](https://github.com/IBM/parl_agents): Hierarchical RL agent codes 
* [parl_minigrid](https://github.com/IBM/parl_minigrid): Add-on to the minigrid environemtns
* adding different kinds of annotation to RL task, we extend `parl_annotations`
* adding new annotated RL environments, we addd new `parl_benchmark` such as `parl_minigrid`

# Install
* first create a conda environment for installing parl_annotations, parl_agents, parl_minigrid.
```
$ conda create -n parl python=3.7
``` 
* install packages as editable library
```
pip install -r requirements
pip install -e .
```

## Minigrid
* We use gym-minigrid version 1.0.2. 
* The current active version is not compatible with this code base anymore. 
* The version 1.2.0 may be compatible but there are some refactoring of the code that may breaks dependency in parl_minigrid. Therefore, we will add the version 1.0.2 in this repository.

### Custom Environments
* `parl_minigrid.envs.maze_rooms` defines `MazeRooms` class 
* `parl_minigrid.envs.maze_example` defines pre-generated gym environments
* For the custom environments, see `parl_minigrid.annotations.strips`


### minigrid world object encoding
* In minigrid, every object is a subclass of `WorldObj` that has 3-tuple encoding (type_ind, color_ind, 3-state).
* The 3-state is `{0: open, 1: closed, 2:locked}` that applies to doors.
  
### Disposable keys
* since a `Key` can be used multiple times, we added `KeyDisposable` and `DoorDisposable` to simulate the situation that an agent can use a key only once.
* the modification is simply adding two more types to the environment
  * add a `KeyDisposable` with its internal states `{0: unused, 1: used)`
  * `DoorDisposable` checks the `KeyDisposable` state before applying toggle
* this changes global variables in minigrid. Therefore, the current branch won't be compatible with gym-minigrid.


# Usage
there are sample scripts for running gym environments under `tests`

# Citations
* 2021 ICAPS PRL Workshop paper
```
@inproceedings{lee2021ai,
  title={AI Planning Annotation in Reinforcement Learning: Options and Beyond},
  author={Lee, Junkyu and Katz, Michael and Agravante, Don Joven and Liu, Miao and Klinger, Tim and Campbell, Murray and Sohrabi, Shirin and Tesauro, Gerald},
  booktitle={Planning and Reinforcement Learning PRL Workshop at ICAPS},
  year={2021}
}
```

* 2023 NEURIPS GenPlan Workshop paper
```
@inproceedings{lee2021ai,
  title={Hierarchical Reinforcement Learning with AI Planning Models},
  author={Lee, Junkyu and Katz, Michael and Agravante, Don Joven and Liu, Miao and Tasse, Geraud Nangue and Klinger, Tim and Sohrabi, Shirin},
  booktitle={Generalization in Planning GenPlan Workshop at NEURIPS},
  year={2023}
}
```

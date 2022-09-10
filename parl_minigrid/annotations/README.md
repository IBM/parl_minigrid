# annotations
* annotation classes are not gym environments!
* they all implement abstract class `AnnotatedTask` defined in `parl_annotations`


# strips option task
* define option specification from planning tasks using `StripsOption` class defined in `parl_annotations`
* PDDL domain and instance file
  * domain file is `maze_rooms.pddl` and instances files are stored under `problems`
  
* more on `StripsOption` objects
  * they boundd to the names in a grounded planning task
  * we handle literals using FD translator and Pyperplan parsers, installed with `parl_annotations`


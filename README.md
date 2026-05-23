# Bayesian Dice Engine

A stateful, parameter-driven stochastic game engine optimized for high-velocity simulation and real-time Bayesian probability modeling. 

The core game loop mechanics decouple state storage, physics engine parameters, and interface execution. This architecture allows the system to be run natively as a local CLI simulator, a mass parallel processing data collector, or a stateless backend API.

## Repository File Tree

``` text
bayesian-dice-engine/
├── src/
|   ├── game_engine/
|   │   ├── __init__.py
|   │   ├── depleting_dice.py
|   │   ├── game_state.py
|   │   ├── game.py
|   |   └── simulator.py
│   └── agent_algorithms/
|       ├── __init__.py
|       ├── agent.py
|       ├── expectimax_agent.py
|       ├── heuristic_agent.py
|       ├── random_agent.py
|       └── single_path_agent.py
├── tests/
|   ├── agent_test.py
|   ├── random_agent_test.py
|   ├── dice_test.py
|   └── game_test.py
├── .gitignore
├── LICENSE
└── README.md
```
## Architectural Paradigm

The codebase strictly adheres to clean Object-Oriented Programming (OOP) boundaries and separation of concerns. Python code is divided into `src` and `tests` directories. `src` contains all programs that will run in the actual application, whereas `tests` contains the unit tests for every object 


## Game Engine

The game engine is the model upon which all other simulations are built. The basic game mechanics are as follows.
1. 2 n-sided dice are rolled (standard: 6). The sides that they are rolled onto are removed, and cannot be rolled again
2. The sum of these two faces are reported to the user/agent/simulation
3. Repeat steps 1-2 r times (standard: 4). The dice state is continuous, meaning that all sides are permanently removed.

### 
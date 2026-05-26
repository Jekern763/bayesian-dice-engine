# Bayesian Dice Engine

A simulation environment designed to test and compare human cognitive biases against mathematically optimal strategies under shifting probabilities.

The core game loop strictly decouples the state storage, the physics engine, and the interface execution. This clean Object-Oriented Architecture allows the system to be run natively as a local CLI simulator, a mass parallel-processing data collector, or a stateless backend API.

## Abstract

The goal is to create a unique, simple dice game, with a new twist. Every time a dice is rolled, that face is removed for the remainder of the round. It also incorporates the properties of two dice, to create a weighted probability curve which is the highest at 7. The player of the game has incomplete knowledge of what dice sides have been rolled, they only know the sum of the two dice.

Using that simple game as a model, 6 different algorithms were built to play the game, either as human approximations or as a floor/ceiling control. These agents are not artificial intelligence, but rather simple algorithms that play the game in a set way

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
|   ├── expectimax_agent_test.py
|   ├── heuristic_agent_test.py
|   ├── single_path_agent_test.py
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

### Game Mechanic

The game engine is the model upon which all other simulations are built. The basic game mechanics are as follows.

1. 2 n-sided dice are rolled (standard: n=6). The sides that they are rolled onto are removed, and cannot be rolled again
2. The sum of these two faces are reported to the user/agent/simulation
3. Repeat steps 1-2 r times (standard: r=4). The dice state is continuous, meaning that all sides are permanently removed.

### Standardized Game Loop

1. User "peeks" 4 times (r=4)
2. User guesses what the 5th roll will be
3. Game mechanic runs for a final time, and calculates payout based on generalized the formula below

### Payout Formula

The payout formula is based on 2 different variables. The first is the distance of the users guess from the actual roll. The second is the distance of the users guess from the median roll, (usually 7). The first variable is the base determinator. The second is simply a multiplier that applies to both net gains and losses. The constant multipliers and shape of this function are still in developement

## Agent Algorithms

Each agent algorithm found under the `agent_algorithms` directory is meant to simulate either a floor, ceiling, or human playstyle.

+ `random_agent.py`: This agent simulates the worst possible way to play the game. It simply returns and random, unweighted value from the valid range 2-12

+ `heuristic_agent.py`: This is actually a collection of 3 agents.
    1. The first agent, reflection agent, finds the average of all revelaed peeks, then reflects them across the median possible roll (7). This simulates a human sub-consciously guessing in the opposite "direction" of the rolls it saw.
    2. The invariant agent uses the fact that if 2 dice are rolled 6 times each, in the manner that removes a side each time, the sum must be 42. Extapolated from that it uses `sum_remaining_rolls = 42 - sum_previous_rolls`. Because there are two rolls remaining, it divides the sum of remaining rolls by two to get the average next roll.
    3. The gamblers fallacy agent is based completely on the reflection agent. The only difference is that it will not guess a sum that it saw in previous peeks, instead preferring to go in a random direction until it finds a new sum to guess.

+ `single_path_agent`: This agent will calculate out one specific belief of what sides were rolled on each die. It will randomly choose a belief state, and continue down that path until it finds what it believes to be the two remaining sides on each die. At that point it will iterate through all 4 possible combinations, and all 12 valid guesses, and see what guess on average will give it the best results.

+ `expectimax_agent`: This agent recursively calculates all possible endings to the give scenario. It then iterates through all of them, similar to the `single_path_agent` to find which guess is best. This simulates that absolute ceiling, the best way to play the game.

## Unit Tests

Unit tests have been written for each individual game mechanic and agent algorithm. For the agent_algorithm tests some random methods were mocked, as well as the payout function. These tests insure proper game and algorithm logic for future iterations.

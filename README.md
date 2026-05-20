# Bayesian Dice Engine

A stateful, parameter-driven stochastic game engine optimized for high-velocity simulation and real-time Bayesian probability modeling. 

The core game loop mechanics decouple state storage, physics engine parameters, and interface execution. This architecture allows the system to be run natively as a local CLI simulator, a mass parallel processing data collector, or a stateless backend API.

## Architectural Paradigm

The codebase strictly adheres to clean Object-Oriented Programming (OOP) boundaries and separation of concerns. The system is split into three primary operational domains:

1. **Physics Engine (`depleting_dice.py`)**: Manages the dynamic probability mechanics of the physical objects. The dice are stateful, non-repeating memory samplers where the distribution shifts conditionally after every execution roll.
2. **State Container (`game_state.py`)**: A lightweight, mutable data container utilizing Python `dataclasses` and explicit typing via `enum` abstractions. It holds running tracking variables for the environment without embedded business logic.
3. **Execution Machine (`game.py`)**: A stateless transaction matrix class. It acts as the system's supervisor, accepting input operations, executing logic against the physical objects, mutating the state container, and returning structural updates.
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
│   └──
├── tests/
|   ├── dice_test.py
|   └── game_test.py
├── .gitignore
├── LICENSE
└── README.md
```

## Game Engine
The game engine is based on a simple dice game, using standard 6-sided die simulations. All game logic is found in `game.py`. The process is below
1. **Peeks** (`Game.peek()`): A pseudo random number is rolled on two dice. The faces rolled are removed from the respective die, and the sum is returned
2. **Guesses** (`Game.guess()`): The user/simulation/agent guesses a number. It is compared to an actual roll, and payout is calculated as below
3. **Payout** (`Game.calculate_payout()`): Payout is based on three factors. Distance from actual roll (scales linearly), distance from original median 7 (scales quadratically), and two specific conditions. If the guess is exactly two away from the roll, payout=0. If the guess is seven, payout=0.

Gameplay flow is as follows. 
1. The user peeks four times, with persisting state of depleting die.
2. The user guesses one time, still using the partially depleted die.
3. The payout is returned.
4. The simulation is reset.
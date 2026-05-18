# Bayesian Dice Engine

A stateful, parameter-driven stochastic game engine optimized for high-velocity simulation and real-time Bayesian probability modeling. 

The core game loop mechanics decouple state storage, physics engine parameters, and interface execution. This architecture allows the system to be run natively as a local CLI simulator, a mass parallel processing data collector, or a stateless backend API.

## Architectural Paradigm

The codebase strictly adheres to clean Object-Oriented Programming (OOP) boundaries and separation of concerns. The system is split into three primary operational domains:

1. **Physics Engine (`depleting_dice.py`)**: Manages the dynamic probability mechanics of the physical objects. The dice are stateful, non-repeating memory samplers where the distribution shifts conditionally after every execution roll.
2. **State Container (`game_state.py`)**: A lightweight, mutable data container utilizing Python `dataclasses` and explicit typing via `enum` abstractions. It holds running tracking variables for the environment without embedded business logic.
3. **Execution Machine (`game.py`)**: A stateless transaction matrix class. It acts as the system's supervisor, accepting input operations, executing logic against the physical objects, mutating the state container, and returning structural updates.
## Repository File Tree

'''text
bayesian-dice-engine/
│
├── src/
│   ├── __init__.py
│   ├── depleting_dice.py    # Non-repeating conditional probability dice logic
│   ├── game_state.py        # Typed dataclasses and structural Status enums
│   ├── game.py              # Main transaction matrix and payout algorithms
│   └── simulator.py         # Chronological logging simulation script
│
├── .gitignore               # Automated exclusions for virtual environments and caches
├── LICENSE                  # Open-source MIT License configuration
└── README.md                # Comprehensive documentation architecture
'''
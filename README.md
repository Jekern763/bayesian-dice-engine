# Bayesian Dice Engine

A stateful, parameter-driven stochastic game engine optimized for high-velocity simulation and real-time Bayesian probability modeling. 

The core game loop mechanics decouple state storage, physics engine parameters, and interface execution. This architecture allows the system to be run natively as a local CLI simulator, a mass parallel processing data collector, or a stateless backend API.

## Architectural Paradigm

The codebase strictly adheres to clean Object-Oriented Programming (OOP) boundaries and separation of concerns. The system is split into three primary operational domains:

1. **Physics Engine (`depleting_dice.py`)**: Manages the dynamic probability mechanics of the physical objects. The dice are stateful, non-repeating memory samplers where the distribution shifts conditionally after every execution roll.
2. **State Container (`game_state.py`)**: A lightweight, mutable data container utilizing Python `dataclasses` and explicit typing via `enum` abstractions. It holds running tracking variables for the environment without embedded business logic.
3. **Execution Machine (`game.py`)**: A stateless transaction matrix class. It acts as the system's supervisor, accepting input operations, executing logic against the physical objects, mutating the state container, and returning structural updates.

   [ Interface / Simulation Loop / API Layer ]
          │                           ▲
Invokes  │                           │ 4. Returns Updated
Action   ▼                           │    Data Class
┌─────────────────────────────────────┐
│            Game Engine              │
│            (game.py)                │
└────────┬───────────────────▲────────┘
│                   │
2. Alters  │                   │ 3. Mutates State
Memory  ▼                   │    Properties
┌──────────────────────┐  ┌───────┴──────────────┐
│     Physics Core     │  │   State Container    │
│ (depleting_dice.py)  │  │   (game_state.py)    │
└──────────────────────┘  └──────────────────────┘


## Repository File Tree

```text
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
⚙️ Core Component Implementation
1. State Container & Enumeration Boundary
The game environment phases are strictly defined via a finite universe of allowable statuses to prevent type-breaking errors.

Python
# src/game_state.py
from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple

class Status(Enum):
    INACTIVE = auto()
    WAITING = auto()
    ROLLING = auto()
    GUESSING = auto()
    FINISHED = auto()

@dataclass
class GameState:
    current_dice: Tuple
    status: Status = Status.INACTIVE
    net_score: float = 0.0
    current_round: int = 0
2. Transaction Engine
The execution core uses a return-driven model that accepts parameters and updates properties without relying on standard IO blocks.

Python
# src/game.py
from game_state import GameState
from depleting_dice import DepletingDice

class Game:
    def __init__(self, num_peeks: int = 4):
        self.die1 = DepletingDice()
        self.die2 = DepletingDice()
        self.state = GameState(current_dice=(self.die1, self.die2))
        self.num_peeks = num_peeks

    def reset(self):
        self.die1.reset()
        self.die2.reset()
        self.state = GameState(current_dice=(self.die1, self.die2))

    def peek(self) -> int:
        """Executes a physical roll to gather data. Does not alter financial yield."""
        roll = self.die1.roll() + self.die2.roll()
        return roll
    
    def calc_payout(self, guess: int, roll: int) -> float:
        # Complex probability matrix payout formulation goes here
        return 0.0 
    
    def guess(self, guess: int) -> float:
        """Executes a high-stakes roll and updates the network net score tracker."""
        roll = self.die1.roll() + self.die2.roll()
        payout = self.calc_payout(guess, roll)
        self.state.net_score += payout
        self.state.current_round += 1
        return payout
Execution & Simulation Workflows
Virtual Environment Initialization
Isolate dependencies locally by creating and activating a standard workspace interpreter sandbox inside the project root:

Bash
# Create the local environment folder
python3 -m venv .venv

# Activate the isolated context
source .venv/bin/activate
Generating Historical Records
Because the GameState is optimized for running adjustments, you should utilize standard deep-copy serialization (asdict) when writing tracking scripts or passing states into a historical array to prevent reference blending:

Python
# src/simulator.py
from dataclasses import asdict
from game import Game

game = Game()
simulation_history = []

# High-velocity loop iteration pattern
while game.state.current_round < 100000:
    # 1. Execute interaction
    payout = game.guess(guess=7)
    
    # 2. Extract and preserve an independent data snapshot
    snapshot = asdict(game.state)
    simulation_history.append(snapshot)
License
Distributed under the MIT License. See LICENSE for structural authorization details.
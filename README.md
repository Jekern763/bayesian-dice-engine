
# Gamblint

A simulation environment designed to test and compare human cognitive biases against mathematically optimal strategies under shifting probabilities.

The core game loop strictly decouples the state storage, the physics engine, and the interface execution. This clean Object-Oriented Architecture allows the system to be run natively as a local CLI simulator, a mass parallel-processing data collector, or a stateless backend API.

---

## Abstract

Bayesian Dice Engine is a probability-based game and simulation framework designed to study decision making under uncertainty. The project combines game design, probability theory, statistical analysis, and cloud engineering to compare human play against mathematically optimal strategies.

The goal is to create a unique, simple dice game, with a new twist. Every time a dice is rolled, that face is removed for the remainder of the round. It also incorporates the properties of two dice, to create a weighted probability curve which is the highest at 7. The player of the game has incomplete knowledge of what dice sides have been rolled, they only know the sum of the two dice.

Using that simple game as a model, 6 different algorithms were built to play the game, either as human approximations or as a floor/ceiling control. These agents are not artificial intelligence, but rather simple algorithms that play the game in a set way. The goal of these algorithms is to correlate human behavior patterns with certain play styles, and also to discover underlying behaviors of the game.

---

## Project Goals

While the project began as a simple game mechanic, and a quick python program, its overarching goals have since become much larger, and interdisciplinary. While the game itself represents unique mathematics and statistics, the value can go much deeper. The game will be used to conduct research at human behavior patterns. A full mathematical model will be made, and will be used to hopefully generate new sequences or series of other mathematic importance. Using that model, an expected value formula will be found, and then set to 0. Overall, the project combines multiple areas of study:

- Game design

- Computer Science

- Frontend Design

- Platform Engineering (AWS CDK architecture)

- Mathematics  (branching trees, stochastic and bayesian probability)

- Statistics (Human playstyle correlation)

- Business (Setting expected value)

- Behavioral Analysis (Research on human playstyles and patterns)

- Scientific Research (Writing a scientific paper, professionally summarizing results)

### Technologies Used

- Python

- TypeScript

- JavaScript

- Vanilla HTML

- CSS

- AWS CDK

- GitHub Actions

- pytest/pytest-mock

- pnpm

- uv

---

## System Architecture

  The system architecture can be divided into a couple of different sections.

``` mermaid
graph LR

Frontend --> API

API --> Game

Game --> GameState
Game --> Dice
Game --> Payout

Agents --> Game

RandomAgent --> Agents
HeuristicAgent --> Agents
SinglePathAgent --> Agents
ExpectimaxAgent --> Agents
```

### Game Engine

The game engine strictly adheres to Object Oriented Programing principles, along with separation of concerns. Within it is a python dataclass to represent the game state, a class to represent the unique dice system the game uses, and a class to represent the game as a whole. The game object can easily serialize and deserialize through methods from_json and to_json. The same is true of the game state. Therefore, a game can be started from any point in its timeline, and current game state can be kept completely in the backend game database. The game itself has no knowledge of any game loop, only its internal state and logic. It acts as the physics of the game, only setting bounds and returning outcomes. The game object takes 2 multipliers as arguments: riskiness multiplier and jackpot multiplier. It applies these with every payout calculation.

### Agent Algorithms

In total there are 6 algorithms. Each one represents a different human play style, or the absolute baseline/ceiling of possible play. It is important to note that these agents are **not** artificial intelligence, but just hand coded algorithms that play the game in different ways. The algorithms use a game object, but cannot peek inside it to get the internal state, and therefore cannot "cheat".

### Backend API

The backend API is completely serverless. It is built an AWS Lambda Python Function, but traffic is routed to it through API Gateway. It does not track the gameloop, but has two simple routes

1. api/start-game: This simply initializes a game, storing a mid-session record to DynamoDB. It takes a jackpot multiplier and a riskiness multiplier as data, and returns the peeks and session_id
2. api/guess: This takes a guess, calculates payout, and saves the result to the database. It takes the guess, and a game object (as json) to then randomly generate the actual roll based on the current game state

### Frontend

The frontend files are stored in an AWS S3 bucket, and served to the user via a cloudfront formation.  The frontend completely tracks the game loop itself, as well as keeping an user data stored in local storage. Because each round is independent any user data is completely cosmetic, such as net score or total rounds. The do however add a feeling of accomplishment for the player. After refactoring the scripts behind the frontend, there is now an object for storage, game state, and user interface.

### Infrastructure

``` mermaid
graph TB

subgraph Internet
    User([User])
    DNS["Route 53<br/>gamblint.jamesekern.com"]
end

subgraph AWS["AWS Infrastructure"]

    CF["CloudFront Distribution"]

    S3[(S3 Frontend File Storage)]

    API["API Gateway"]

    Lambda["Backend Lambda Function"]

    DB[(DynamoDB)]

    Logs[(CloudWatch Logs)]

    DNS --> CF

    CF -->|Frontend Files| S3
    CF -->|/api/*| API
    API --> Lambda
    Lambda <--> DB
    Lambda --> Logs

end

subgraph CICD["CI / CD"]

    GitHub["GitHub Actions"]

    CDK["AWS CDK"]

    Infra["Infrastructure Stack"]

    Frontend["Frontend Build"]

    GitHub --> CDK
    CDK --> Infra

    Infra --> CF
    Infra --> API
    Infra --> Lambda
    Infra --> DB
    Infra --> S3

    CDK --> Frontend
    Frontend --> S3

end

User --> DNS
```

---

## Development Practices

Throught development the project used the follwing practices:

- Object-Oriented Programming

- Type hints

- Formatting

- Dependency management

- Code reviews

- Documentation standards

- Version Control via Github

- Complete unit tests

---

## Continuous Integration & Deployment

A github actions workflow was setup (in `.github/workflows`) to preserve any current working structure. In the workflow triggers were either on a pull request or on a push to main

- on: pull request
    1. linting and formatting
    2. Dependency checking
    3. Unit tests
    4. CDK synthesis check
- on: push to main
    1. Automatic CDK deployment

---

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

The payout formula is based on 2 different variables. The first is the distance of the users guess from the actual roll. The second is the distance of the users guess from the median roll, (usually 7). The first variable is the base determinator. The second is simply a multiplier that applies to both net gains and losses. The constant multipliers and shape of this function are still in developement.

This payout function is not currently optimized to achieve EV=0. Instead, it is in the base format. The 2 independent variables were chosen to prevent the strategy of guessing median numbers. This strategy can still work, but risky guessing has been incentivised by giving it equal weight to accuracy. The risk variable, however, can never completely overcome the accuracy, because the accuracy is bounded by some number that gives the range for a positive payout.

The payout formula creates some interesting graphs. Let R equal the actual roll, and x be the guess, and y be the payout. All possible multipliers will be set to 1 to simply see the shape of the payout function.

[See the payout graph here](https://www.desmos.com/calculator/vscz5xr4ew)

There appear to be 3 zeroes. The first is always at 7, which is the guess at which payout is always 0 because the riskiness is 0. The other 2 are exactly 2 units away from the actual roll, because this is where accuracy "breaks even". If you are more than 2 away, you have a negative payout, less and you have a positive payout. While that is always true, sometimes the payout can be increasing although the guess is moving away from the roll. This is because the riskiness decreases enough to where accuracy starts to not matter, but the payout will never be positive if the guess is more than 2 away from the roll, although it can increase.

---

## Agent Algorithms

Each agent algorithm found under the `agent_algorithms` directory is meant to simulate either a floor, ceiling, or human playstyle.

1. Random Agent `random_agent.py`: This agent guesses a completely random number between 2 and 12, and acts as the floor
2. Heuristic Agents `heuristic_agent.py`: This collection of 3 agents represents a possible human playstyle, with decisions mostly made based on "vibes".
    1. Reflection Agent: This agent simply takes the mean of the observed sums and reflects it across 7 (the median roll)
    2. Invariant Agent: This agent uses the fact that the sum of any 6 sums in a given round must equal 42, and therefore the remaining sums must equal 42-(observed sums). It then takes the average remaining sum and guesses that number
    3. Gamblers Falllacy Agent: This agent is based on the reflection agent, but it will not guess a number that it previously saw in the peeks. It will go from its believed best guess in a random direction until it comes across a unique sum
3. Single Path Agent `single_path_agent.py`: This agent will go down a random path of possible face rolls for its given sums. It will choose a single belief state then go to the end of that path, and calculate the best guess based on expected value of that guess.
4. Expectimax Agent `expectimax_agent.py`: This agent will calculate every possible combination of faces give the observed sums, and based on that information maximize EV with its guess. This agent is the absolute ceiling for game play, although it only finds the best guess through brute force.

---

## Testing

Tests were written using pytest and pytest-mock.

Unit tests have been written for each individual game mechanic and agent algorithm. For the agent algorithm tests some random methods were mocked, as well as the payout function. These tests ensure proper game and algorithm logic for future iterations.

Tests were also written for the datase gateway, using moto to mock AWS DynamoDB.

The goal of the tests is to provide a complete framework of testing to find any flaws before deployment. All tests run during the CI/CD pipeline, and the merge cannot be completed until they all pass.

Tests have not been written for Javascript or Typescript yet, but they are coming soon.

---

## Current Project Status

### Completed

- Core game engine

- Handcrafted agent framework

- Backend API

- Frontend

- AWS Infrastructure as Code

- CI/CD pipeline

- Unit testing

### In Progress

Begin collecting game play data, while developing the next versions of the frontend.

---

## Roadmap

- Human gameplay data collection

- Large-scale agent simulations

- Statistical analysis

- Mathematical modeling of the game

- Expected value optimization

- Research paper

- Sequences/Series Research

- Publication

The long-term objective is to build a mathematically grounded framework for studying human probabilistic reasoning, compare heuristic strategies against optimal play, and publish the resulting mathematical and behavioral findings.

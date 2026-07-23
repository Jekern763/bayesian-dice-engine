from pathlib import Path

import pandas as pd

FIG_DIR = Path("/Users/jamesekern/pythonProjects/gamblint/research/figures")
AGENT_COMPARIONS_FIG_DIR = Path(
    "/Users/jamesekern/pythonProjects/gamblint/research/figures/agent_comparisons"
)

ALGORITHMS = [
    "random_agent",
    "reflection_agent",
    "invariant_agent",
    "gamblers_fallacy_agent",
    "single_path_agent",
    "expectimax_agent",
    "average_agent",
]

ALGORITHM_DFS = {
    algorithm: pd.read_csv(
        f"/Users/jamesekern/pythonProjects/gamblint/research/data/metric_tables/{algorithm}/{algorithm}.csv"
    )
    for algorithm in ALGORITHMS
}

ALGORITHM_DFS_BY_GUESS = {
    algorithm: pd.read_csv(
        f"/Users/jamesekern/pythonProjects/gamblint/research/data/metric_tables/{algorithm}/{algorithm}_by_guess.csv"
    )
    for algorithm in ALGORITHMS
}

ALGORITHM_DFS_BY_ROLL = {
    algorithm: pd.read_csv(
        f"/Users/jamesekern/pythonProjects/gamblint/research/data/metric_tables/{algorithm}/{algorithm}_by_roll.csv"
    )
    for algorithm in ALGORITHMS
}

ALGORITHM_DFS_BY_PEEKS = {
    algorithm: pd.read_csv(
        f"/Users/jamesekern/pythonProjects/gamblint/research/data/metric_tables/{algorithm}/{algorithm}_by_peeks.csv"
    )
    for algorithm in ALGORITHMS
}

CONSTANT_ALGORITHMS = [f"constant_agent_{i}" for i in range(2, 13)]

WIDTH = 900
HEIGHT = 600
FONT_SIZE = 18

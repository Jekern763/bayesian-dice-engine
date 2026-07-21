from pathlib import Path

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

CONSTANT_ALGORITHMS = [f"constant_agent_{i}" for i in range(2, 13)]

WIDTH = 900
HEIGHT = 600
FONT_SIZE = 18

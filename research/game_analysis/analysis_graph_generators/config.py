import sys
from pathlib import Path

import pandas as pd

game_analysis_dir = Path(
    "/Users/jamesekern/pythonProjects/gamblint/research/game_analysis"
).resolve()

if str(game_analysis_dir) not in sys.path:
    sys.path.append(str(game_analysis_dir))


def get_dataframes() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Returns history, config"""
    raw_data_path = (
        "/Users/jamesekern/pythonProjects/gamblint/research/data/game_analysis"
    )
    analysis_by_history = pd.read_pickle(f"{raw_data_path}/analysis_by_history.pkl")
    analysis_by_config = pd.read_pickle(f"{raw_data_path}/analysis_by_dice_config.pkl")
    return analysis_by_history, analysis_by_config

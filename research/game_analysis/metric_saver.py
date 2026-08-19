from analysis_by_dice_config import generate_metrics
from analysis_by_history import build_all_history_metrics

DICE_SIDES = range(1, 7)
DICE_NUMS = range(1, 3)

DATA_PATH = "../data/game_analysis"

by_history_df = build_all_history_metrics(DICE_NUMS, DICE_SIDES)
by_config_df = generate_metrics(by_history_df)

by_history_df.to_pickle(f"{DATA_PATH}/analysis_by_history.pkl")


by_config_df.to_pickle(f"{DATA_PATH}/analysis_by_dice_config.pkl")

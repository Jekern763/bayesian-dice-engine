import sys

import numpy as np
import pandas as pd
from sklearn.feature_selection import mutual_info_regression

sys.path.append("../game_analysis")


history_df = pd.read_pickle("../data/game_analysis/analysis_by_history.pkl")


def history_to_vector(row):
    history = row["history"]
    num_sides = row["num_sides"]

    return np.array(list(history) + [0] * (num_sides - len(history)))


def get_mutual_information(col_x: pd.Series, col_y: pd.Series) -> float:
    # This reshape(-1, 1) fixes the 2D error automatically
    X = col_x.values.reshape(-1, 1)
    y = col_y.values
    mi_score = mutual_info_regression(X, y)
    return float(mi_score[0])


history_df["history_vector"] = history_df.apply(history_to_vector, axis=1)
history_df["magnitude"] = history_df["history_vector"].apply(np.linalg.norm)


def do_corrs(vector_attr, history_attr):
    spearman_corr = history_df[[vector_attr, history_attr]].corr(method="spearman")

    print(spearman_corr.iloc[-1, 0])

    mutual_info = get_mutual_information(
        history_df[vector_attr], history_df[history_attr]
    )
    print(mutual_info)

    return spearman_corr, mutual_info


do_corrs("magnitude", "most_likely_roll")

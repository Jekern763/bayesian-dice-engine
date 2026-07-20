# This will find the specific metrics of an algorithms play that is provided as a list to the function.
"""
Metrics to find are
performance
    - Average payout
    - Median payout
    - Standard deviation of payout
    - Minimum payout
    - Maximum payout
accuracy
    - Exact hit rate (% of guesses equal to the roll)
    - Mean absolute error (MAE)
    - Mean squared error (MSE)
guess behavior
    - Guess frequency
    - Average deviation from 7
    - Distribution of deviation from 7
operation complexity
    - average decision operations
    - maximum decision operations

Things to condition on
- guess
- actual roll
"""

from statistics import mean, median, stdev

import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error


class AlgorithmMetrics:
    def __init__(self, path: str):
        self.df = pd.read_parquet(path)
        self.name = self.df["algorithm"].iloc[0]

    def __call__(self):
        raw = self.df.to_dict(orient="records")
        return raw

    def performance(self) -> dict:

        avg_payout = mean(self.df["payout"])
        median_payout = median(self.df["payout"])
        std_dev_payout = stdev(self.df["payout"])
        min_payout = min(self.df["payout"])
        max_payout = max(self.df["payout"])

        return {
            "average": avg_payout,
            "median": median_payout,
            "standard_deviation": std_dev_payout,
            "minimum": min_payout,
            "maximum": max_payout,
        }

    def accuracy(self):
        exact_hit_num = (self.df["guess"] == self.df["roll"]).sum()
        exact_hit_rate = exact_hit_num / len(self.df)

        mae = mean_absolute_error(self.df["roll"], self.df["guess"])

        mse = mean_squared_error(self.df["roll"], self.df["guess"])

        return {
            "exact_hit_rate": exact_hit_rate,
            "mean_absolute_error": mae,
            "mean_squared_error": mse,
        }

    def guess_behavior(self):
        guess_frequency = {}

        for i in range(2, 12):
            guess_frequency[str(i)] = (self.df["guess"] == i).sum

        avg_deviation = self.df["guess"].sub(7).avg().mean()

        return {"guess_frequency": guess_frequency, "average_deviation": avg_deviation}

    def operation_complexity(self):
        average_ops = mean(self.df["total_operations"])
        maximum_ops = max(self.df["total_operations"])

        return {"average_operations": average_ops, "maximum_operations": maximum_ops}

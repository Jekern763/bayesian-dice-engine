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

from dataclasses import dataclass
from statistics import mean, median, stdev

import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error


@dataclass
class PerformanceMetrics:
    average: float
    median: float
    standard_deviation: float
    minimum: int
    maximum: int


@dataclass
class AccuracyMetrics:
    exact_hit_rate: float
    mean_absolute_error: float
    mean_squared_error: float


@dataclass
class BehaviorMetrics:
    guess_frequency: dict
    average_deviation: float


@dataclass
class OperationMetrics:
    average: float
    maximum: int


class AlgorithmMetrics:
    def __init__(self, path: str):
        self.df = pd.read_parquet(path)
        self.name = self.df["algorithm"].iloc[0]
        self.as_dict = self.df.to_dict(orient="records")

    def performance(self) -> PerformanceMetrics:

        avg_payout = mean(self.df["payout"])
        median_payout = median(self.df["payout"])
        std_dev_payout = stdev(self.df["payout"])
        min_payout = min(self.df["payout"])
        max_payout = max(self.df["payout"])

        return PerformanceMetrics(
            average=avg_payout,
            median=median_payout,
            standard_deviation=std_dev_payout,
            minimum=min_payout,
            maximum=max_payout,
        )

    def accuracy(self) -> AccuracyMetrics:
        exact_hit_num = float((self.df["guess"] == self.df["roll"]).sum())
        exact_hit_rate = exact_hit_num / len(self.df)

        mae = mean_absolute_error(self.df["roll"], self.df["guess"])

        mse = mean_squared_error(self.df["roll"], self.df["guess"])

        return AccuracyMetrics(
            exact_hit_rate=exact_hit_rate,
            mean_absolute_error=mae,
            mean_squared_error=mse,
        )

    def guess_behavior(self) -> BehaviorMetrics:
        guess_frequency = {}

        for i in range(2, 13):
            guess_frequency[str(i)] = int((self.df["guess"] == i).sum() / len(self.df))

        avg_deviation = int((self.df["guess"] - 7).abs().mean())

        return BehaviorMetrics(
            guess_frequency=guess_frequency, average_deviation=avg_deviation
        )

    def operation_complexity(self) -> OperationMetrics:
        average_ops = mean(self.df["total_operations"])
        maximum_ops = max(self.df["total_operations"])

        return OperationMetrics(average=average_ops, maximum=maximum_ops)

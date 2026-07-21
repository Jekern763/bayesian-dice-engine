import csv
from pathlib import Path

from algorithm_metrics import AlgorithmMetrics

"""
The goal is to generate some readable CSVs first grouped simply by algorithm, and later by specific conditions on that algorithm.
The general patter of file storage will be:
data/metric_tables/[algorithm_name]
----- [algorithm_name].csv (contains the basic metrics)
----- [algorithm_name_by_guess].csv (contains the same metrics but for each guess)
----- [algorithm_name_by_roll].csv (contains the same metrics but for each roll)
"""

base_path = "/Users/jamesekern/pythonProjects/gamblint/research/data/"
metrics = AlgorithmMetrics(path=f"{base_path}raw/random_agent_10000.parquet")


def write_csv(path: str, data: list):
    if type(data) is dict:
        data = [data]
    file_path = Path(path)

    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)


## testing one out here, lets just get the basic metrics for the random algorithm

write_csv(
    path=f"{base_path}metric_tables/random_agent/random_agent.csv", data=metrics.all()
)

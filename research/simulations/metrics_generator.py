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
    if isinstance(data, dict):
        data = [data]

    if not data:
        return  # Prevent errors if the list is empty

    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Collect all unique keys from all dictionaries in the list
    all_keys = []
    for item in data:
        for key in item.keys():
            if key not in all_keys:
                all_keys.append(key)

    with open(file_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=all_keys)
        writer.writeheader()
        writer.writerows(data)


"""
TODO for each algoirthm: generate basic data. Group by guess. Group by roll.

"""

# First, loop through each file in raw.

for raw_data_path in Path(f"{base_path}raw").iterdir():
    file_name = raw_data_path.name
    algorithm_name = file_name.replace("10000.parquet", "")
    algorithm_name = (
        algorithm_name[:-1] if algorithm_name[-1] == "_" else algorithm_name
    )
    # generate csv of basic data
    algorithm_metrics = AlgorithmMetrics(raw_data_path)
    write_csv(
        f"{base_path}metric_tables/{algorithm_name}/{algorithm_name}.csv",
        algorithm_metrics.all(),
    )

    # generate grouped by roll
    write_csv(
        f"{base_path}metric_tables/{algorithm_name}/{algorithm_name}_by_roll.csv",
        algorithm_metrics.filtered("roll", algorithm_metrics.all),
    )

    # generate grouped by guess
    write_csv(
        f"{base_path}metric_tables/{algorithm_name}/{algorithm_name}_by_guess.csv",
        algorithm_metrics.filtered("guess", algorithm_metrics.all),
    )

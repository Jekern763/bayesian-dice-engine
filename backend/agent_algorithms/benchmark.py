import cProfile
import pstats
from pathlib import Path
from typing import List

import pandas as pd


def benchmark(
    agent, run_name: str, num_runs: int, save_results: bool = True
) -> List[dict]:
    results = []

    for i in range(num_runs):
        local_profiler = cProfile.Profile()
        local_profiler.enable()

        result = agent.simulate_round()
        result["algorithm"] = run_name
        result["run_num"] = i
        results.append(result)

        local_stats = pstats.Stats(local_profiler)
        total_calls_this_run = local_stats.total_calls

        result["total_operations"] = total_calls_this_run
        agent.reset_session()
    if save_results:
        df = pd.DataFrame(results)

        output = Path(
            f"~/pythonProjects/gamblint/research/data/raw/{run_name}_{num_runs}.parquet"
        )

        df.to_parquet(output)

    return results

from pathlib import Path
from typing import List

import pandas as pd


def benchmark(
    agent, run_name: str, num_runs: int, save_results: bool = True
) -> List[dict]:
    results = []

    for i in range(num_runs):
        result = agent.simulate_round()
        result["algorithm"] = run_name
        result["run_num"] = i
        results.append(result)

        agent.reset_session()
    if save_results:
        df = pd.DataFrame(results)

        output = Path(
            f"~/pythonProjects/gamblint/research/data/{run_name}_{num_runs}.parquet"
        )
        output.parent.mkdir(parents=True, exist_ok=True)

        df.to_parquet(output)

    return results

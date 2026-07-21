from dataclasses import asdict

from algorithm_metrics import AlgorithmMetrics

metrics = AlgorithmMetrics(
    path="~/pythonProjects/gamblint/research/data/reflection_agent_10000.parquet"
)

print(f"Performance: {asdict(metrics.performance())}\n")
print(f"Accuracy: {asdict(metrics.accuracy())}\n")
print(f"Behavior: {asdict(metrics.guess_behavior())}\n")
print(f"Operation Complexity: {asdict(metrics.operation_complexity())}\n")

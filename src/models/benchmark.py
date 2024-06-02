import json
from pathlib import Path

from models.benchmark_run_group import BenchmarkRunGroup
from src.models.benchmark_report import BenchmarkReport


class Benchmark:
    """
    Represent a benchmark output directory with general report, and run reports.
    """

    def __init__(self, report: BenchmarkReport, run_groups: list[BenchmarkRunGroup]):
        """
        Initialize the benchmark.
        :param report: Benchmark report
        :param run_groups: List of run groups
        """
        self.report = report
        self.run_groups = run_groups

    @property
    def name(self) -> str:
        """
        Get the name of the benchmark.
        """
        return self.report.name

    @classmethod
    def from_dir(cls, path: str) -> "Benchmark":
        """
        Load benchmark from a directory.
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"{path} does not exist.")

        if not path.is_dir():
            raise NotADirectoryError(f"{path} is not a directory.")

        report_path = path / "report.json"
        if not report_path.exists():
            raise FileNotFoundError(f"{report_path} does not exist.")

        with report_path.open() as f:
            report = BenchmarkReport(json.load(f), path.name)

        runs_path = path / "runs"
        if not runs_path.exists():
            raise FileNotFoundError(f"{runs_path} does not exist.")

        runs = []
        for generator_folder in runs_path.iterdir():
            if generator_folder.is_dir():
                runs.append(BenchmarkRunGroup.from_dir(generator_folder))

        return cls(report, runs)

    def __str__(self):
        return f"Benchmark({self.report.name})"



    @property
    def run_groups_sorted(self) -> list[BenchmarkRunGroup]:
        """
        Get the run groups sorted by algorithm and stop coverage.
        """
        run_groups = self.run_groups
        run_groups.sort(key=Benchmark._run_group_sort_lambda)
        return run_groups

    @staticmethod
    def _run_group_sort_lambda(run_group: BenchmarkRunGroup):
        return run_group.algorithm, run_group.stop_coverage

    @property
    def run_groups_grouped(self) -> dict[str, list[BenchmarkRunGroup]]:
        """
        Get the run groups grouped by algorithm.
        """
        run_groups = {}
        for run_group in self.run_groups_sorted:
            if run_group.algorithm not in run_groups:
                run_groups[run_group.algorithm] = []
            run_groups[run_group.algorithm].append(run_group)
        return run_groups

import json
from pathlib import Path

from src.models.benchmark_report import BenchmarkReport


class Benchmark:
    """
    Represent a benchmark output directory with general report, and run reports.
    """

    def __init__(self, report: BenchmarkReport, runs: dict):
        """
        Initialize the benchmark.
        :param report: Benchmark report
        :param runs: Runs dictionary
        """
        self.report = report
        self.runs = runs

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

        runs = {}
        # E.g. a folder "DirectedChinesePostmanPath(EdgeCoverage(80))" with run_0_path.json and run_0_report.json, etc... for run_1, run_2, etc...
        for generator_folder in runs_path.iterdir():
            if not generator_folder.is_dir():
                continue

            runs[generator_folder.name] = []
            for run_file in generator_folder.iterdir():
                if not run_file.is_file():
                    continue

                if run_file.name.endswith("_report.json"):
                    with run_file.open() as f:
                        # TODO: Create RunReport class
                        pass
                elif run_file.name.endswith("_path.json"):
                    with run_file.open() as f:
                        # TODO: Create RunPath class
                        pass

        return cls(report, runs)

    def __str__(self):
        return f"Benchmark({self.report.name})"

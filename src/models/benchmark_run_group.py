from pathlib import Path

from models.benchmark_run import BenchmarkRun
from utils.benchmark_name_parser import *


class BenchmarkRunGroup:
    """
    Group of runs for a specific algorithm and coverage criterion.
    """

    def __init__(self, algorithm: str, stop_condition: str, coverage: int, runs: list[BenchmarkRun]):
        """
        Create a benchmark run group

        :param algorithm: The algorithm
        :param stop_condition: The stop condition
        :param coverage: The coverage criterion
        :param runs: The runs
        """
        self.algorithm = algorithm
        self.stop_condition = stop_condition
        self.coverage = coverage
        self.runs = runs

    @classmethod
    def from_dir(cls, path: Path) -> 'BenchmarkRunGroup':
        """
        Load a benchmark run group from a directory

        :param path: The path to the directory
        :return: The benchmark run group
        """
        algorithm = parse_algorithm_from_name(path.name)
        stop_condition = parse_stop_condition_from_name(path.name)
        coverage = parse_coverage_from_stop_condition(stop_condition)

        runs = []

        for file in path.iterdir():
            if file.is_dir():
                continue

            if file.name.endswith('_path.json'):
                run_iteration = int(file.name.split('_')[1])

                path_file = file
                report_file = path / f"run_{run_iteration}_report.json"
                test_results_file = path / f"run_{run_iteration}_test_results.json"
                runs.append(BenchmarkRun.from_files(path_file, report_file, test_results_file))

        return cls(algorithm, stop_condition, coverage, runs)

from pathlib import Path

from models.benchmark_run import BenchmarkRun
from utils.benchmark_name_parser import *


class BenchmarkRunGroup:
    """
    Group of runs for a specific algorithm and coverage criterion.
    """

    def __init__(self, algorithm: str, stop_condition: str, stop_coverage: int, runs: list[BenchmarkRun]):
        """
        Create a benchmark run group

        :param algorithm: The algorithm
        :param stop_condition: The stop condition
        :param stop_coverage: The coverage criterion
        :param runs: The runs
        """
        self.algorithm = algorithm
        self.stop_condition = stop_condition
        self.stop_coverage = stop_coverage
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

    @property
    def successful_runs(self) -> list[BenchmarkRun]:
        """
        The successful runs in the group

        :return: The successful runs
        """
        return [run for run in self.runs if not run.is_failure]

    @property
    def failed_runs(self) -> list[BenchmarkRun]:
        """
        The failed runs in the group

        :return: The failed runs
        """
        return [run for run in self.runs if run.is_failure]

    @property
    def average_test_duration(self) -> float:
        """
        The average test duration of the runs in the group

        :return: The average test duration
        """
        return sum([run.test_duration for run in self.successful_runs]) / len(self.successful_runs)

    @property
    def average_driver_time_spent_waiting(self) -> float:
        """
        The average driver time spent waiting of the runs in the group

        :return: The average driver time spent waiting
        """
        return sum([run.driver_time_spent_waiting for run in self.successful_runs]) / len(self.successful_runs)

    @property
    def average_vertex_coverage(self) -> float:
        """
        The average vertex coverage of the runs in the group

        :return: The average vertex coverage
        """
        return sum([run.vertex_coverage for run in self.successful_runs]) / len(self.successful_runs)

    @property
    def average_edge_coverage(self) -> float:
        """
        The average edge coverage of the runs in the group

        :return: The average edge coverage
        """
        return sum([run.edge_coverage for run in self.successful_runs]) / len(self.successful_runs)

    @property
    def minimum_test_duration(self) -> float:
        """
        The minimum test duration of the runs in the group

        :return: The minimum test duration
        """
        return min([run.test_duration for run in self.successful_runs])

    @property
    def maximum_test_duration(self) -> float:
        """
        The maximum test duration of the runs in the group

        :return: The maximum test duration
        """
        return max([run.test_duration for run in self.successful_runs])

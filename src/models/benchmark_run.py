import json
from pathlib import Path


class BenchmarkRun:
    """
    A single run of a benchmark.
    """

    def __init__(self, path: dict, report: dict, test_results: dict):
        """
        Create a benchmark run

        :param path: The path of the run
        :param report: The report of the run
        :param test_results: The test results of the run
        """
        self.path = path
        self.report = report
        self.test_results = test_results

    @classmethod
    def from_files(cls, path_file: Path, report_file: Path, test_results_file: Path) -> 'BenchmarkRun':
        """
        Load a benchmark run from files

        :param path_file: The path file
        :param report_file: The report file
        :param test_results_file: The test results file
        :return: The benchmark run
        """
        path = json.loads(path_file.read_text())
        report = json.loads(report_file.read_text())
        if test_results_file.exists():
            test_results = json.loads(test_results_file.read_text())
        else:
            test_results = {}

        return cls(path, report, test_results)

    @property
    def test_duration(self) -> float:
        """
        The duration of the test

        :return: The duration of the test
        """
        return self.test_results['testDuration']

    @property
    def driver_time_spent_waiting(self) -> float:
        """
        The time the driver spent waiting

        :return: The time the driver spent waiting
        """
        return self.test_results['driverTimeSpentWaiting']

    @property
    def vertex_coverage(self) -> int:
        """
        The vertex coverage

        :return: The vertex coverage
        """
        return self.test_results['vertexCoverage']

    @property
    def edge_coverage(self) -> int:
        """
        The edge coverage

        :return: The edge coverage
        """
        return self.test_results['edgeCoverage']

    @property
    def is_failure(self) -> bool:
        """
        Whether the run is a failure

        :return: Whether the run is a failure
        """
        return 'failures' in self.test_results

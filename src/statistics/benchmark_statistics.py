from typing import Callable

from models.benchmark_generator import BenchmarkGenerator


class BenchmarkStatistics:
    """
    A class used to calculate statistics for the benchmark results
    """

    @staticmethod
    def get_statistics_functions() -> dict[str, Callable[[dict[str, list[BenchmarkGenerator]]], dict]]:
        """
        Get the available statistics functions

        :return: a dictionary with the available statistics functions
        """
        return {}

    @staticmethod
    def create_statistics(grouped_generators: dict[str, list[BenchmarkGenerator]], whitelist: list[str] = None,
                          blacklist: list[str] = None) -> dict[str, dict]:
        """
        Create the statistics for the benchmark

        :param grouped_generators: The generator benchmarks to analyse, grouped by generator name
        :param whitelist: The list of plot functions to include, if None, all are included
        :param blacklist: The list of plot functions to exclude, if None, none are excluded
        :return: A dictionary with the statistics
        """
        statistics: dict[str, dict] = {}

        for function_name, statistics_function in BenchmarkStatistics.get_statistics_functions().items():
            statistics[function_name] = statistics_function(grouped_generators)

        return statistics

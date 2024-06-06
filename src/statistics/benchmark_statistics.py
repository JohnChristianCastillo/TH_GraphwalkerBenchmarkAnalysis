from typing import Callable

from models.benchmark import Benchmark
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
        return {'total_test_suite_size_comparison': BenchmarkStatistics.total_test_suite_size_comparison,
                'total_generation_time_comparison': BenchmarkStatistics.total_generation_time_comparison,
                'average_test_suite_size_comparison': BenchmarkStatistics.average_test_suite_size_comparison,
                'average_generation_time_comparison': BenchmarkStatistics.average_generation_time_comparison,
                'min_test_suite_size_comparison': BenchmarkStatistics.min_test_suite_size_comparison,
                'min_generation_time_comparison': BenchmarkStatistics.min_generation_time_comparison,
                'max_test_suite_size_comparison': BenchmarkStatistics.max_test_suite_size_comparison,
                'max_generation_time_comparison': BenchmarkStatistics.max_generation_time_comparison}

    @staticmethod
    def get_statistics_functions_test_execution() -> dict[
        str, Callable[[Benchmark, dict[str, list[BenchmarkGenerator]]], dict]]:
        """
        Get the available statistics functions for test execution time

        :return: a dictionary with the available statistics functions
        """
        return {'average_test_execution_time_comparison': BenchmarkStatistics.average_test_execution_time_comparison,
                'min_test_execution_time_comparison': BenchmarkStatistics.min_test_execution_time_comparison,
                'max_test_execution_time_comparison': BenchmarkStatistics.max_test_execution_time_comparison}

    @staticmethod
    def create_statistics(benchmark: Benchmark, grouped_generators: dict[str, list[BenchmarkGenerator]]) -> dict[
        str, dict]:
        """
        Create the statistics for the benchmark

        :param benchmark: The benchmark to analyse
        :param grouped_generators: The generator benchmarks to analyse, grouped by generator name
        :return: A dictionary with the statistics
        """
        statistics: dict[str, dict] = {}

        for function_name, statistics_function in BenchmarkStatistics.get_statistics_functions().items():
            statistics[function_name] = statistics_function(grouped_generators)

        if all([run_group.successful_runs for run_group in benchmark.run_groups]):
            for function_name, statistics_function in BenchmarkStatistics.get_statistics_functions_test_execution().items():
                statistics[function_name] = statistics_function(benchmark, grouped_generators)

        return statistics

    @staticmethod
    def percentual_comparison(grouped_generators: dict[str, list[BenchmarkGenerator]],
                              value_lambda: Callable[[BenchmarkGenerator], int]) -> dict[str, dict[int, float]]:
        """
        Calculate the percentual comparison for the benchmark in percentage, using the smallest value as 100%

        :param grouped_generators: The generator benchmarks to analyse, grouped by generator name
        :param value_lambda: The lambda function to get the value to compare
        :return: A dictionary with the percentual comparison
        """
        percentual_comparison: dict[str, dict[int, float]] = {}

        value_lowest: dict[int, int] = {}
        for generator_name, generators in grouped_generators.items():
            for generator in generators:
                value = value_lambda(generator)
                if generator.stop_coverage not in value_lowest or value < value_lowest[generator.stop_coverage]:
                    value_lowest[generator.stop_coverage] = value

        for generator_name, generators in grouped_generators.items():
            percentual_comparison[generator_name] = {}
            for generator in generators:
                value = value_lambda(generator)
                percentual_comparison[generator_name][generator.stop_coverage] = value / value_lowest[
                    generator.stop_coverage] * 100

        return percentual_comparison

    @staticmethod
    def total_test_suite_size_comparison(grouped_generators: dict[str, list[BenchmarkGenerator]]) -> dict:
        """
        Calculate the total test suite size comparison for the benchmark in percentage, using the smallest total size as 100%

        :param grouped_generators: The generator benchmarks to analyse, grouped by generator name
        :return: A dictionary with the total test suite size comparison
        """
        return BenchmarkStatistics.percentual_comparison(grouped_generators,
                                                         lambda generator: generator.total_test_suite_size)

    @staticmethod
    def total_generation_time_comparison(grouped_generators: dict[str, list[BenchmarkGenerator]]) -> dict:
        """
        Calculate the total generation time comparison for the benchmark in percentage, using the smallest total time as 100%

        :param grouped_generators: The generator benchmarks to analyse, grouped by generator name
        :return: A dictionary with the total generation time comparison
        """
        return BenchmarkStatistics.percentual_comparison(grouped_generators,
                                                         lambda generator: generator.total_generation_time)

    @staticmethod
    def average_test_suite_size_comparison(grouped_generators: dict[str, list[BenchmarkGenerator]]) -> dict:
        """
        Calculate the average test suite size comparison for the benchmark in percentage, using the smallest average size as 100%

        :param grouped_generators: The generator benchmarks to analyse, grouped by generator name
        :return: A dictionary with the average test suite size comparison
        """
        return BenchmarkStatistics.percentual_comparison(grouped_generators,
                                                         lambda generator: generator.average_test_suite_size)

    @staticmethod
    def average_generation_time_comparison(grouped_generators: dict[str, list[BenchmarkGenerator]]) -> dict:
        """
        Calculate the average generation time comparison for the benchmark in percentage, using the smallest average time as 100%

        :param grouped_generators: The generator benchmarks to analyse, grouped by generator name
        :return: A dictionary with the average generation time comparison
        """
        return BenchmarkStatistics.percentual_comparison(grouped_generators,
                                                         lambda generator: generator.average_generation_time)

    @staticmethod
    def min_test_suite_size_comparison(grouped_generators: dict[str, list[BenchmarkGenerator]]) -> dict:
        """
        Calculate the min test suite size comparison for the benchmark in percentage, using the smallest min size as 100%

        :param grouped_generators: The generator benchmarks to analyse, grouped by generator name
        :return: A dictionary with the min test suite size comparison
        """
        return BenchmarkStatistics.percentual_comparison(grouped_generators,
                                                         lambda generator: generator.min_test_suite_size)

    @staticmethod
    def min_generation_time_comparison(grouped_generators: dict[str, list[BenchmarkGenerator]]) -> dict:
        """
        Calculate the min generation time comparison for the benchmark in percentage, using the smallest min time as 100%

        :param grouped_generators: The generator benchmarks to analyse, grouped by generator name
        :return: A dictionary with the min generation time comparison
        """
        return BenchmarkStatistics.percentual_comparison(grouped_generators,
                                                         lambda generator: generator.min_generation_time)

    @staticmethod
    def max_test_suite_size_comparison(grouped_generators: dict[str, list[BenchmarkGenerator]]) -> dict:
        """
        Calculate the max test suite size comparison for the benchmark in percentage, using the smallest max size as 100%

        :param grouped_generators: The generator benchmarks to analyse, grouped by generator name
        :return: A dictionary with the max test suite size comparison
        """
        return BenchmarkStatistics.percentual_comparison(grouped_generators,
                                                         lambda generator: generator.max_test_suite_size)

    @staticmethod
    def max_generation_time_comparison(grouped_generators: dict[str, list[BenchmarkGenerator]]) -> dict:
        """
        Calculate the max generation time comparison for the benchmark in percentage, using the smallest max time as 100%

        :param grouped_generators: The generator benchmarks to analyse, grouped by generator name
        :return: A dictionary with the max generation time comparison
        """
        return BenchmarkStatistics.percentual_comparison(grouped_generators,
                                                         lambda generator: generator.max_generation_time)

    @staticmethod
    def create_statistics_test_execution(benchmark: Benchmark, grouped_generators: dict[str, list[BenchmarkGenerator]],
                                         value_lambda: Callable) -> dict:
        """
        Create the statistics for a test execution time comparison

        :param benchmark: The benchmark to analyse
        :param grouped_generators: The generator benchmarks, grouped by generator name, to use as whitelist
        :param value_lambda: The lambda function to get the value to compare
        :return: A dictionary with the statistics
        """
        grouped_run_groups = {}
        for run_group in benchmark.run_groups_sorted:
            if run_group.algorithm not in grouped_generators.keys():
                continue  # Skip algorithms that are not in the grouped_generators
            if run_group.algorithm not in grouped_run_groups:
                grouped_run_groups[run_group.algorithm] = []
            grouped_run_groups[run_group.algorithm].append(run_group)

        return BenchmarkStatistics.percentual_comparison(grouped_run_groups, value_lambda)

    @staticmethod
    def average_test_execution_time_comparison(benchmark: Benchmark,
                                               grouped_generators: dict[str, list[BenchmarkGenerator]]) -> dict:
        """
        Calculate the average test execution time comparison for the benchmark in percentage, using the smallest average time as 100%

        :param benchmark: The benchmark to analyse
        :param grouped_generators: The generator benchmarks, grouped by generator name, to use as whitelist
        :return: A dictionary with the average test execution time comparison
        """

        return BenchmarkStatistics.create_statistics_test_execution(benchmark, grouped_generators,
                                                                    lambda group: group.average_test_duration)

    @staticmethod
    def min_test_execution_time_comparison(benchmark: Benchmark,
                                           grouped_generators: dict[str, list[BenchmarkGenerator]]) -> dict:
        """
        Calculate the min test execution time comparison for the benchmark in percentage, using the smallest min time as 100%

        :param benchmark: The benchmark to analyse
        :param grouped_generators: The generator benchmarks, grouped by generator name, to use as whitelist
        :return: A dictionary with the min test execution time comparison
        """
        return BenchmarkStatistics.create_statistics_test_execution(benchmark, grouped_generators,
                                                                    lambda group: group.minimum_test_duration)

    @staticmethod
    def max_test_execution_time_comparison(benchmark: Benchmark,
                                           grouped_generators: dict[str, list[BenchmarkGenerator]]) -> dict:
        """
        Calculate the max test execution time comparison for the benchmark in percentage, using the smallest max time as 100%

        :param benchmark: The benchmark to analyse
        :param grouped_generators: The generator benchmarks, grouped by generator name, to use as whitelist
        :return: A dictionary with the max test execution time comparison
        """
        return BenchmarkStatistics.create_statistics_test_execution(benchmark, grouped_generators,
                                                                    lambda group: group.maximum_test_duration)

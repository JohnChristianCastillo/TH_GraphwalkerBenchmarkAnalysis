from io import BytesIO
from typing import Callable

import matplotlib.pyplot as plt
import numpy as np

from models.benchmark_generator import BenchmarkGenerator
from src.models.benchmark import Benchmark


class BenchmarkPlotter:
    """
    A class used to plot the benchmark results
    """
    @staticmethod
    def get_plot_functions() -> dict[str, Callable[[dict[str, list[BenchmarkGenerator]]], None]]:
        """
        Get the available plot functions

        :return: a dictionary with the available plot functions
        """
        return {
            'Total Time': BenchmarkPlotter.plot_total_time,
            'Total Size': BenchmarkPlotter.plot_total_size,
            'Average Time': BenchmarkPlotter.plot_average_time,
            'Average Size': BenchmarkPlotter.plot_average_size,
            'Minimum Time': BenchmarkPlotter.plot_minimum_time,
            'Maximum Time': BenchmarkPlotter.plot_maximum_time,
            'Minimum Size': BenchmarkPlotter.plot_minimum_size,
            'Maximum Size': BenchmarkPlotter.plot_maximum_size,
            'Max-Min Size': BenchmarkPlotter.plot_max_minus_min_size,
            'Coverage vs Time': BenchmarkPlotter.plot_coverage_vs_time,
            'Size/Time': BenchmarkPlotter.plot_average_size_divided_by_average_time
        }

    @staticmethod
    def create_plots(benchmark: Benchmark, whitelist: list[str] = None, blacklist: list[str] = None, show: bool = True) -> dict[str, BytesIO]:
        """
        Plot the benchmark results

        :param benchmark: The benchmark to plot
        :param whitelist: The list of generators to include, if None, all are included
        :param blacklist: The list of generators to exclude, if None, none are excluded
        :param show: bool: Whether to show the plots
        """
        plt.close()
        plots: dict[str, BytesIO] = {}

        grouped_generators = benchmark.report.generators_grouped
        if whitelist:
            grouped_generators = {key: value for key, value in grouped_generators.items() if key.lower() in [x.lower() for x in whitelist]}

        if blacklist:
            grouped_generators = {key: value for key, value in grouped_generators.items() if key.lower() not in [x.lower() for x in blacklist]}

        for plot_function_name, plot_function in BenchmarkPlotter.get_plot_functions().items():
            plt.close()
            plot_function(grouped_generators)
            if show:
                plt.show()
            plots[plot_function_name] = BenchmarkPlotter.save_plot_bytesio()

        return plots

    @staticmethod
    def _post_process_plot(fig, ax):
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

    @staticmethod
    def _plot_bars(fig, ax, grouped_generators: dict[str, list[BenchmarkGenerator]], value_lambda: Callable[[BenchmarkGenerator], int], add_trend_line: bool = True):
        """
        Plot results for a list of benchmark generators
        :param fig: The figure to plot on
        :param ax: The axis to plot on
        :param grouped_generators: The generator benchmarks to plot, grouped by generator name
        :param value_lambda: The lambda function to get the value to plot
        :param add_trend_line: Whether to add a trend line to the plot
        :return:
        """
        group_count = len(grouped_generators)
        bar_width = 6 / group_count

        for i, generator_group in enumerate(grouped_generators):
            coverage_values = [generator.stop_coverage + i * bar_width for generator in
                               grouped_generators[generator_group]]
            property_values = [value_lambda(generator) for generator in
                               grouped_generators[generator_group]]

            ax.bar(coverage_values, property_values, label=generator_group, width=bar_width, align='center')

            if add_trend_line:
                coefficients = np.polyfit(coverage_values, property_values, 4)
                trend_line_function = np.poly1d(coefficients)
                ax.plot(coverage_values, trend_line_function(coverage_values), linestyle='--', linewidth=1)

        BenchmarkPlotter._post_process_plot(fig, ax)

    @staticmethod
    def _plot_lines(fig, ax, grouped_generators: dict[str, list[BenchmarkGenerator]], value_lambda: Callable[[BenchmarkGenerator], int]):
        """
        Plot results for a list of benchmark generators
        :param fig: The figure to plot on
        :param ax: The axis to plot on
        :param grouped_generators: The generator benchmarks to plot, grouped by generator name
        :param value_lambda: The lambda function to get the value to plot
        :return:
        """
        for generator_group in grouped_generators:
            coverage_values = [generator.stop_coverage for generator in grouped_generators[generator_group]]
            property_values = [value_lambda(generator) for generator in grouped_generators[generator_group]]

            ax.plot(coverage_values, property_values, label=generator_group)

        BenchmarkPlotter._post_process_plot(fig, ax)

    @staticmethod
    def plot_total_time(grouped_generators: dict[str, list[BenchmarkGenerator]]):
        """
        Plot the total time taken for each generator in the benchmark

        :param grouped_generators: The generator benchmarks to plot, grouped by generator name
        """
        fig, ax = plt.subplots()

        ax.set_title('Total generation time per generator by coverage value')
        ax.set_xlabel('Coverage (%)')
        ax.set_ylabel('Total Time (μs)')

        BenchmarkPlotter._plot_bars(fig, ax, grouped_generators, lambda generator: generator.total_generation_time)

    @staticmethod
    def plot_total_size(grouped_generators: dict[str, list[BenchmarkGenerator]]):
        """
        Plot the total size of each generator's path in the benchmark

        :param grouped_generators: The generator benchmarks to plot, grouped by generator name
        """
        fig, ax = plt.subplots()

        ax.set_title('Total test suite size per generator by coverage value')
        ax.set_xlabel('Coverage (%)')
        ax.set_ylabel('Total Size (element count)')

        BenchmarkPlotter._plot_bars(fig, ax, grouped_generators, lambda generator: generator.total_test_suite_size)

    @staticmethod
    def plot_average_time(grouped_generators: dict[str, list[BenchmarkGenerator]]):
        """
        Plot the average time taken for each generator in the benchmark

        :param grouped_generators: The generator benchmarks to plot, grouped by generator name
        """
        fig, ax = plt.subplots()

        ax.set_title('Average generation time per generator by coverage value')
        ax.set_xlabel('Coverage (%)')
        ax.set_ylabel('Average Time (μs)')

        BenchmarkPlotter._plot_bars(fig, ax, grouped_generators, lambda generator: generator.average_generation_time)

    @staticmethod
    def plot_average_size(grouped_generators: dict[str, list[BenchmarkGenerator]]):
        """
        Plot the average size of each generator's path in the benchmark

        :param grouped_generators: The generator benchmarks to plot, grouped by generator name
        """
        fig, ax = plt.subplots()

        ax.set_title('Average test suite size per generator by coverage value')
        ax.set_xlabel('Coverage (%)')
        ax.set_ylabel('Average Size (element count)')

        BenchmarkPlotter._plot_bars(fig, ax, grouped_generators, lambda generator: generator.average_test_suite_size)

    @staticmethod
    def plot_minimum_time(grouped_generators: dict[str, list[BenchmarkGenerator]]):
        """
        Plot the minimum time taken for each generator in the benchmark

        :param grouped_generators: The generator benchmarks to plot, grouped by generator name
        """
        fig, ax = plt.subplots()

        ax.set_title('Minimum generation time per generator by coverage value')
        ax.set_xlabel('Coverage (%)')
        ax.set_ylabel('Minimum Time (μs)')

        BenchmarkPlotter._plot_bars(fig, ax, grouped_generators, lambda generator: generator.min_generation_time)

    @staticmethod
    def plot_maximum_time(grouped_generators: dict[str, list[BenchmarkGenerator]]):
        """
        Plot the maximum time taken for each generator in the benchmark

        :param grouped_generators: The generator benchmarks to plot, grouped by generator name
        """
        fig, ax = plt.subplots()

        ax.set_title('Maximum generation time per generator by coverage value')
        ax.set_xlabel('Coverage (%)')
        ax.set_ylabel('Maximum Time (μs)')

        BenchmarkPlotter._plot_bars(fig, ax, grouped_generators, lambda generator: generator.max_generation_time)

    @staticmethod
    def plot_minimum_size(grouped_generators: dict[str, list[BenchmarkGenerator]]):
        """
        Plot the minimum size of each generator's path in the benchmark

        :param grouped_generators: The generator benchmarks to plot, grouped by generator name
        """
        fig, ax = plt.subplots()

        ax.set_title('Minimum test suite size per generator by coverage value')
        ax.set_xlabel('Coverage (%)')
        ax.set_ylabel('Minimum Size (element count)')

        BenchmarkPlotter._plot_bars(fig, ax, grouped_generators, lambda generator: generator.min_test_suite_size)

    @staticmethod
    def plot_maximum_size(grouped_generators: dict[str, list[BenchmarkGenerator]]):
        """
        Plot the maximum size of each generator's path in the benchmark

        :param grouped_generators: The generator benchmarks to plot, grouped by generator name
        """
        fig, ax = plt.subplots()

        ax.set_title('Maximum test suite size per generator by coverage value')
        ax.set_xlabel('Coverage (%)')
        ax.set_ylabel('Maximum Size (element count)')

        BenchmarkPlotter._plot_bars(fig, ax, grouped_generators, lambda generator: generator.max_test_suite_size)

    @staticmethod
    def plot_max_minus_min_size(grouped_generators: dict[str, list[BenchmarkGenerator]]):
        """
        Plot the difference between the maximum and minimum size of each generator's path in the benchmark

        :param grouped_generators: The generator benchmarks to plot, grouped by generator name
        """
        fig, ax = plt.subplots()

        ax.set_title('Difference between maximum and minimum test suite size\nper generator by coverage value')
        ax.set_xlabel('Coverage (%)')
        ax.set_ylabel('Difference (element count)')

        BenchmarkPlotter._plot_bars(fig, ax, grouped_generators, lambda generator: generator.max_test_suite_size - generator.min_test_suite_size)

    @staticmethod
    def plot_coverage_vs_time(grouped_generators: dict[str, list[BenchmarkGenerator]]):
        """
        Plot the coverage vs time for each generator in the benchmark

        :param grouped_generators: The generator benchmarks to plot, grouped by generator name
        """
        fig, ax = plt.subplots()

        ax.set_title('Coverage vs Time per generator')
        ax.set_xlabel('Coverage (%)')
        ax.set_ylabel('Time (μs)')

        BenchmarkPlotter._plot_lines(fig, ax, grouped_generators, lambda generator: generator.total_generation_time)

    @staticmethod
    def plot_average_size_divided_by_average_time(grouped_generators: dict[str, list[BenchmarkGenerator]]):
        """
        Plot the average size of each generator's path divided by the average time taken for each generator in the benchmark

        --> Higher values indicate a more efficient generator because it generates more elements in less time?

        :param grouped_generators: The generator benchmarks to plot, grouped by generator name
        """
        fig, ax = plt.subplots()

        ax.set_title('Average test suite size divided by\naverage generation time per generator by coverage value')
        ax.set_xlabel('Coverage (%)')
        ax.set_ylabel('Size/Time (element count/μs)')

        BenchmarkPlotter._plot_bars(fig, ax, grouped_generators, lambda generator: generator.average_test_suite_size / generator.average_generation_time)

    @staticmethod
    def save_plot(output: str):
        """
        Save the plot to a file

        :param output: str: The path to save the plot
        """
        plt.savefig(output)

    @staticmethod
    def save_plot_bytesio() -> BytesIO:
        """
        Save the plot to a BytesIO object
        """
        bytesio = BytesIO()
        plt.savefig(bytesio)
        return bytesio

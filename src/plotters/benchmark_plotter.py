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
    def plot_benchmark(benchmark: Benchmark, show: bool = True):
        """
        Plot the benchmark results

        :param benchmark: Benchmark: The benchmark to plot
        :param show: bool: Whether to show the plot
        """
        plt.close()
        plots: list[BytesIO] = []

        BenchmarkPlotter.plot_total_time(benchmark)
        if show:
            plt.show()
        plots.append(BenchmarkPlotter.save_plot_bytesio())
        plt.close()

        BenchmarkPlotter.plot_average_time(benchmark)
        if show:
            plt.show()
        plots.append(BenchmarkPlotter.save_plot_bytesio())
        plt.close()

        BenchmarkPlotter.plot_total_size(benchmark)
        if show:
            plt.show()
        plots.append(BenchmarkPlotter.save_plot_bytesio())
        plt.close()

        BenchmarkPlotter.plot_average_size(benchmark)
        if show:
            plt.show()
        plots.append(BenchmarkPlotter.save_plot_bytesio())
        plt.close()

    @staticmethod
    def _plot_benchmark(fig, ax, benchmark: Benchmark, value_lambda: Callable[[BenchmarkGenerator], int]):
        """
        Plot a property of the benchmark
        :param benchmark: The benchmark to plot
        :param value_lambda: The lambda function to get the value to plot
        :return:
        """
        generator_groups = benchmark.report.generators_grouped
        group_count = len(generator_groups)
        bar_width = 6 / group_count

        for i, generator_group in enumerate(generator_groups):
            coverage_values = [generator.stop_coverage + i * bar_width for generator in
                               generator_groups[generator_group]]
            property_values = [value_lambda(generator) for generator in
                               generator_groups[generator_group]]

            ax.bar(coverage_values, property_values, label=generator_group, width=bar_width, align='center')

            coefficients = np.polyfit(coverage_values, property_values, 4)
            trend_line_function = np.poly1d(coefficients)
            ax.plot(coverage_values, trend_line_function(coverage_values), linestyle='--', linewidth=1)

        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

    @staticmethod
    def plot_total_time(benchmark: Benchmark):
        """
        Plot the total time taken for each generator in the benchmark

        :param benchmark: Benchmark: The benchmark to plot
        """
        fig, ax = plt.subplots()

        ax.set_title('Total generation time per generator by coverage value')
        ax.set_xlabel('Coverage (%)')
        ax.set_ylabel('Total Time (μs)')

        BenchmarkPlotter._plot_benchmark(fig, ax, benchmark, lambda generator: generator.total_generation_time)

    @staticmethod
    def plot_total_size(benchmark: Benchmark):
        """
        Plot the total size of each generator's path in the benchmark

        :param benchmark: Benchmark: The benchmark to plot
        """
        fig, ax = plt.subplots()

        ax.set_title('Total test suite size per generator by coverage value')
        ax.set_xlabel('Coverage (%)')
        ax.set_ylabel('Total Size (element count)')

        BenchmarkPlotter._plot_benchmark(fig, ax, benchmark, lambda generator: generator.total_test_suite_size)

    @staticmethod
    def plot_average_time(benchmark: Benchmark):
        """
        Plot the average time taken for each generator in the benchmark

        :param benchmark: Benchmark: The benchmark to plot
        """
        fig, ax = plt.subplots()

        ax.set_title('Average generation time per generator by coverage value')
        ax.set_xlabel('Coverage (%)')
        ax.set_ylabel('Average Time (μs)')

        BenchmarkPlotter._plot_benchmark(fig, ax, benchmark, lambda generator: generator.average_generation_time)

    @staticmethod
    def plot_average_size(benchmark: Benchmark):
        """
        Plot the average size of each generator's path in the benchmark

        :param benchmark: Benchmark: The benchmark to plot
        """
        fig, ax = plt.subplots()

        ax.set_title('Average test suite size per generator by coverage value')
        ax.set_xlabel('Coverage (%)')
        ax.set_ylabel('Average Size (element count)')

        BenchmarkPlotter._plot_benchmark(fig, ax, benchmark, lambda generator: generator.average_test_suite_size)

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

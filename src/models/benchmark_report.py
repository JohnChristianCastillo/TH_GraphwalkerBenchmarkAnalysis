import json

from src.models.benchmark_generator import BenchmarkGenerator


class BenchmarkReport(dict):
    """
    Represents a general benchmark report, read from a JSON file.
    """

    def __init__(self, data: dict, name: str):
        """
        Initialize the benchmark report.
        """
        super().__init__(data)
        self._name = name

    @classmethod
    def from_file(cls, path: str) -> "BenchmarkReport":
        """
        Load benchmark report from a file.
        """
        with open(path, "r") as file:
            return cls(json.load(file), file.name.rstrip(".json"))

    @property
    def generators(self) -> list[BenchmarkGenerator]:
        """
        Get the generator results.
        """
        generators = []
        for generator in self["Generators"].keys():
            generators.append(BenchmarkGenerator(self["Generators"][generator], generator))
        return generators

    @property
    def generators_sorted(self) -> list[BenchmarkGenerator]:
        """
        Get the generator results sorted by name.
        """
        generators = self.generators
        generators.sort(key=BenchmarkReport.generator_sort_lambda)
        return generators

    @staticmethod
    def generator_sort_lambda(generator: BenchmarkGenerator):
        return generator.generator, generator.stop_coverage

    @property
    def generators_grouped(self) -> dict[str, list[BenchmarkGenerator]]:
        """
        Get the generator results grouped by generator name.
        """
        generators = {}
        for generator in self.generators_sorted:
            if generator.generator not in generators:
                generators[generator.generator] = []
            generators[generator.generator].append(generator)
        return generators

    @property
    def name(self) -> str:
        """
        Get the name of the benchmark.
        """
        return self._name

    @property
    def runs(self) -> int:
        """
        Get the number of runs.
        """
        return self["Runs"]

    @property
    def threads(self) -> int:
        """
        Get the number of threads.
        """
        return self["Threads"]

    @property
    def verbose(self) -> bool:
        """
        Get the verbose flag.
        """
        return self["Verbose"]

    @property
    def unified(self) -> bool:
        """
        Get the unified flag.
        """
        return self["Unified"]

    @property
    def output(self) -> str:
        """
        Get the output directory.
        """
        return self["Output"]

    @property
    def model_path(self) -> str:
        """
        Get the (input) model path.
        """
        return self["ModelPath"]

    @property
    def generators_path(self) -> str:
        """
        Get the (input) generators path.
        """
        return self["GeneratorsPath"]

    @property
    def base_seed(self) -> int:
        """
        Get the base seed.
        """
        return self["BaseSeed"]

    @property
    def kill_after(self) -> int:
        """
        Get the kill after value.
        """
        return self["KillAfter"]

    @property
    def timestamp(self) -> str:
        """
        Get the timestamp.
        """
        return self["Timestamp"]

    @property
    def median_runs(self) -> int:
        """
        Get the number of runs to calculate the median.
        """
        return self["MedianRuns"]

    def __str__(self) -> str:
        """
        Get the string representation.
        """
        return f"BenchmarkReport({self['Output']})"

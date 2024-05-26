class BenchmarkGenerator(dict):
    """
    Represents a generator in a benchmark report.
    """
    def __init__(self, generator: dict, name: str):
        super().__init__(generator)
        self._name = name

    @property
    def name(self) -> str:
        """
        Get the generator name.
        """
        return self._name

    @property
    def generator(self) -> str:
        """
        Get the generator.
        """
        return self.name.split("(")[0]

    @property
    def stop_condition(self) -> str:
        """
        Get the stop condition.
        """
        start = self.name.find("(")
        end = self.name.rfind(")")
        return self.name[start + 1:end]

    @property
    def total_generation_time(self) -> int:
        """
        Get the total generation time.
        """
        return self["TotalGenerationTime"]

    @property
    def total_test_suite_size(self) -> int:
        """
        Get the total test suite size.
        """
        return self["TotalTestSuiteSize"]

    @property
    def average_generation_time(self) -> int:
        """
        Get the average generation time.
        """
        return self["AverageGenerationTime"]

    @property
    def average_test_suite_size(self) -> int:
        """
        Get the average test suite size.
        """
        return self["AverageTestSuiteSize"]

    @property
    def min_generation_time(self) -> int:
        """
        Get the minimum generation time.
        """
        return self["MinGenerationTime"]

    @property
    def max_generation_time(self) -> int:
        """
        Get the maximum generation time.
        """
        return self["MaxGenerationTime"]

    @property
    def min_test_suite_size(self) -> int:
        """
        Get the minimum test suite size.
        """
        return self["MinTestSuiteSize"]

    @property
    def max_test_suite_size(self) -> int:
        """
        Get the maximum test suite size.
        """
        return self["MaxTestSuiteSize"]

    def __str__(self):
        """
        Return the string representation.
        """
        return f"{self.name} ({self.total_generation_time}ms, {self.total_test_suite_size} tests)"

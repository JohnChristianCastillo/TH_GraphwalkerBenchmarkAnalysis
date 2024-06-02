from utils.benchmark_name_parser import parse_stop_condition_from_name, parse_coverage_from_stop_condition, \
    parse_algorithm_from_name


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
    def algorithm(self) -> str:
        """
        Get the generator's algorithm.
        """
        return parse_algorithm_from_name(self.name)

    @property
    def stop_condition(self) -> str:
        """
        Get the stop condition.
        """
        return parse_stop_condition_from_name(self.name)

    @property
    def stop_coverage(self) -> int:
        """
        Get the stop condition's coverage.
        """
        return parse_coverage_from_stop_condition(self.stop_condition)

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

    @property
    def total_vertex_visits(self) -> int:
        """
        Get the total vertex visits.
        """
        return self["TotalVertexVisits"]

    @property
    def total_edge_visits(self) -> int:
        """
        Get the total edges visits.
        """
        return self["TotalEdgeVisits"]

    @property
    def average_vertex_visits(self) -> int:
        """
        Get the average vertex visits.
        """
        return self["AverageVertexVisits"]

    @property
    def average_edge_visits(self) -> int:
        """
        Get the average edges visits.
        """
        return self["AverageEdgeVisits"]

    @property
    def total_unvisited_vertices(self) -> int:
        """
        Get the total unvisited vertices.
        """
        return self["TotalUnvisitedVertices"]

    @property
    def average_unvisited_vertices(self) -> int:
        """
        Get the average unvisited vertices.
        """
        return self["AverageUnvisitedVertices"]

    @property
    def total_unvisited_edges(self) -> int:
        """
        Get the total unvisited edges.
        """
        return self["TotalUnvisitedEdges"]

    @property
    def average_unvisited_edges(self) -> int:
        """
        Get the average unvisited edges.
        """
        return self["AverageUnvisitedEdges"]

    @property
    def total_vertex_visits_individual(self) -> dict[str, int]:
        """
        Get the total vertex visits by individual vertex.
        """
        return self["TotalVertexVisitsIndividual"]

    @property
    def total_edge_visits_individual(self) -> dict[str, int]:
        """
        Get the total edges visits by individual edge.
        """
        return self["TotalEdgeVisitsIndividual"]

    @property
    def average_vertex_visits_individual(self) -> dict[str, int]:
        """
        Get the average vertex visits by individual vertex.
        """
        return self["AverageVertexVisitsIndividual"]

    @property
    def average_edge_visits_individual(self) -> dict[str, int]:
        """
        Get the average edges visits by individual edge.
        """
        return self["AverageEdgeVisitsIndividual"]

    def __str__(self):
        """
        Return the string representation.
        """
        return f"{self.name} ({self.total_generation_time}ms, {self.total_test_suite_size} tests)"

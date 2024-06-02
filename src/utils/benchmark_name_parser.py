def parse_algorithm_from_name(name: str) -> str:
    """
    Parse the algorithm from a generator name.

    :param name: The generator name.
    :return: The algorithm.
    """
    return name.split("(")[0]


def parse_stop_condition_from_name(name: str) -> str:
    """
    Parse the stop condition from a generator name.

    :param name: The generator name.
    :return: The stop condition.
    """
    start = name.find("(")
    end = name.rfind(")")
    return name[start + 1:end]


def parse_coverage_from_stop_condition(stop_condition: str) -> int:
    """
    Parse the coverage from a stop condition.

    :param stop_condition: The stop condition.
    :return: The coverage.
    """
    start = stop_condition.lower().find("coverage(")
    end = stop_condition.find(")")
    return int(stop_condition[start + 9:end])

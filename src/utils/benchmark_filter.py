from models.benchmark_generator import BenchmarkGenerator


def filter_whitelist_grouped_generators(grouped_generators: dict[str, list[BenchmarkGenerator]],
                                        whitelist: list[str]) -> dict[str, list[BenchmarkGenerator]]:
    """
    Filter grouped generators by the whitelist

    :param grouped_generators: The generator benchmarks to filter
    :param whitelist: The whitelist of generators to include
    :return: The filtered generators
    """
    if not whitelist:
        return grouped_generators
    return {key: value for key, value in grouped_generators.items() if key.lower() in [x.lower() for x in whitelist]}


def filter_blacklist_grouped_generators(grouped_generators: dict[str, list[BenchmarkGenerator]],
                                        blacklist: list[str]) -> dict[str, list[BenchmarkGenerator]]:
    """
    Filter grouped generators by the blacklist

    :param grouped_generators: The generator benchmarks to filter
    :param blacklist: The blacklist of generators to exclude
    :return: The filtered generators
    """
    if not blacklist:
        return grouped_generators
    return {key: value for key, value in grouped_generators.items() if
            key.lower() not in [x.lower() for x in blacklist]}


def filter_grouped_generators(generators: dict[str, list[BenchmarkGenerator]], whitelist: list[str],
                              blacklist: list[str]) -> dict[str, list[BenchmarkGenerator]]:
    """
    Filter the generators by the whitelist and blacklist

    :param generators: The generator benchmarks to filter
    :param whitelist: The whitelist of generators to include
    :param blacklist: The blacklist of generators to exclude
    :return: The filtered generators
    """
    return filter_blacklist_grouped_generators(filter_whitelist_grouped_generators(generators, whitelist), blacklist)

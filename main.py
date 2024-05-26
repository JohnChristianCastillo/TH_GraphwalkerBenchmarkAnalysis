from pathlib import Path

from src.models.benchmark import Benchmark
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create benchmark plots & human-readable reports from GraphWalker benchmark output.')
    parser.add_argument('--benchmark', '-b', type=str, help='Path to the benchmark directory.', required=True)
    parser.add_argument('--output', '-o', type=str, help='Path to the output directory. Default \".\"', default='.')
    parser.add_argument('--verbose', '-v', action='store_true', help='Print verbose output.')
    args = parser.parse_args()

    input_path = Path(args.benchmark)
    if not input_path.exists():
        print(f'Error: Path \"{input_path.absolute()}\" does not exist.')
        raise FileNotFoundError(input_path.absolute())

    if args.verbose:
        print(f'Creating benchmark from \"{input_path}\"')

    benchmark = Benchmark.from_dir(str(input_path.absolute()))
    if args.verbose:
        print(f'Loaded benchmark \"{benchmark}\" with {len(benchmark.report.generators)} generators.')

    output = Path(args.output)
    output = output / benchmark.name
    output.mkdir(parents=True, exist_ok=True)

    if args.verbose:
        print(f'Saving output to \"{output.absolute()}\"')
import argparse
from pathlib import Path

from report.report_factory import ReportFactory
from src.models.benchmark import Benchmark

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create benchmark plots & human-readable reports from GraphWalker benchmark output.')
    parser.add_argument('--benchmark', '-b', type=str, help='Path to the benchmark directory.', required=True)
    parser.add_argument('--output', '-o', type=str, help='Path to the output directory. Default \".\"', default='.')
    parser.add_argument('--output_suffix', '-s', type=str, help='Suffix to append to the output directory name.')
    parser.add_argument('--report_type', '-r', type=str,
                        help='Type of report to generate. Default \"html\". Options: html, pdf, raw_data\nNote that pdf requires playwright to be installed. (\'playwright install\', using an activated python environment with playwright)',
                        default='pdf')
    parser.add_argument('--whitelist', nargs='+', help='Whitelist of generators to include in the report.')
    parser.add_argument('--blacklist', nargs='+', help='Blacklist of generators to exclude from the report.')
    parser.add_argument('--verbose', '-v', action='store_true', help='Print verbose output.')
    args = parser.parse_args()

    input_path = Path(args.benchmark)
    if not input_path.exists():
        print(f'Error: Path \"{input_path.absolute()}\" does not exist.')
        raise FileNotFoundError(input_path.absolute())

    # Create early to fail fast if the report type is invalid
    report_factory = ReportFactory(args.report_type)

    if args.verbose:
        print(f'Creating benchmark from \"{input_path}\"')

    benchmark = Benchmark.from_dir(str(input_path.absolute()))
    if args.verbose:
        print(f'Loaded benchmark \"{benchmark}\" with {len(benchmark.report.generators)} generators.')

    output = Path(args.output)
    output = output / benchmark.name if not args.output_suffix else output / f'{benchmark.name}{args.output_suffix}'
    output.mkdir(parents=True, exist_ok=True)

    if args.verbose:
        print(f'Saving output to \"{output.absolute()}\"')

    report_factory.create_report(benchmark, output, whitelist=args.whitelist, blacklist=args.blacklist)

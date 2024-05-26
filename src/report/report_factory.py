import json
from pathlib import Path
from shutil import rmtree
from time import time

from playwright.sync_api import sync_playwright
from seedir import seedir

from models.benchmark import Benchmark
from plotters.benchmark_plotter import BenchmarkPlotter
from statistics.benchmark_statistics import BenchmarkStatistics
from utils.benchmark_filter import filter_grouped_generators


class ReportFactory:
    def __init__(self, report_type: str = 'html', prompt_delete_temp: bool = True):
        """
        Create a report factory

        :param report_type: The type of report to create
        :param prompt_delete_temp: Whether to prompt the user to delete temporary files
        """
        self.report_type = report_type
        self.prompt_delete_temp = prompt_delete_temp
        self.report = None

    def create_report(self, benchmark: Benchmark, output: Path, whitelist: list[str] = None,
                      blacklist: list[str] = None):
        """
        Create the report

        :param benchmark: The benchmark to create the report for
        :param output: The output path
        :param whitelist: The whitelist of generators to include in the report
        :param blacklist: The blacklist of generators to exclude from the report
        """
        if self.report_type.lower() == 'html':
            return self.create_html_report(benchmark, output, whitelist, blacklist)
        elif self.report_type.lower() == 'pdf':
            return self.create_pdf_report(benchmark, output, whitelist, blacklist, self.prompt_delete_temp)
        elif self.report_type.lower() == 'raw_data':
            return self.create_raw_report(benchmark, output, whitelist, blacklist)
        else:
            raise ValueError(f'Unknown report type \"{self.report_type}\"')

    @staticmethod
    def create_raw_report(benchmark: Benchmark, output: Path, whitelist: list[str] = None, blacklist: list[str] = None):
        """
        Create a raw report
        """
        grouped_generators = filter_grouped_generators(benchmark.report.generators_grouped, whitelist, blacklist)
        statistics = BenchmarkStatistics.create_statistics(grouped_generators)
        plots = BenchmarkPlotter.create_plots(grouped_generators)

        with open(output / 'benchmarks.json', 'w') as f:
            f.write(json.dumps(benchmark.report, indent=4))

        with open(output / 'statistics.json', 'w') as f:
            f.write(json.dumps(statistics, indent=4))

        images_dir = output / 'images'
        images_dir.mkdir(parents=True, exist_ok=True)
        for name, bytesIO in plots.items():
            with open(images_dir / f'{name}.png', 'wb') as f:
                f.write(bytesIO.getvalue())

    @staticmethod
    def create_html_report(benchmark: Benchmark, output: Path, whitelist: list[str] = None,
                           blacklist: list[str] = None):
        """"
        Create an HTML report
        """
        grouped_generators = filter_grouped_generators(benchmark.report.generators_grouped, whitelist, blacklist)
        plots = BenchmarkPlotter.create_plots(grouped_generators)
        statistics = BenchmarkStatistics.create_statistics(grouped_generators)

        html_file = output / 'index.html'
        images_dir = output / 'images'
        images_dir.mkdir(parents=True, exist_ok=True)
        for name, bytesIO in plots.items():
            with open(images_dir / f'{name}.png', 'wb') as f:
                f.write(bytesIO.getvalue())

        with open(html_file, 'w') as f:
            f.write('<html>\n')
            f.write('<head>\n')
            f.write(f"<title>GraphWalker Benchmark Report</title>\n")
            f.write('</head>\n')
            f.write('<body>\n')

            f.write(f"<h1>GraphWalker Benchmark Report: {benchmark.name}</h1>\n")

            f.write('<h2>Statistics</h2>\n')
            f.write('<table>\n')

            #
            #   Statistics are first grouped by statistic type, then grouped by generator name, and then by stop coverage, to then result in a value.
            #
            #   Example table:
            #
            #   | Statistic | Generator | Stop Coverage | Value |
            #   |-----------|-----------|---------------|-------|
            #   | Statistic 1 | Generator 1 | 100 | 123 |
            #   | Statistic 1 | Generator 1 | 90 | 456 |
            #   | Statistic 1 | Generator 2 | 100 | 789 |
            #   | Statistic 1 | Generator 2 | 90 | 1011 |
            #   | Statistic 2 | Generator 1 | 100 | 1213 |
            #

            # We will group them by one table per statistic

            for statistic_name, statistics in statistics.items():
                f.write(f"<h3>{statistic_name}</h3>\n")
                f.write('<table>\n')
                f.write('<tr>\n')
                f.write('<th>Generator</th>\n')
                f.write('<th>Stop Coverage</th>\n')
                f.write('<th>Value</th>\n')
                f.write('</tr>\n')

                for generator_name, generator_statistics in statistics.items():
                    for stop_coverage, value in generator_statistics.items():
                        f.write('<tr>\n')
                        f.write(f'<td>{generator_name}</td>\n')
                        f.write(f'<td>{stop_coverage}</td>\n')
                        f.write(f'<td>{round(value, 2)}</td>\n')
                        f.write('</tr>\n')

                f.write('</table>\n')

            f.write('<h2>Plots</h2>\n')
            for name in plots.keys():
                f.write(f'<h3>{name}</h3>\n')
                f.write(f'<img src="images/{name}.png" alt="{name}">\n')

            f.write('</body>\n')
            f.write('</html>\n')

    @staticmethod
    def create_pdf_report(benchmark: Benchmark, output: Path, whitelist: list[str] = None, blacklist: list[str] = None,
                          prompt_delete_temp: bool = True):
        """
        Create a PDF report
        """
        temp_dir = output / f"temp_{time()}"
        temp_dir.mkdir(parents=True, exist_ok=False)

        ReportFactory.create_html_report(benchmark, temp_dir, whitelist, blacklist)

        playwright_instance = sync_playwright().start()
        chromium = playwright_instance.chromium
        browser = chromium.launch()
        page = browser.new_page()
        page.goto(f'file://{temp_dir.absolute()}/index.html')
        page.pdf(path=output / 'report.pdf')
        browser.close()
        playwright_instance.stop()

        # List files in temp directory, and give prompt to delete
        print(f'PDF report created at \"{output / "report.pdf"}\"')
        if prompt_delete_temp:
            print(f'Temporary files are located at \"{temp_dir}\":')
            seedir(temp_dir)

            print('Delete temporary files? (y/n)')
            delete_temp = input()
            if delete_temp.lower() == 'y':
                rmtree(temp_dir)
                print('Files deleted.')
            else:
                print(f'Files not deleted. Temporary files are located at \"{temp_dir}\"')
        else:
            rmtree(temp_dir)
            print('Temporary files deleted.')

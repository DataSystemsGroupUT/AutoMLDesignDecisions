import argparse
import warnings

from benchmark import *

warnings.simplefilter("ignore")


def benchmark(dataset_file: str, output_file: str,
              time: int, model: str, dataset_test_file: str = None,
              config: List[str] = None):
    model_to_bench = {
        'autosklearn': AutoSklearnBenchmark,
        'autosklearn-v': AutoSklearnVanillaBenchmark,
        'autosklearn-m': AutoSklearnMetaBenchmark,
        'autosklearn-e': AutoSklearnEnsBenchmark,
        'tpot': TPOTBenchmark,
        'recipe': RecipeBenchmark
    }
    if model in model_to_bench:
        model_to_bench[model]().benchmark(dataset_file, output_file,
                                          time_limit=time, dataset_test_file=dataset_test_file,
                                          config=config)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='Dataset file')
    parser.add_argument('output_file', help='Benchmark result file')
    parser.add_argument('-t', '--time', type=int, help='Time budget')
    parser.add_argument('-m', '--model', help='AutoML Model')
    parser.add_argument('-te', '--test_file', help='Dataset test file')
    parser.add_argument('-c', '--config', nargs='*')
    args = parser.parse_args()

    benchmark(dataset_file=args.input_file, output_file=args.output_file,
              time=args.time, model=args.model, dataset_test_file=args.test_file,
              config=args.config)

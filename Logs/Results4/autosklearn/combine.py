import argparse
import warnings
import os
import pandas as pd

warnings.simplefilter("ignore")


def combine(input_dir, output_dir):
    data = {}
    for root, subdirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.csv'):
                dataset = pd.read_csv(os.path.join(root, file))
                data.setdefault(file, []).append(dataset)
    for model, datasets in data.items():
        dataset = pd.concat(datasets)

        dataset = dataset.rename(columns={dataset.columns[0]: 'dataset'}).set_index('dataset').sort_index()
        dataset.to_csv(os.path.join(output_dir, model))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir')
    parser.add_argument('output_dir')
    args = parser.parse_args()

    combine(input_dir=args.input_dir, output_dir=args.output_dir)
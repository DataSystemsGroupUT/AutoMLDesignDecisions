import pandas as pd
import os


def parse_smartML(directory):
    result = pd.DataFrame(columns=['smartml_model', 'smartml_train_acc', 'smartml_valid_acc'])  # output DataFrame
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            log = open(os.path.join(subdir, file))
            for line in log.readlines():
                val = []  # a single row in df that parse a single line
                line_list = line.split(',')
                val.append('_'.join(line_list[0].split('/')[-1].split('_')[:-1])) # dataset name
                val.append(line_list[1]) # selected algorithm
                val.append(line_list[3]) # training accuracy
                val.append(line_list[4]) # validation accuracy
                result.loc[val[0]] = val[1:]
    return result


def main():
    path = r'C:\Users\HassanEldeeb\Desktop\Benchmark_Deliverables\Logs\Results10\smartml'
    parse_smartML(path)


if __name__ == "__main__":
    # execute only if run as a script
    main()
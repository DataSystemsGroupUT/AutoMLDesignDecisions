import pandas as pd
import os


def parse_recipe(directory):
    result = pd.DataFrame(columns=['recipe_valid_acc', 'recipe_valid_precision', 'recipe_valid_recall', 'recipe_valid_f1',
                                   'recipe_train_acc', 'recipe_train_precision', 'recipe_train_recall', 'recipe_train_f1',
                                   'recipe_test_acc', 'recipe_test_precision', 'recipe_test_recall', 'recipe_test_f1'])  # output DataFrame
    for filename in os.listdir(directory):
        if filename.endswith(".csv") and filename.startswith('Result'):
            f = open(os.path.join(directory,filename))
            lines = f.readlines()
            vars = lines[0].split(',')
            vals = vars[4:16]
            if vals == []:
                vals = 12*['NA']
            result.loc['_'.join(filename.split('_')[1:-1])] = vals
    return result


def main():
    path = r'C:\Users\HassanEldeeb\Desktop\Benchmark_Deliverables\Logs\Results30\Recipe'
    parse_recipe(path)


if __name__ == "__main__":
    # execute only if run as a script
    main()
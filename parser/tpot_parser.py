import pandas as pd
import os
import ast

def parse_tpot(directory):
    result = pd.DataFrame(columns=['tpot_accuracy_mean', 'tpot_f1_score_mean', 'tpot_model_1',
                                   'tpot_precision_mean', 'tpot_recall_mean', 'tpot_time_mean'])
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                sub_result = pd.read_csv(os.path.join(subdir, file), index_col=0)
                for col in sub_result.columns:
                    if col not in ['accuracy_mean', 'f1score_mean', 'model_1', 'precision_mean', 'recall_mean', 'time_mean']:
                        sub_result.drop(col, axis='columns', inplace=True)
                # sub_result = sub_result[['accuracy_mean', 'f1score_mean', 'model_1', 'precision_mean', 'recall_mean', 'time_mean']]
                sub_result.rename(columns={'accuracy_mean': 'tpot_accuracy_mean',
                                       'f1score_mean': 'tpot_f1_score_mean',
                                       'model_1': 'tpot_model_1',
                                       'precision_mean': 'tpot_precision_mean',
                                       'recall_mean': 'tpot_recall_mean',
                                       'time_mean': 'tpot_time_mean'}, inplace=True)
                # result = result.append(sub_result)
                result = pd.concat([result, sub_result], axis=0, sort=True)
    result.tpot_model_1 = result.tpot_model_1.apply(get_class)
    return result

def get_class (model):
    if isinstance(model, str):
        model = '{' +'}'.join('{'.join(model.split('{')[1:]).split('}')[0:1]) + '}'
        m = ast.literal_eval(model)
        if 'classifier:__choice__' in m:
            classifier = m['classifier:__choice__']
        else:
            classifier = ''
        return classifier
    else:
        return ''


def main():
    path = r'C:\Users\HassanEldeeb\Desktop\Benchmark_Deliverables\Logs\Results10\tpot'
    parse_tpot(path)


if __name__ == "__main__":
    # execute only if run as a script
    main()
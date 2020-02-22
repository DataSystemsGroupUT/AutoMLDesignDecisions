import pandas as pd
import os
import ast

def parse_autoweka(directory):
    result = pd.DataFrame(columns=['autoweka_accuracy_mean', 'autoweka_f1_score_mean', 'autoweka_model_1',
                                   'autoweka_precision_mean', 'autoweka_recall_mean', 'autoweka_time_mean'])
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                sub_result = pd.read_csv(os.path.join(subdir, file), index_col=0)
                for col in sub_result.columns:
                    if col not in ['accuracy_mean', 'f1score_mean', 'model_1', 'precision_mean', 'recall_mean', 'time_mean']:
                        sub_result.drop(col, axis='columns', inplace=True)
                #sub_result = sub_result[['accuracy_mean', 'f1score_mean', 'model_1', 'precision_mean', 'recall_mean', 'time_mean']]
                sub_result.rename(columns={'accuracy_mean': 'autoweka_accuracy_mean',
                                       'f1score_mean': 'autoweka_f1_score_mean',
                                       'model_1': 'autoweka_model_1',
                                       'precision_mean': 'autoweka_precision_mean',
                                       'recall_mean': 'autoweka_recall_mean',
                                       'time_mean': 'autoweka_time_mean'}, inplace=True)
                #result = result.append(sub_result)
                result = pd.concat([result, sub_result], axis=0, sort=True)
    result.autoweka_model_1 = result.autoweka_model_1.apply(get_class)
    return result

def get_class (model):
    if isinstance(model, str):
        tmp = model.split('weka.classifiers.')[1]
        classifier = tmp.split('\n')[0]

        if classifier:
            return classifier
        else:
            return ''
    else:
        return ''



def main():
    path = r'C:\Users\HassanEldeeb\Desktop\Benchmark_Deliverables\Logs\Results10\autoweka'
    parse_autoweka(path)


if __name__ == "__main__":
    # execute only if run as a script
    main()
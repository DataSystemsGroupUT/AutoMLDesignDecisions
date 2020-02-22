import pandas as pd
import os
import ast
import numpy as np


def parse_sklearn_v(directory):
    result = pd.DataFrame(columns=['sklearn_v_accuracy_mean', 'sklearn_v_f1_score_mean', 'sklearn_v_model_1',
                                   'sklearn_v_precision_mean', 'sklearn_v_recall_mean', 'sklearn_v_time_mean'])
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                sub_result = pd.read_csv(os.path.join(subdir, file), index_col=0)
                for col in sub_result.columns:
                    if col not in ['accuracy_mean', 'f1score_mean', 'model_1', 'precision_mean', 'recall_mean', 'time_mean']:
                        sub_result.drop(col, axis='columns', inplace=True)
                # sub_result = sub_result[['accuracy_mean', 'f1score_mean', 'model_1', 'precision_mean', 'recall_mean', 'time_mean']]
                sub_result.rename(columns={'accuracy_mean': 'sklearn_v_accuracy_mean',
                                       'f1score_mean': 'sklearn_v_f1_score_mean',
                                       'model_1': 'sklearn_v_model_1',
                                       'precision_mean': 'sklearn_v_precision_mean',
                                       'recall_mean': 'sklearn_v_recall_mean',
                                       'time_mean': 'sklearn_v_time_mean'}, inplace=True)
                # result = result.append(sub_result)
                result = pd.concat([result, sub_result], axis=0, sort=True)
    result.sklearn_v_model_1 = result.sklearn_v_model_1.apply(get_class)
    return result


def parse_sklearn_m(directory):
    result = pd.DataFrame(columns=['sklearn_m_accuracy_mean', 'sklearn_m_f1_score_mean', 'sklearn_m_model_1',
                                   'sklearn_m_precision_mean', 'sklearn_m_recall_mean', 'sklearn_m_time_mean'])
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                sub_result = pd.read_csv(os.path.join(subdir, file), index_col=0)
                for col in sub_result.columns:
                    if col not in ['accuracy_mean', 'f1score_mean', 'model_1', 'precision_mean', 'recall_mean', 'time_mean']:
                        sub_result.drop(col, axis='columns', inplace=True)
                # sub_result = sub_result[['accuracy_mean', 'f1score_mean', 'model_1', 'precision_mean', 'recall_mean', 'time_mean']]
                sub_result.rename(columns={'accuracy_mean': 'sklearn_m_accuracy_mean',
                                       'f1score_mean': 'sklearn_m_f1_score_mean',
                                       'model_1': 'sklearn_m_model_1',
                                       'precision_mean': 'sklearn_m_precision_mean',
                                       'recall_mean': 'sklearn_m_recall_mean',
                                       'time_mean': 'sklearn_m_time_mean'}, inplace=True)
                # result = result.append(sub_result)
                result = pd.concat([result, sub_result], axis=0, sort=True)
    result.sklearn_m_model_1 = result.sklearn_m_model_1.apply(get_class)
    return result


def parse_sklearn_e(directory):
    result = pd.DataFrame(columns=['sklearn_e_accuracy_mean', 'sklearn_e_f1_score_mean', 'sklearn_e_model_1',
                                   'sklearn_e_precision_mean', 'sklearn_e_recall_mean', 'sklearn_e_time_mean'])
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                sub_result = pd.read_csv(os.path.join(subdir, file), index_col=0)
                for col in sub_result.columns:
                    if col not in ['accuracy_mean', 'f1score_mean', 'model_1', 'precision_mean', 'recall_mean', 'time_mean']:
                        sub_result.drop(col, axis='columns', inplace=True)
                # sub_result = sub_result[['accuracy_mean', 'f1score_mean', 'model_1', 'precision_mean', 'recall_mean', 'time_mean']]
                sub_result.rename(columns={'accuracy_mean': 'sklearn_e_accuracy_mean',
                                       'f1score_mean': 'sklearn_e_f1_score_mean',
                                       'model_1': 'sklearn_e_model_1',
                                       'precision_mean': 'sklearn_e_precision_mean',
                                       'recall_mean': 'sklearn_e_recall_mean',
                                       'time_mean': 'sklearn_e_time_mean'}, inplace=True)
                # result = result.append(sub_result)
                result = pd.concat([result, sub_result], axis=0, sort=True)
    result.sklearn_e_model_1 = result.sklearn_e_model_1.apply(get_class)
    return result


def parse_sklearn(directory):
    result = pd.DataFrame(columns=['sklearn_accuracy_mean', 'sklearn_f1_score_mean', 'sklearn_model_1',
                                   'sklearn_precision_mean', 'sklearn_recall_mean', 'sklearn_time_mean'])
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                sub_result = pd.read_csv(os.path.join(subdir, file), index_col=0)
                for col in sub_result.columns:
                    if col not in ['accuracy_mean', 'f1score_mean', 'model_1', 'precision_mean', 'recall_mean', 'time_mean']:
                        sub_result.drop(col, axis='columns', inplace=True)
                # sub_result = sub_result[['accuracy_mean', 'f1score_mean', 'model_1', 'precision_mean', 'recall_mean', 'time_mean']]
                sub_result.rename(columns={'accuracy_mean': 'sklearn_accuracy_mean',
                                       'f1score_mean': 'sklearn_f1_score_mean',
                                       'model_1': 'sklearn_model_1',
                                       'precision_mean': 'sklearn_precision_mean',
                                       'recall_mean': 'sklearn_recall_mean',
                                       'time_mean': 'sklearn_time_mean'}, inplace=True)
                # result = result.append(sub_result)
                result = pd.concat([result, sub_result], axis=0, sort=True)
    result.sklearn_model_1 = result.sklearn_model_1.apply(get_class)
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
    path = r'C:\Users\HassanEldeeb\Desktop\Benchmark_Deliverables\Logs\Results10\autosklearn'
    parse_sklearn(path)


if __name__ == "__main__":
    # execute only if run as a script
    main()
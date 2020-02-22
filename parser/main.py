from smartML_parser import parse_smartML
from sklearn_parser import parse_sklearn, parse_sklearn_v, parse_sklearn_e, parse_sklearn_m
from autoweka_parser import parse_autoweka
from tpot_parser import parse_tpot
from recipe_parser import parse_recipe
import os
import pandas as pd


def time_experiment(directory):
    tb_result_dict = {} # time budget result
    for filename in os.listdir(directory):
        if filename == 'smartml':
            tb_result_dict['smartml_result'] = parse_smartML(os.path.join(directory, filename))
        elif filename == 'autosklearn':
            tb_result_dict['skleran_result'] = parse_sklearn(os.path.join(directory, filename))
        elif filename == 'autosklearn_v':
            tb_result_dict['skleran_v_result'] = parse_sklearn_v(os.path.join(directory, filename))
        elif filename == 'autosklearn_e':
            tb_result_dict['skleran_e_result'] = parse_sklearn_e(os.path.join(directory, filename))
        elif filename == 'autosklearn_m':
            tb_result_dict['skleran_m_result'] = parse_sklearn_m(os.path.join(directory, filename))
        elif filename == 'autoweka':
            tb_result_dict['autoweka_result'] = parse_autoweka(os.path.join(directory, filename))
        elif filename == 'tpot':
            tb_result_dict['tpot_result'] = parse_tpot(os.path.join(directory, filename))
        elif filename == 'recipe':
            tb_result_dict['recipe_result'] = parse_recipe(os.path.join(directory, filename))
    return tb_result_dict


if __name__ == "__main__":
    # execute only if run as a script
    min = [r'10', r'30', r'60', r'4']
    for m in min:
        directory = r'C:\Users\HassanEldeeb\Documents\GitHub\AutoMLBenchmarking\Logs\Results' + m
        tb_result_dict = time_experiment(directory)
        tb_result_df = pd.DataFrame()
        for key in tb_result_dict.keys():
            #print(tb_result_df.shape, tb_result_dict[key].shape)
            tb_result_df = pd.concat([tb_result_df, tb_result_dict[key].loc[~tb_result_dict[key].index.duplicated()]], sort=True, axis= 1)
        tb_result_df.to_csv(os.path.join(directory, directory.split('\\')[-1] + '.csv'))
    print('Done!')
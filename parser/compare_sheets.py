import pandas as pd
import warnings
warnings.filterwarnings("ignore")

my_sheet = pd.read_excel(r'C:\Users\HassanEldeeb\Documents\GitHub\AutoMLBenchmarking\Complete_Sheet.xlsx', sheet_name=None)
old_sheet = pd.read_excel(r'C:\Users\HassanEldeeb\Documents\GitHub\AutoMLBenchmarking\AutoML Benchmarking Results.xlsx', sheet_name=None)

my_cols = ['autoweka_accuracy_mean', 'tpot_accuracy_mean', 'smartml_valid_acc', 'recipe_test_acc', 'sklearn_accuracy_mean', 'sklearn_v_accuracy_mean', 'sklearn_m_accuracy_mean', 'sklearn_e_accuracy_mean']
old_cols = ['AutoWeka', 'TPot', 'SmartML', 'Receipe', 'AutoSkLearn', 'AutoSkLearn - Vanilla', 'AutoSkLearn - Vanilla + MetaLearning', 'AutoSkLearn - Vanilla + Ensembling']

for min in ['10 Min', '30 Min', '60 Min', '4 Hours']:
    my_df = my_sheet[min]#.loc[my_sheet[min]['dataset'].str.lower().sort_values().index]
    old_df = old_sheet[min]#.loc[old_sheet[min]['Dataset'].str.lower().sort_values().index]
    #print("Correct Order") if my_df.dataset.equals(old_df.Dataset) else print("Shir in order")
    print("===================================", min, "===================================")
    for i in range(len(old_cols)):
        print("---------", old_cols[i], ":  ", min,  "---------")
        my_col = pd.to_numeric(my_df.loc[:, my_cols[i]], errors='coerce').fillna(0)
        old_col = pd.to_numeric(old_df.loc[:, old_cols[i]], errors='coerce').fillna(0)
        result = my_col - old_col
        out_df = pd.DataFrame({'old_dataset': old_df.Dataset.iloc[result.iloc[0:100].round(1).nonzero()],
                               'new_dataset': my_df.dataset.iloc[result.iloc[0:100].round(1).nonzero()],
                               'old_acc': old_col.iloc[result.iloc[0:100].round(1).nonzero()],
                               'new_acc': my_col.iloc[result.iloc[0:100].round(1).nonzero()],
                               'error': result.iloc[result.iloc[0:100].round(1).nonzero()]})
        #print(result.iloc[result.iloc[0:100].round(1).nonzero()])
        print(out_df.to_string())


print("Done!")
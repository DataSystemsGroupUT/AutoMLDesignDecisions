import pandas as pd

min = [r'10', r'30', r'60', r'4']
sheet_names = ['10 Min', '30 Min', '60 Min', '4 Hours']
writer = pd.ExcelWriter(r'C:\Users\HassanEldeeb\Documents\GitHub\AutoMLBenchmarking\Complete_Sheet.xlsx', engine='xlsxwriter')
for m, name in zip(min, sheet_names):
    result = pd.read_csv(r'C:\Users\HassanEldeeb\Documents\GitHub\AutoMLBenchmarking\Logs\Results' + m + r'\Results' + m + r'.csv')
    short_result = result.drop(['sklearn_model_1', 'sklearn_e_model_1', 'sklearn_v_model_1', 'sklearn_m_model_1', 'autoweka_model_1', 'tpot_model_1'], axis=1)
    short_result.rename(columns={'Unnamed: 0': 'dataset'}, inplace=True)
    short_result = short_result.loc[short_result['dataset'].str.lower().sort_values().index]
    short_result.to_csv(r'C:\Users\HassanEldeeb\Documents\GitHub\AutoMLBenchmarking\Logs\Results' + m + r'\Results' + m + r'_short.csv')
    short_result.to_excel(writer, sheet_name=name)
writer.save()
print('Done!')
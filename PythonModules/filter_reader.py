import os
import PythonModules.logger_finder as logger_finder
import PythonModules.progressBar as pgB

import pandas as pd

# reads filter file and outputs a reference file for other functions
def filter_reader():
    logger_df = pd.read_excel(logger_finder.get_logger())
    
    filter_df = pd.read_excel(logger_finder.file_finder('merge_file_filter'))
    filter_df = filter_df.dropna(axis = 1, how = 'all')
    filter_df = filter_df.columns.to_frame().T.append(filter_df, ignore_index=True)
    filter_df.columns = range(len(filter_df.columns))
    filter_df_list = filter_df.T.values.tolist()
    cleaned_filter_df_list = []
    for ind_list in filter_df_list:
        ind_list = [x for x in ind_list if str(x) != 'nan']
        cleaned_filter_df_list.append(ind_list)
    
    df_match = logger_df.copy()
    pgB.printProgressBar(0, len(cleaned_filter_df_list), prefix = 'Filter Progress:', suffix = 'Complete', length = 50)
    for i in range(len(cleaned_filter_df_list)):
        target_column = cleaned_filter_df_list[i][0]
        headless_col = cleaned_filter_df_list[i].copy()
        del headless_col[0]
        df_match = df_match[df_match[target_column].isin(headless_col)]
        pgB.printProgressBar(i+1, len(cleaned_filter_df_list), prefix = 'Filter Progress:', suffix = 'Complete', length = 50)
    
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + '\\'
    df_match.to_excel(desktop + 'filtered_logger_temp.xlsx')

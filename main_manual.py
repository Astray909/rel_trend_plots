import os
import shutil
import time

import PythonModules.graph_plotter as graph_plotter
import PythonModules.data_cleanup_pandas_sns as dcp
import PythonModules.logger_finder as logger_finder
import PythonModules.progressBar as pgB
import pandas as pd

from tkinter.filedialog import askopenfilename
from tkinter import messagebox

def filter_reader():
    logger_df = pd.read_excel(logger_finder.get_logger())
    messagebox.showinfo(title="Important message", message="Please select a filter file")
    filter_df = pd.read_excel(askopenfilename())
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

if __name__ == "__main__":
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + '\\'
    filter_reader()
    dcp.csv_merger(99, desktop + 'filtered_logger_temp.xlsx')
    if not os.path.exists(desktop + '\\REL_TREND_PLOTS'):
            os.makedirs(desktop + '\\REL_TREND_PLOTS')
    filenames = next(os.walk(desktop + '\\REL_TREND_PLOTS\\'), (None, None, []))[2]  # [] if no file
    filenames = [ x for x in filenames if ".png" in x ]

    if filenames:
        modTimesinceEpoc = os.path.getmtime(desktop + '\\REL_TREND_PLOTS\\' + filenames[0])
        arc_dir_name = '\\' + time.strftime('%Y_%m_%d_%H_%M', time.localtime(modTimesinceEpoc))

        if not os.path.exists(desktop + '\\REL_TREND_PLOTS\\Archived' + arc_dir_name):
            os.makedirs(desktop + '\\REL_TREND_PLOTS\\Archived' + arc_dir_name)

        for file in filenames:
            shutil.move(desktop + '\\REL_TREND_PLOTS\\' + file, desktop + '\\REL_TREND_PLOTS\\Archived' + arc_dir_name)
    inputcsv = str(desktop + 'csv_merge\\csv_merge_result.csv')
    graph_plotter.data_importer(inputcsv, True)
    messagebox.showinfo(title="Important message", message="Task Complete")

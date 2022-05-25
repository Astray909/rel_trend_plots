import os
import shutil
import time

import PythonModules.graph_plotter as graph_plotter
import PythonModules.data_cleanup_pandas_sns as dcp
import PythonModules.filter_reader as filter_reader

if __name__ == "__main__":
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + '\\'
    filter_reader.filter_reader()
    dcp.csv_merger(99, desktop + 'filtered_logger_temp.xlsx')
    filenames = next(os.walk('X:\\PLC\\Prod Docs\\Qual\\qrw_script\\Rel Trend Charts\\'), (None, None, []))[2]  # [] if no file
    filenames = [ x for x in filenames if ".png" in x ]

    if filenames:
        modTimesinceEpoc = os.path.getmtime('X:\\PLC\\Prod Docs\\Qual\\qrw_script\\Rel Trend Charts\\' + filenames[0])
        arc_dir_name = '\\' + time.strftime('%Y_%m_%d_%H_%M', time.localtime(modTimesinceEpoc))

        if not os.path.exists('X:\\PLC\\Prod Docs\\Qual\\qrw_script\\Rel Trend Charts\\Archived' + arc_dir_name):
            os.makedirs('X:\\PLC\\Prod Docs\\Qual\\qrw_script\\Rel Trend Charts\\Archived' + arc_dir_name)

        for file in filenames:
            shutil.move('X:\\PLC\\Prod Docs\\Qual\\qrw_script\\Rel Trend Charts\\' + file, 'X:\\PLC\\Prod Docs\\Qual\\qrw_script\\Rel Trend Charts\\Archived' + arc_dir_name)
    inputcsv = str(desktop + 'csv_merge\\csv_merge_result.csv')
    graph_plotter.data_importer(inputcsv, False, [])

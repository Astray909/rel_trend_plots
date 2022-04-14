import glob
import os
import re
import pandas as pd
import seaborn as sns
import matplotlib.ticker as mtick

from matplotlib import pyplot as plt

import PythonModules.progressBar as pgB
import PythonModules.logger_finder as logger_finder

from tkinter.filedialog import askopenfilename

def data_importer(inputcsv):
    inputdf = pd.read_csv(inputcsv)
    # print(inputdf)

    ori_path = os.getcwd()
    path = 'X://PLC//Prod Docs//Qual//qrw_script//'
    extension = "xlsm"
    os.chdir(path)
    all_xlsx_files = glob.glob('*.{}'.format(extension))
    return_arr = []
    for xlsx_file in all_xlsx_files:
        if str('test_initiator') in xlsx_file and '~$' not in xlsx_file:
            return_arr.append(xlsx_file)
    return_arr = ntSort(return_arr)
    return_path = path + return_arr[-1]
    os.chdir(ori_path)
    limits_path = return_path
    
    initiator = limits_path
    initiator_df = pd.read_excel(initiator, sheet_name = 'product_id')
    
    result_df_list = []
    test_type_list = inputdf['Rel Test'].tolist()
    # volt_type_list = [str(vinttost) for vinttost in inputdf['Voltage (V)'].tolist()]
    result_df_master = inputdf.loc[(inputdf['Test Hours_Cycles'] == 1000)]

    filter_df = pd.read_excel(logger_finder.file_finder('merge_file_filter'))
    logger_df = pd.read_excel(logger_finder.get_logger())

    filter_df = filter_df.dropna(axis = 1, how = 'all')
    filter_df_columns = filter_df.columns.tolist()
    filter_df_columns.remove('Test')
    filter_df_columns.remove('Product')
    
    pd.options.mode.chained_assignment = None  # default='warn'
    for index, row in result_df_master.iterrows():
        for filter_df_col in filter_df_columns:
            target_row = logger_df.loc[(logger_df['UID'] == row['UID'])]
            target_info = str(target_row.loc[:,filter_df_col].iloc[0])
            result_df_master.loc[index,filter_df_col] = target_info
    pd.options.mode.chained_assignment = 'warn'  # default='warn'
    
    
    for test, df_test in result_df_master.groupby('Rel Test'):
        for volt, df_volt in df_test.groupby(filter_df_columns):
            result_df_list.append(df_volt)

    for result_df in result_df_list:
        result_df_test = str(list(dict.fromkeys(result_df.loc[:,'Rel Test'].tolist()))[0])
        # result_df_volt = str(list(dict.fromkeys(result_df.loc[:,'Voltage (V)'].tolist()))[0])
        result_df_conds = []
        result_df_conds.append(result_df_test)
        for filter_df_col_2 in filter_df_columns:
            cond = str(list(dict.fromkeys(result_df.loc[:,filter_df_col_2].tolist()))[0])
            result_df_conds.append(cond)
        
        joined_name = '_'.join(result_df_conds)
        print(joined_name)

        result_datecodes_list = result_df['YYWW_datecode'].tolist()
        result_datecodes_list = list(dict.fromkeys(result_datecodes_list))
        
        product_id_list = []
        series_id_list = []
        part_list = result_df['product'].tolist()
        for part in part_list:
            part_result_df = initiator_df.loc[(initiator_df['product'] == part)]
            prod_id = part_result_df['die']
            series_id = part_result_df['series']
            product_id_list.append(prod_id.to_string(index=False))
            series_id_list.append(series_id.to_string(index=False))

        product_id_list_cleaned = ntSort(list(dict.fromkeys(product_id_list)))
        product_id_list_len = len(product_id_list)
        series_id_list_cleaned = ntSort(list(dict.fromkeys(series_id_list)))
        series_id_list_len = len(series_id_list)

        pd.options.mode.chained_assignment = None  # default='warn'
        result_df.loc[:,"die"] = product_id_list
        result_df.loc[:,"series"] = series_id_list
        pd.options.mode.chained_assignment = 'warn'  # default='warn'

        # id_list_cleaned = product_id_list_cleaned + series_id_list_cleaned
        id_list_cleaned = series_id_list_cleaned

        df_list = []
        # for region, df_region in result_df.groupby('die'):
        #     df_list.append(df_region)
        for region_2, df_region_2 in result_df.groupby('series'):
            df_list.append(df_region_2)

        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

        columns_arr = ['Rdson_aging(%)','Vth_aging(%)','Igss_rise(x)','Idoff_rise(x)']
        for c in columns_arr:
            pgB.printProgressBar(0, len(df_list), prefix =  c + 'Graphs Progress:', suffix = 'Complete', length = 50)
            for i in range(len(df_list)):
                df_TEMP = df_list[i].copy()
                df_TEMP = df_TEMP.sort_values(by = ['YYWW_datecode'])
                if c == 'Rdson_aging(%)' or c == 'Vth_aging(%)':
                    df_TEMP.loc[:,c] = df_TEMP.loc[:,c] * 100
                i_no_number = ''.join([ii for ii in str(i) if not ii.isdigit()])
                plt_filename = 'plt_' + joined_name + '_' + str(id_list_cleaned[i]) + '_' + str(i_no_number) + str(c)
                plt.figure(figsize=(20, 6))
                sns.set_theme(style="whitegrid")
                plotname = 'plt_' + joined_name + '_' + str(i)
                plotname = sns.boxplot(x="YYWW_datecode", y=c, data=df_TEMP, width=0.5)
                plotname.set_title(joined_name + '_' + str(id_list_cleaned[i]))
                plotname.set_xticklabels(plotname.get_xticklabels(),rotation = 30)
                if c == 'Igss_rise(x)' or c == 'Idoff_rise(x)':
                    plt.ylim(0, 50)
                    outlier_df_lower = df_list[i][(df_list[i][c] < 0)]
                    outlier_df_higher = df_list[i][(df_list[i][c] > 50)]
                    outlier_df = pd.concat([outlier_df_lower, outlier_df_higher])
                    outlier_df = outlier_df[['YYWW_datecode','device', c]]
                    if outlier_df.empty == False:
                        decimals = 2    
                        outlier_df[c] = outlier_df[c].apply(lambda x: round(x, decimals))
                        plt.table(cellText=outlier_df.values,colWidths = [0.08]*len(outlier_df.columns),
                        rowLabels=outlier_df.index,
                        colLabels=outlier_df.columns,
                        cellLoc = 'center', rowLoc = 'center',
                        loc='best')
                elif c == 'Rdson_aging(%)':
                    plt.ylim(-50, 150)
                    plotname.yaxis.set_major_formatter(mtick.PercentFormatter())
                    outlier_df_lower = df_list[i][(df_list[i][c] < -0.5)]
                    outlier_df_higher = df_list[i][(df_list[i][c] > 1.5)]
                    outlier_df = pd.concat([outlier_df_lower, outlier_df_higher])
                    outlier_df = outlier_df[['YYWW_datecode','device', c]]
                    if outlier_df.empty == False:
                        decimals = 2    
                        outlier_df[c] = outlier_df[c].apply(lambda x: round(x, decimals))
                        plt.table(cellText=outlier_df.values,colWidths = [0.08]*len(outlier_df.columns),
                        rowLabels=outlier_df.index,
                        colLabels=outlier_df.columns,
                        cellLoc = 'center', rowLoc = 'center',
                        loc='best')
                elif c == 'Vth_aging(%)':
                    plt.ylim(-50, 50)
                    plotname.yaxis.set_major_formatter(mtick.PercentFormatter())
                    outlier_df_lower = df_list[i][(df_list[i][c] < -0.5)]
                    outlier_df_higher = df_list[i][(df_list[i][c] > 0.5)]
                    outlier_df = pd.concat([outlier_df_lower, outlier_df_higher])
                    outlier_df = outlier_df[['YYWW_datecode','device', c]]
                    if outlier_df.empty == False:
                        decimals = 2    
                        outlier_df[c] = outlier_df[c].apply(lambda x: round(x, decimals))
                        plt.table(cellText=outlier_df.values,colWidths = [0.08]*len(outlier_df.columns),
                        rowLabels=outlier_df.index,
                        colLabels=outlier_df.columns,
                        cellLoc = 'center', rowLoc = 'center',
                        loc='best')
                # plt.show()
                plt.savefig('X:\\PLC\\Prod Docs\\Qual\\qrw_script\\Rel Trend Charts\\' + plt_filename + '.png')
                plt.close()
                pgB.printProgressBar(i + 1, len(df_list), prefix =  c + 'Graphs Progress:', suffix = 'Complete', length = 50)

#natural sort
def ntSort(input): 
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(input, key = alphanum_key)

if __name__ == "__main__":
    inputcsv = askopenfilename()
    data_importer(inputcsv)

#merges all csvs into 1 large csv
import glob
import os
import re
import time
import traceback

from tkinter.filedialog import askopenfilename

import numpy as np
import pandas as pd

import PythonModules.logger_finder as logger_finder
import PythonModules.progressBar as pgB

retest_keywords=['retest','re-test','rt']

def csv_merger(mode,*target_init):
    column_header_rearr = ['Off-Idl','Off-Idl_check']
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + '\\'
    # logger_df = pd.read_excel('X:\\PLC\\Prod Docs\\Qual\\qrw_script\\test_logger_v02.xlsx')
    logger_df = pd.read_excel(logger_finder.get_logger()) #logger file as df
    ori_dir = os.getcwd() #original processing directory
    target_folders_arr = []
    csv_arr = []
    if mode != 99:
        target = askopenfilename()
    elif mode == 99:
        target = target_init[0]
        mode = 0
    print(target)
    reference_df = pd.read_excel(target)
    uid_series = (reference_df['UID'])
    dir = 'X:\\PLC\\Prod Docs\\Qual\\qrw'
    # dir = desktop + 'qrw_column_header_test'
    subdirs = [dI for dI in os.listdir(dir) if os.path.isdir(os.path.join(dir,dI))]
    subdirs_new = [dir + '\\' + x for x in subdirs]

    for uid in uid_series:
        for iterator in subdirs_new:
            if uid in iterator:
                target_folders_arr.append(iterator)

    # check folder integrity and skip ones with missing folders
    problem_lots = folder_inte_check(target_folders_arr)
    problem_lots_df = pd.DataFrame(problem_lots,columns=['Lot','reason'])
    if mode != 66:
        problem_lots_df.to_excel('X:\\PLC\\Prod Docs\\Qual\\qrw_script\\dataAnalysis\\csv_merge_skipped.xlsx')
    else:
        problem_lots_df.to_excel('X:\\PLC\\Prod Docs\\Qual\\qrw_script\\dataAnalysis\\interval_test_errors\\skipped.xlsx')
    for i in range(len(problem_lots)):
        target_folders_arr.remove(problem_lots[i][0])

    target_folders_arr_x = target_folders_arr
        
    # change source dir based on mode
    if mode == 0:
        target_folders_arr = [x + '\\2_processed_data' for x in target_folders_arr]
    elif mode == 1:
        target_folders_arr = [x + '\\2_processed_data\\AZUREFORMAT\\' for x in target_folders_arr]
    subdirs_new_replaced = [x.replace("\\", "/") for x in target_folders_arr_x]
    
    extension = 'csv'
    for target_folder in target_folders_arr:
        try:
            os.chdir(target_folder)
            local_result = glob.glob('*.{}'.format(extension))
            local_result = ntSort(local_result)
            for i in range(len(local_result)):
                local_result[i] = target_folder + '\\' + local_result[i]
            for local_result_i in local_result:
                if 'global' not in local_result_i:
                    csv_arr.append(local_result_i)
        except Exception as E:
            full_exception = traceback.format_exc()
            current_time = time.strftime(r"%d_%m_%H_%M_%S", time.localtime())
            print('Error encountered' + str(full_exception))
            f = open("X:\\PLC\\Prod Docs\\Qual\\qrw_script\\dataAnalysis\\Errors\\csv_merge_errors.txt","a+")
            f.write("\n" + current_time + str(full_exception) + '\n')
            f.close()
            pass

    os.chdir(ori_dir)
    df_arr = []
    pgB.printProgressBar(0, len(csv_arr), prefix = 'Merge Progress:', suffix = 'Complete', length = 50)
    for i in range(len(csv_arr)):
        try:
            # print(csv_arr[i])
            for uid in uid_series:
                if uid in csv_arr[i]:
                    test_uid = uid
            index = int((np.where(logger_df["UID"] == test_uid))[0])
            info_df = logger_df.loc[[index]]
            info_df = info_df.fillna('')
            product_code = info_df['Product'].astype(str).iloc[0]
            date_code = info_df['Date Code'].astype(str).iloc[0]
            yw_code = date_code[:2]
            valid_date_code = False
            try:
                y_code = int(re.search("\d+", yw_code)[0])
                valid_date_code = True
                w_code = yw_code.replace(str(y_code),'')
                w_number = ord(w_code) - 64
                y_index = yw_code.index(str(y_code))
                if y_index == 0:
                    ww = w_number
                else:
                    ww = w_number + 26
                yy = '2' + str(y_code)
                if y_code == 7 or y_code == 8 or y_code == 9:
                    yy = '1' + str(y_code)
                if len(str(ww)) == 1:
                    ww = '0' + str(ww)
            except:
                y_code = 9
                valid_date_code = False
            
            if valid_date_code:
                yyww_datecode = yy + str(ww) + '_' + date_code
            else:
                yyww_datecode = 'Date Code Not Available'
            if date_code.isnumeric():
                yyww_datecode = str(date_code) + '_' + date_code
            test_type = info_df['Test'].astype(str).iloc[0]
            volt_type = info_df['Voltage (V)'].astype(str).iloc[0]
            csv_file_name = (get_info(csv_arr[i], '\\'))[-1]
            time_code = (get_info(csv_file_name, '_'))[3]
            time_code = time_code.replace('T','')
            data_df = pd.read_csv(csv_arr[i])
            try:
                data_df = data_df.drop('Off-Idl_check|MaxIdss@LowV at V STEP|uA', 1)
            except:
                pass

            is_retest = 'NO'
            csv_info_lower = get_info(csv_file_name.lower(), '_')
            if len(list(set(csv_info_lower).intersection(retest_keywords))) > 0:
                is_retest = 'YES'

            if mode == 0:
                meta_df_temp = pd.DataFrame([[test_uid,product_code,date_code,yyww_datecode,test_type,csv_file_name,time_code]], columns=['UID','product','date code','YYWW_datecode','Rel Test','csv file name','Test Hours_Cycles'])
            if mode == 1:
                meta_df_temp = pd.DataFrame([[test_uid,csv_file_name,time_code,is_retest,yyww_datecode]], columns=['UID','csv file name','Test Hours_Cycles','retest','YYWW_datecode'])
            meta_df = pd.concat([meta_df_temp]*len(data_df.index), ignore_index=True)
            final_df = pd.concat([meta_df, data_df], axis=1)
            df_arr.append(final_df)
        except Exception as E:
            full_exception = traceback.format_exc()
            current_time = time.strftime(r"%d_%m_%H_%M_%S", time.localtime())
            print('Error encountered' + str(full_exception))
            f = open("X:\\PLC\\Prod Docs\\Qual\\qrw_script\\dataAnalysis\\Errors\\csv_merge_errors.txt","a+")
            f.write("\n" + current_time + str(full_exception) + '\n')
            f.close()
            pass
        pgB.printProgressBar(i + 1, len(csv_arr), prefix = 'Merge Progress:', suffix = 'Complete', length = 50)


    try:
        os.mkdir(desktop + 'csv_merge\\')
    except Exception as e:
        print(e)
        pass
    
    return_df = pd.concat(df_arr)

    header_need_rearr = []
    header_need_rearr_check = []
    original_index = []
    original_index_check = []
    return_df_column = return_df.columns.tolist()
    # rearrange OffId columns
    for i in range(len(return_df_column)):
        if 'OffId' in return_df_column[i]:
            original_index.append(i)
            header_need_rearr.append(return_df_column[i])
    for i in range(len(return_df_column)):
        if 'OffIdChk' in return_df_column[i]:
            header_need_rearr_check.append(return_df_column[i])
    header_need_rearr = list(dict.fromkeys(header_need_rearr))
    header_need_rearr = ntSort(header_need_rearr)
    header_need_rearr_check = list(dict.fromkeys(header_need_rearr_check))
    header_need_rearr_check = ntSort(header_need_rearr_check)
    for header_need in header_need_rearr:
        return_df_column.remove(header_need)
    for i in range(len(header_need_rearr)):
        return_df_column.insert(original_index[0]+i, header_need_rearr[i])
    for header_need in header_need_rearr_check:
        return_df_column.remove(header_need)
    for i in range(len(return_df_column)):
        if 'DeltaIrglChk' in return_df_column[i]:
            original_index_check.append(i)
    for i in range(len(header_need_rearr_check)):
        return_df_column.insert(original_index_check[0]+i, header_need_rearr_check[i])

    if 'KVth|SAME| ' in return_df_column and 'KIGS|SAME|m ' in return_df_column:
        index_kth = return_df_column.index('KVth|SAME| ')
        index_kigs = return_df_column.index('KIGS|SAME|m ')
        return_df_column.insert(index_kth + 1, return_df_column.pop(index_kigs))

    return_df = return_df[return_df_column]
    delay_columns = []
    for i in range(len(return_df_column)):
        if 'Delay' in return_df_column[i]:
            delay_columns.append(return_df_column[i])
    for i in range(len(delay_columns)):
        try:
            return_df = return_df.drop(delay_columns[i], 1)
        except:
            pass

    return_df.to_csv(desktop + 'csv_merge\\csv_merge_result.csv',index=False)

    if mode == 0:
        add_shifts_columns(desktop)

    open_path = desktop + 'csv_merge\\'
    open_path = os.path.realpath(open_path)
    # os.startfile(open_path)

    return

# checks integrity of folders for missing folders
def folder_inte_check(target):
    prob_lots = []
    pgB.printProgressBar(0, len(target), prefix = 'Folder Integrity Check Progress:', suffix = 'Complete', length = 50)
    for i in range(len(target)):
        # print(target[i])
        output = [dI for dI in os.listdir(target[i]) if os.path.isdir(os.path.join(target[i],dI))]
        if '1_raw_data' not in output or '2_processed_data' not in output or '6_paperwork' not in output:
            prob_lots.append((target[i],'Missing Folder(s)'))
        elif '1_raw_data' in output:
            output_2 = [dI for dI in os.listdir(target[i] + '\\1_raw_data') if os.path.isdir(os.path.join(target[i] + '\\1_raw_data' ,dI))]
            if '1_interval' not in output_2:
                prob_lots.append((target[i],'Missing Folder(s)'))
            elif '1_interval' in output_2:
                output_3 = [dI for dI in os.listdir(target[i] + '\\1_raw_data\\1_interval') if os.path.isdir(os.path.join(target[i] + '\\1_raw_data\\1_interval' ,dI))]
                try:
                    csv_files = csvgetter(target[i] + '\\1_raw_data\\1_interval\\' + output_3[0],True)
                    try:
                        if 'T0' not in csv_files[0]:
                            if 'msl' not in csv_files[0].lower():
                                prob_lots.append((target[i],'Missing T0/MSL3'))
                    except:
                        prob_lots.append((target[i],'Empty T0 Folder'))
                        pass
                except:
                    prob_lots.append((target[i],'Missing Folders in 1_interval'))
                    pass
        pgB.printProgressBar(i+1, len(target), prefix = 'Folder Integrity Check Progress:', suffix = 'Complete', length = 50)
    return prob_lots

#natural sort
def ntSort(input): 
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(input, key = alphanum_key)

#seperates words from a formatted long string
def get_info(word,seperator):
    word = word
    words = []
    words = word.split(seperator)

    return words

# parametric shifts calculation
def add_shifts_columns(desktop):
    calc_arr = []
    init_df = pd.read_csv(desktop + 'csv_merge\\csv_merge_result.csv')
    pgB.printProgressBar(0, len(init_df.index), prefix = 'Shift Column Progress:', suffix = 'Complete', length = 50)
    for index, row in init_df.iterrows():
        rdson_self = row['rdson/mOhms']
        vth_self = row['vth/V']
        igs_self = row['igs/uA']
        idoff_self = row['idoff/uA']

        if rdson_self == 'inf':
            rdson_self = 999999999
        if vth_self == 'inf':
            vth_self = 999999999
        if igs_self == 'inf':
            igs_self = 999999999
        if idoff_self == 'inf':
            idoff_self = 999999999
        
        # locate same device and uid if time != 0
        if row['Test Hours_Cycles'] == 0:
            try:
                calc_arr.append([(rdson_self/rdson_self - 1), (vth_self/vth_self - 1), (igs_self/igs_self), (idoff_self/idoff_self)])
            except:
                calc_arr.append(['N/A','N/A','N/A','N/A'])
        else:
            row_uid = row['UID']
            row_date = row['date code']
            row_test = row['Rel Test']
            row_device_no = row['device']
            result_df = init_df.loc[(init_df['UID'] == row_uid) & (init_df['date code'] == row_date) & (init_df['Rel Test'] == row_test) & (init_df['device'] == row_device_no) & (init_df['Test Hours_Cycles'] == 0)]
            try:
                rdson_self_sub = result_df['rdson/mOhms'].values[0]
                vth_self_sub = result_df['vth/V'].values[0]
                igs_self_sub = result_df['igs/uA'].values[0]
                idoff_self_sub = result_df['idoff/uA'].values[0]
                calc_arr.append([(rdson_self/rdson_self_sub - 1), (vth_self/vth_self_sub - 1), (igs_self/igs_self_sub), (idoff_self/idoff_self_sub)])
            except:
                calc_arr.append(['N/A','N/A','N/A','N/A'])
        pgB.printProgressBar(index + 1, len(init_df.index), prefix = 'Shift Column Progress:', suffix = 'Complete', length = 50)
    return_df = pd.DataFrame(calc_arr, columns=['Rdson_aging(%)','Vth_aging(%)','Igss_rise(x)','Idoff_rise(x)'])
    final_df = pd.concat([init_df, return_df], axis=1)
    final_df.to_csv(desktop + 'csv_merge\\csv_merge_result.csv',index=False)
    return

# gets correct raw data csv files
def csvgetter(dir, retest):
    open_path = dir
    output_arr = []
    extension = 'csv'
    os.chdir(open_path)
    result = glob.glob('*.{}'.format(extension))
    is_FTI = True
    for item in result:
        if 'String' in item:
            is_FTI = False
    # for keathley files: only take ones with 'String' in first index
    if is_FTI:
        for i in range(len(result)):
            testforretest = result[i].lower()
            testforretest = get_info (testforretest, '_')
            if retest:
                output_arr.append(result[i])
            else:
                if len(list(set(testforretest).intersection(retest_keywords))) > 0:
                    pass
                else:
                    output_arr.append(result[i])
    else:
        for i in range(len(result)):
            testforretest = result[i].lower()
            testforretest = get_info (testforretest, '_')
            if 'String' in result[i]:
                if retest:
                    output_arr.append(result[i])
                else:
                    if len(list(set(testforretest).intersection(retest_keywords))) > 0:
                        pass
                    else:
                        output_arr.append(result[i])
            else:
                pass
    return ntSort(output_arr)
    
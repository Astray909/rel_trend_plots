# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 2021

@author: Justin Huang
"""

import os
import glob
import re


def file_finder(filename_keywords):
    ori_path = os.getcwd()
    path = 'X://PLC//Prod Docs//Qual//qrw_script//'
    extension = "xlsx"
    os.chdir(path)
    all_xlsx_files = glob.glob('*.{}'.format(extension))
    return_arr = []
    for xlsx_file in all_xlsx_files:
        if str(filename_keywords) in xlsx_file and '~$' not in xlsx_file:
            return_arr.append(xlsx_file)
    return_arr = ntSort(return_arr)
    return_path = path + return_arr[-1]
    os.chdir(ori_path)
    return return_path

#get the latest version of logger file
def get_logger():
    return_path = file_finder('test_logger')
    return return_path

def get_event_logger():
    return_path = file_finder('test_event_logger')
    return return_path

def unified_header_finder():
    return_path = file_finder('Unified_Headers_Lookup')
    return return_path

#seperates words from a formatted long string
def get_info(word,seperator):
    word = word
    words = []
    words = word.split(seperator)

    return words

#natural sort
def ntSort(input): 
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(input, key = alphanum_key)

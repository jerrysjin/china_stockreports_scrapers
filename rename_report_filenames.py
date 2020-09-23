#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import re
import shutil
import glob
import argparse


parser = argparse.ArgumentParser()
parser.add_argument(
    '--root_dir',
    help = 'root dir for all report files',
    type = str,
    required = True
)
parser.add_argument(
    '--code_file',
    help = 'file containing all ticker code',
    type = str,
    required = True
)
parser.add_argument(
    '--output_dir',
    help = 'output dir',
    type = str,
    required = True
)
args = parser.parse_args()


def filter_filename(filename):
    invalid_words = [
        '取消',
        '英文'
    ]
    
    for word in invalid_words:
        if word in filename:
            return False
    return True


def rename_filename(ticker, filename):
    report_year = re.search(r'\d+', filename)[0]
    
    report_type = 'AN'
    if '一季' in filename:
        report_type = 'Q1'
    if '三季' in filename:
        report_type = 'Q3'
    if '半年' in filename:
        report_type = 'SA'
    
    report_tag = 'Full'
    if '摘要' in filename:
        report_tag = 'Abstract'
    if '正文' in filename:
        report_tag = 'Main'
    if '补充' in filename:
        report_tag = 'Suppl'
    
    return '_'.join([ticker, report_year, report_type, report_tag]) + '.pdf'


if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)

with open(args.code_file, 'r') as codes:
    code_list = []
    for line in codes:
        code_list.append(line.strip().split('.')[0])

for code in code_list:
    code_dir = os.path.join(args.output_dir, code)
    if not os.path.exists(code_dir):
        os.makedirs(code_dir)
    
    for filepath in glob.glob('{}/{}/*'.format(args.root_dir, code)):
        filename = filepath.split('/')[-1]
        if not filter_filename(filename):
            continue
        
        try:
            new_filename = rename_filename(code, filename)
            new_filepath = os.path.join(code_dir, new_filename)
        
            shutil.copy2(filepath, new_filepath)
        except:
            pass

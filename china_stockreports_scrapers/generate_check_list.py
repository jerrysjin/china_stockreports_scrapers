#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import argparse
import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument('--input', help = 'input report dir', required = True)
parser.add_argument('--code_file', help = 'code list file', required = True)
parser.add_argument('--output', help = 'output dest file', required = True)
args = parser.parse_args()

code_list = []
with open(args.code_file, 'r') as codes:
    for line in codes:
        code_list.append(line.strip().split('.')[0])

codes, years, types, tags = [], [], [], []

for code in code_list:
    code_dir = os.path.join(args.input, code)
    for filename in sorted(os.listdir(code_dir)):
        namestr = filename.split('.')[0]
        tk, yr, tp, tg = namestr.split('_')
        codes.append(tk)
        years.append(yr)
        types.append(tp)
        tags.append(tg)

df = pd.DataFrame({'Code': codes, 'Year': years, 'Type': types, 'Tags': tags})
df.to_csv(args.output, index = False)

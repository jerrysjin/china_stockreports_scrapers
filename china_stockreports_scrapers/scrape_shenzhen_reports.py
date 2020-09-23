#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime
import time
from szreport_scraper import SZReportScraper

# adjust begin date and end date here
begin_date = '2000-01-01'
end_date = '2020-09-08'

sz_scraper = SZReportScraper(['010301', '010303', '010305', '010307'])

with open('shenzhen_code', 'r') as shenzhen_code:
    code_list = []
    for line in shenzhen_code:
        code_list.append(line.strip().split('.')[0])

save_path = 'downloads/shenzhen'
if not os.path.exists(save_path):
    os.makedirs(save_path)

for code in code_list:
    start_time = datetime.now()
    print('= start scraping reports for {}'.format(code), flush = True)
    
    flag = False
    while not flag:
        try:
            sz_scraper.download(code, save_path, begin_date, end_date)
            flag = True
        except:
            print(' - exception; pause for 10 secs')
            time.sleep(10)
            pass
    
    end_time = datetime.now()
    print(' - elapsed time for scraping {}: {}'.format(code, end_time - start_time), flush = True)

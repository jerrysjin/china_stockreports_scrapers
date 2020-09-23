#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
import grequests
import requests
import datetime
import json
from pathlib import Path
import time
import warnings
warnings.filterwarnings('ignore')


class SHReportScraper(object):
    def __init__(self, cookies):
        self.cookies = cookies
    
    def _date_ranges(self, begin_date, end_date):
        begin_obj = datetime.datetime.strptime(begin_date, '%Y-%m-%d')
        end_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        interval = datetime.timedelta(days = 900)
        dates = [begin_obj.strftime('%Y-%m-%d')]
        date_obj = begin_obj
        
        while True:
            if (date_obj < end_obj) & (date_obj + interval < end_obj):
                date_obj = date_obj + interval
                dates.append(date_obj.strftime('%Y-%m-%d'))
            else:
                dates.append(end_obj.strftime('%Y-%m-%d'))
                break
        
        return [(d1, d2) for d1, d2 in zip(dates, dates[1:])]
    
    def pdfurls(self, code, begin_date, end_date):
        urls, filenames = [], []
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'Referer': 'http://www.sse.com.cn/disclosure/listedinfo/regular/'
        }
        
        base = 'http://query.sse.com.cn/security/stock/queryCompanyBulletin.do?isPagination=true&productId={code}&keyWord=&securityType=0101%2C120100%2C020100%2C020200%2C120200&reportType2=DQBG&reportType=ALL&beginDate={beginDate}&endDate={endDate}&pageHelp.pageSize=25&pageHelp.pageCount=50&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.cacheSize=1&pageHelp.endPage=5'
        date_ranges = self._date_ranges(begin_date, end_date)
        
        for begin, end in date_ranges:
            flag, retries = True, 0
            while flag:
                try:
                    retries += 1
                    url = base.format(code = code, beginDate = begin, endDate = end)
                    resp = requests.get(url, headers = headers, cookies = self.cookies, timeout = 10)
                    print(' - trying to retrieve pdf urls for date range [{}, {}]'.format(begin, end))
                    raw_data = json.loads(resp.text)
                    results = raw_data['result']
                    for result in results:
                        try:
                            url = 'http://www.sse.com.cn' + result['URL']
                            urls.append(url)
                            pdfname = result['BULLETIN_YEAR'] + '-' + result['TITLE']
                            if not pdfname.lower().endswith('.pdf'):
                                pdfname = pdfname + '.pdf'
                            filenames.append(pdfname)
                        except:
                            print(result)
                            pass
                    flag = False
                except:
                    if retries > 3:
                        flag = False
                    else:
                        time.sleep(5)
                        pass
        
        return urls, filenames
    
    def download(self, code, savepath, begin_date, end_date):
        path = Path(savepath).joinpath(code)
        Path(path).mkdir(parents = True, exist_ok = True)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'Referer': 'http://www.sse.com.cn/disclosure/listedinfo/regular/'
        }
        
        urls, filenames = self.pdfurls(code, begin_date, end_date)
        print(' - fetched pdf urls for {}'.format(code), flush = True)
        
        print(' - start downloading pdf reports', flush = True)
        tasks = [grequests.request('GET', url = url, headers = headers, cookies = self.cookies, timeout = 10) for url in urls]
        results = grequests.map(tasks)
        
        for result, pdfname, url in zip(results, filenames, urls):
            try:
                pdfpath = path.joinpath(pdfname)
                
                with open(pdfpath, 'wb') as f:
                    f.write(result.content)
                    print('  - downloaded {}'.format(pdfname), flush = True)
            
            except Exception as e:
                print('  - [X]fail to download {}'.format(pdfname), flush = True)
                
                flag, retries = True, 0
                while flag:
                    try:
                        retries += 1
                        resp = requests.get(url, headers = headers, timeout = 10)
                        with open(pdfpath, 'wb') as f:
                            f.write(resp.content)
                            print('  - downloaded {}'.format(pdfname), flush = True)
                        flag = False
                    except:
                        if retries > 3:
                            raise e
                        else:
                            time.sleep(1)
                            pass

#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
import grequests
import requests
import urllib.request
import urllib.parse
import datetime
import json
import time
from pathlib import Path


class SZReportScraper(object):
    def __init__(self, report_types = ['010301', '010303', '010305', '010307']):
        self.report_types = report_types
    
    def pdfurls(self, code, begin_date, end_date):
        urls, filenames = [], []
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'HOST': 'www.szse.cn',
            'Origin': 'http://www.szse.cn',
            'Referer': 'http://www.szse.cn/disclosure/listed/notice/index.html',
            'X-Request-Type': 'ajax',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        base = 'http://www.szse.cn/api/disc/announcement/annList?random=0.9794648678933643'
        
        file_url = "http://disc.static.szse.cn/download"
        
        page_no = 1
        total_page_num = 1
        
        while page_no <= total_page_num:
            request_payload = {
                'seDate': [begin_date, end_date],
                'stock': [code],
                'channelCode': ['listedNotice_disc'],
                'bigCategoryId': self.report_types,
                'pageSize': 30,
                'pageNum': page_no
            }
            
            request = urllib.request.Request(url = base, headers = headers)
            form_data = json.dumps(request_payload).encode()
            response = urllib.request.urlopen(request, form_data)
            time.sleep(0.1)
            res_list = response.read().decode()
            res = json.loads(res_list)
            
            total = res['announceCount']
            total_page_num = total / 30 + 1
            page_no += 1
            
            for item in res['data']:
                urls.append(file_url + item['attachPath'])
                pdfname = item['title']
                if not pdfname.lower().endswith('.pdf'):
                    pdfname = pdfname + '.pdf'
                filenames.append(pdfname)
        
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
        tasks = [grequests.request('GET', url = url, headers = headers) for url in urls]
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
                        resp = requests.get(url, headers = headers)
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

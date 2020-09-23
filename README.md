# China Stock Reports Scrapers 上市公司报告爬虫

Simple easy-to-use scrapers for crawling stock reports from China Shanghai and Shenzhen Exchanges

简易股票公司报告爬虫，用于爬取指定上市公司公布的报告

#### 基本用法

``` python
# 爬取上交所报告
python3 scrape_shanghai_reports.py

# 爬取深交所报告
python3 scrape_shenzhen_reports.py
```

对于上交所的脚本，需要在上述代码的开头提供 cookies 和指定的开始截止日期。
 
``` python
# add your cookies here
cookies = {
    'cookies': ''
}

# adjust begin date and end date here
begin_date = '2000-01-01'
end_date = '2020-09-08'
```

类似的，对于深交所的脚本，需要在上述代码的开头指定开始截止日期。

可以在 `shanghai_code` 和 `shenzhen_code` 两个文件中指定需要爬取的公司对应的股票代码。

在默认情况下，爬取的报告会保存到 `downloads/` 目录下。

#### 规范化文件名

爬取的文件名没有统一的格式，可以使用 `rename_report_filenames.py` 来统一文件名。统一的格式为

```
[STOCK CODE]_[YEAR]_[REPORT TYPE]_[REPORT TAG].pdf

Report Type:
AN - 年报
SA - 半年报
Q1 - 一季度报
Q3 - 三季度报

Report Tag:
Full - 全文
Main - 正文
Abstract - 摘要
Suppl - 补充材料
```

#### 生成文件清单

使用 `generate_check_list.py` 来生成下载的文件清单，并保存到 csv 文件。

#### 感谢声明

本代码借鉴了

[https://github.com/thunderhit/shreport](https://github.com/thunderhit/shreport)

[https://blog.csdn.net/qq_34472145/article/details/104217808](https://blog.csdn.net/qq_34472145/article/details/104217808)

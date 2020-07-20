from gevent import monkey

monkey.patch_all()
import schedule
import pymongo
import datetime
import requests
import csv
import gevent
import time
from pymongo import MongoClient
from gevent.queue import Queue

# 初始化
start = time.time()             #初始化异步
work = Queue()

client=MongoClient()#初始化数据库
db = client.test_database
collection = db.fund_collection

funds = []       #基金名称
funds_info = []  #基金信息收纳
tasks_list = []  #多线程爬虫任务


def csv_reader():
    with open('temp.csv') as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            funds.append(row[0])

    f.close()


# 读取前200条得基金数据

def fund_scrape():
    while not work.empty():
        url = 'https://api.doctorxiong.club/v1/fund?code={ID}'
        ID = work.get_nowait()
        result = requests.get(url.format(ID=ID))
        js = result.json()
        funds_info.append(js['data'][0])
        print('saving  ' + str(ID))
# 爬取基金信息


def asy_scraper():
    for fund in funds:
        work.put_nowait(fund)
    for x in range(5):
        # 相当于创建了5个爬虫
        task = gevent.spawn(fund_scrape())
        # 用gevent.spawn()函数创建执行crawler()函数的任务。
        tasks_list.append(task)
        # 往任务列表添加任务。
    gevent.joinall(tasks_list)
    # 用gevent.joinall方法，执行任务列表里的所有任务，就是让爬虫开始爬取网站。
    end = time.time()
# 多线程调用




def job():
    csv_reader()
    asy_scraper()
    x = collection.insert_many(funds_info)
    print(x.inserted_ids)
# schedule.every().day.at("06:40").do(job)
# while True:
#     schedule.run_pending()
#     time.sleep(1)

# 输出插入的所有文档对应的 _id 值

# job()

# collection.insert_one({"name":"rua"})
myquery = {"lastYearGrowth" : {'$gt' : 50}}
# myquery = {"code" : '006345'}
results = collection.find().sort('lastYearGrowth', pymongo.DESCENDING)
for x in results:
    print(x)

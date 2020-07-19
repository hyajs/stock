import requests,csv,schedule,time

rows = []
fund_lists = [ '515050','159995','001643','001102','519674','000480','001712','260108','002803','519193','003745','161903','007119','519068']
stock_lists = ['sz002460','sh603960','sh600345','sz000975','sh601168']
# 当前想要获取的股票和基金信息

def fund(ID):
    url = 'https://api.doctorxiong.club/v1/{type}?code={ID}'
    result = requests.get(url.format(type='fund', ID=ID))
    new_url = url.format(type='fund', ID=ID)
    print(new_url)

    js = result.json()
    code = js['data'][0]['code']
    netWorth = js['data'][0]['netWorth']
    name = js['data'][0]['name']
    date = js['data'][0]['netWorthDate']
    print(netWorth)
    row = [code,name,date,netWorth]
    rows.append(row)

def stock(ID):
    url = 'https://api.doctorxiong.club/v1/{type}?code={ID}'
    result = requests.get(url.format(type='stock', ID=ID))
    new_url = url.format(type='fund', ID=ID)
    print(new_url)

    js = result.json()
    code = js['data'][0]['code']
    price = js['data'][0]['price']
    name = js['data'][0]['name']
    date = js['data'][0]['date']

    row = [code,name,date,price]
    print(row)
    rows.append(row)

# 接入股票和基金线上提供的api，通过js的方法读取数据
# 网站原网址 https://www.doctorxiong.club/api/

def create_csv():
    path = "aa.csv"
    with open(path,'w') as f:
        csv_write = csv.writer(f)
        csv_head = ["代码","名称","日期","净值"]
        csv_write.writerow(csv_head)
        for i in rows:
            csv_list = [i[0],i[1],i[2],i[3]]
            csv_write.writerow(csv_list)

#记录并且创建csv文件

def main():
    for stock_list in stock_lists:
        print(stock_list)
        stock(stock_list)
    for fund_list in fund_lists:
        print(fund_list)
        fund(fund_list)
    create_csv()




schedule.every().day.at("06:20").do(main)
while True:
    schedule.run_pending()
    time.sleep(1)
# 每天早上6点20自动运行代码
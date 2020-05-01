# -*-coding:utf8-*-
# http://quotes.money.163.com/service/chddata.html?code=1002714&start=20140117&end=20190927&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP

# 沪深AB
# http://quotes.money.163.com/hs/service/diyrank.php?host=http%3A%2F%2Fquotes.money.163.com%2Fhs%2Fservice%2Fdiyrank.php&page=0&query=STYPE%3AEQA&fields=NO%2CSYMBOL%2CNAME%2CPRICE%2CPERCENT%2CUPDOWN%2CFIVE_MINUTE%2COPEN%2CYESTCLOSE%2CHIGH%2CLOW%2CVOLUME%2CTURNOVER%2CHS%2CLB%2CWB%2CZF%2CPE%2CMCAP%2CTCAP%2CMFSUM%2CMFRATIO.MFRATIO2%2CMFRATIO.MFRATIO10%2CSNAME%2CCODE%2CANNOUNMT%2CUVSNEWS&sort=PERCENT&order=desc&count=24&type=query
# http://quotes.money.163.com/hs/service/diyrank.php?host=http%3A%2F%2Fquotes.money.163.com%2Fhs%2Fservice%2Fdiyrank.php&page=0&query=STYPE%3AEQB&fields=NO%2CSYMBOL%2CNAME%2CPRICE%2CPERCENT%2CUPDOWN%2CFIVE_MINUTE%2COPEN%2CYESTCLOSE%2CHIGH%2CLOW%2CVOLUME%2CTURNOVER%2CHS%2CLB%2CWB%2CZF%2CPE%2CMCAP%2CTCAP%2CMFSUM%2CMFRATIO.MFRATIO2%2CMFRATIO.MFRATIO10%2CSNAME%2CCODE%2CANNOUNMT%2CUVSNEWS&sort=PERCENT&order=desc&count=24&type=query
# 沪深A排序
# http://quotes.money.163.com/hs/service/diyrank.php?host=http%3A%2F%2Fquotes.money.163.com%2Fhs%2Fservice%2Fdiyrank.php&page=0&query=STYPE%3AEQA&fields=NO%2CSYMBOL%2CNAME%2CPRICE%2CPERCENT%2CUPDOWN%2CFIVE_MINUTE%2COPEN%2CYESTCLOSE%2CHIGH%2CLOW%2CVOLUME%2CTURNOVER%2CHS%2CLB%2CWB%2CZF%2CPE%2CMCAP%2CTCAP%2CMFSUM%2CMFRATIO.MFRATIO2%2CMFRATIO.MFRATIO10%2CSNAME%2CCODE%2CANNOUNMT%2CUVSNEWS&sort=SYMBOL&order=asc&count=24&type=query
# 沪A深A
# http://quotes.money.163.com/hs/service/diyrank.php?host=http%3A%2F%2Fquotes.money.163.com%2Fhs%2Fservice%2Fdiyrank.php&page=0&query=STYPE%3AEQA%3BEXCHANGE%3ACNSESH&fields=NO%2CSYMBOL%2CNAME%2CPRICE%2CPERCENT%2CUPDOWN%2CFIVE_MINUTE%2COPEN%2CYESTCLOSE%2CHIGH%2CLOW%2CVOLUME%2CTURNOVER%2CHS%2CLB%2CWB%2CZF%2CPE%2CMCAP%2CTCAP%2CMFSUM%2CMFRATIO.MFRATIO2%2CMFRATIO.MFRATIO10%2CSNAME%2CCODE%2CANNOUNMT%2CUVSNEWS&sort=PERCENT&order=desc&count=24&type=query
# http://quotes.money.163.com/hs/service/diyrank.php?host=http%3A%2F%2Fquotes.money.163.com%2Fhs%2Fservice%2Fdiyrank.php&page=0&query=STYPE%3AEQA%3BEXCHANGE%3ACNSESZ&fields=NO%2CSYMBOL%2CNAME%2CPRICE%2CPERCENT%2CUPDOWN%2CFIVE_MINUTE%2COPEN%2CYESTCLOSE%2CHIGH%2CLOW%2CVOLUME%2CTURNOVER%2CHS%2CLB%2CWB%2CZF%2CPE%2CMCAP%2CTCAP%2CMFSUM%2CMFRATIO.MFRATIO2%2CMFRATIO.MFRATIO10%2CSNAME%2CCODE%2CANNOUNMT%2CUVSNEWS&sort=PERCENT&order=desc&count=24&type=query
# 沪B深B
# http://quotes.money.163.com/hs/service/diyrank.php?host=http%3A%2F%2Fquotes.money.163.com%2Fhs%2Fservice%2Fdiyrank.php&page=0&query=STYPE%3AEQB%3BEXCHANGE%3ACNSESH&fields=NO%2CSYMBOL%2CNAME%2CPRICE%2CPERCENT%2CUPDOWN%2CFIVE_MINUTE%2COPEN%2CYESTCLOSE%2CHIGH%2CLOW%2CVOLUME%2CTURNOVER%2CHS%2CLB%2CWB%2CZF%2CPE%2CMCAP%2CTCAP%2CMFSUM%2CMFRATIO.MFRATIO2%2CMFRATIO.MFRATIO10%2CSNAME%2CCODE%2CANNOUNMT%2CUVSNEWS&sort=PERCENT&order=desc&count=24&type=query
# http://quotes.money.163.com/hs/service/diyrank.php?host=http%3A%2F%2Fquotes.money.163.com%2Fhs%2Fservice%2Fdiyrank.php&page=0&query=STYPE%3AEQB%3BEXCHANGE%3ACNSESZ&fields=NO%2CSYMBOL%2CNAME%2CPRICE%2CPERCENT%2CUPDOWN%2CFIVE_MINUTE%2COPEN%2CYESTCLOSE%2CHIGH%2CLOW%2CVOLUME%2CTURNOVER%2CHS%2CLB%2CWB%2CZF%2CPE%2CMCAP%2CTCAP%2CMFSUM%2CMFRATIO.MFRATIO2%2CMFRATIO.MFRATIO10%2CSNAME%2CCODE%2CANNOUNMT%2CUVSNEWS&sort=PERCENT&order=desc&count=24&type=query


import os
import time
import datetime 

import json
import socket
import urllib
import urllib.error
import urllib.request


# import tushare as ts
#         opendaylist = ts.trade_cal()
import numpy as np 
import pandas as pd
# pd.set_option('display.max_rows',None)
# pd.set_option('display.max_rows',1000)
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
# import csv

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Executor, as_completed, wait, ALL_COMPLETED,FIRST_COMPLETED


# config data
g_needUpdateMarket  = 0
g_stockBeginDate    = '2008-01-01'
g_stockOpenDatePath = '\\.tradday.csv'    
g_dbName            = 'bstock'
g_itChunkSize  = 50
g_itChunkList = []


# global struct
g_pdTraDay              = pd.DataFrame()
g_pdSortStockList    = pd.DataFrame()

# 在Windows下经常用python open函数的人相信都遇到过UnicodeDecodeError: ‘gbk’ codec…这种编码问题。而且很多有经验的人应该知道解决方法是加上参数encoding=“utf-8”，因为"utf-8"是更通用的编码：
import _locale
_locale._getdefaultlocale = (lambda *args: ['zh_CN', 'utf8'])

# logfileimport _locale
g_datapath = os.path.dirname(os.path.abspath(__file__))
logpath = g_datapath + '\\000001amarket_log.txt'
print(logpath)
logfp = open(logpath, "w")
logfp.write("start the A market get data program at %(time)s\n"%{'time' : time.strftime("%H:%M:%S")})
begintime = time.time()
g_datapath = g_datapath + "\\acsvdata"
if (os.path.exists(g_datapath) == False):
    os.makedirs(g_datapath)

g_stockDataPath = g_datapath + "\\.data.csv"
if (os.path.exists(g_stockDataPath) == False):
    file = open(g_stockDataPath, 'w')
    file.close()

# http://file.tushare.org/tsdata/calAll.csv
g_stockOpenDatePath = g_datapath + g_stockOpenDatePath
if (os.path.exists(g_stockOpenDatePath) == False):
    temp = "http://file.tushare.org/tsdata/calAll.csv"
    # http://file.tushare.org/tsdata/calAll.csv
    try:
        urllib.request.urlretrieve(temp, g_stockOpenDatePath)
    except socket.timeout:
        count = 1
        while count <= 5:
            try:
                urllib.request.urlretrieve(temp, g_stockOpenDatePath)                                              
                break
            except socket.timeout:
                err_info = 'Reloading for %d time'%count if count == 1 else 'Reloading for %d times'%count
                print(err_info)
                count += 1
        if count > 5:
            print("download job failed!\n")

g_itData = pd.read_csv(g_stockOpenDatePath, iterator=True)
while True:
    try:
        chunk = g_itData.get_chunk(g_itChunkSize)
        g_itChunkList.append(chunk)
    except StopIteration:
        print ("Iteration is stopped.")
        break
g_pdTraDay = pd.concat(g_itChunkList, ignore_index=True)
# print(g_pdTraDay)
# print(g_pdTraDay.loc[g_pdTraDay['calendarDate'] == '2019-10-01'] )

def getMarket(market):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/2010010 Firefox/62.0'}
    if (market == 'A') or (market == 'B'):#AB股
        temp = "http://quotes.money.163.com/hs/service/diyrank.php?host=http%3A%2F%2Fquotes.money.163.com%2Fhs%2Fservice%2Fdiyrank.php&page=0&query=STYPE%3AEQ" + \
                market + "&fields=NO%2CNAME%2CSYMBOL%2CVOLUME&sort=SYMBOL&order=asc&count=5000&type=query"
    else:
        if (market[:2] == 'SH') or (market[:2] == 'SZ'):
            if (market[-1] == 'A') or (market[-1] == 'B'):
                temp = "http://quotes.money.163.com/hs/service/diyrank.php?host=http%3A%2F%2Fquotes.money.163.com%2Fhs%2Fservice%2Fdiyrank.php&page=0&query=STYPE%3AEQ" + \
                        market[-1] + "%3BEXCHANGE%3ACNSE" + market[:2] + "&fields=NO%2CNAME%2CSYMBOL%2CVOLUME&sort=SYMBOL&order=asc&count=5000&type=query"
        else:
            if (market == 'KCB'):#科创板
                temp = "http://quotes.money.163.com/hs/service/diyrank.php?host=http%3A%2F%2Fquotes.money.163.com%2Fhs%2Fservice%2Fdiyrank.php&page=0&query=STYPE%3AEQA" + \
                        "%3BKSH%3Atrue%3BNODEAL%3Afalse&fields=NO%2CNAME%2CSYMBOL%2CVOLUME&sort=SYMBOL&order=asc&count=5000&type=query"
            else:
                if (market == 'CYB'):#创业板
                    temp = "http://quotes.money.163.com/hs/service/diyrank.php?host=http%3A%2F%2Fquotes.money.163.com%2Fhs%2Fservice%2Fdiyrank.php&page=0&query=STYPE%3AEQA" + \
                            "%3BGEM%3Atrue%3BNODEAL%3Afalse&fields=NO%2CNAME%2CSYMBOL%2CVOLUME&sort=SYMBOL&order=asc&count=5000&type=query"
    print(temp)
    logfp.write(temp)
    logfp.flush()
    req = urllib.request.Request(url=temp, headers=headers)
    try:
        stockopen = urllib.request.urlopen(req, timeout=10)
        html =  str(stockopen.read())
        htmljson = json.loads(html[2:-1])
        sortstocklist = htmljson.get('list')
        for stdict in sortstocklist:
            stdict['NAME'] = stdict['NAME'].encode('utf-8').decode('unicode_escape').lower().replace('*', '_')
        # basetype = np.dtype([('SYMBOL', np.str_, 6), ('NAME', np.str_, 20), ('PRICE', np.str_, 10), ('VOLUME', np.float64, 1)])
        pdSortStockList = pd.DataFrame(sortstocklist, columns=['SYMBOL' , 'NAME', 'PRICE', 'VOLUME'], dtype=str)
                        #  ,dtype = basetype)
        # del pdSortStockList['PRICE']
        # del pdSortStockList['NO']
        pdSortStockList.rename(columns={'PRICE':'DATE'},inplace=True) 
        stockopen.close()
        # print(pdSortStockList)
        pdSortStockList.to_csv(g_stockDataPath, index=False) 
    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            print("e.code")
            print(e.code)
        elif hasattr(e, 'reason'):
            print("e.reason")
            print(e.reason)
        logfp.write("urllib.error.URLError\n")
    except socket.timeout as e:
        print (type(e) )
    return pdSortStockList

# database
# db_info = {'user':'pytest',  
#     'password':'pytest123',  
#     'host':'localhost',  
#     'database': g_dbName  # 这里我们事先指定了数据库，后续操作只需要表即可
# }      
# engine = create_engine('mysql+pymysql://%(user)s:%(password)s@%(host)s/%(database)s?charset=utf8' % db_info,encoding='utf-8')    #这里直接使用pymysql连接,echo=True，会显示在加载数据库所执行的SQL语句。
# data = pd.read_sql_query("select TABLE_NAME from INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA=\'%(db)s\' and TABLE_NAME=\'000000amarket\'"%{'db' : g_dbName},con = engine)

print(os.path.getsize(g_stockDataPath))
g_pdSortStockList = getMarket('A')
# if (os.path.getsize(g_stockDataPath) > 13096):
#     g_pdSortStockList = pd.read_csv(g_stockDataPath, dtype={'SYMBOL' : str, 'NAME' : str, 'PRICE' : str, 'VOLUME' : int})#, encoding='gbk')
#     if(g_pdSortStockList.empty):
#     # if(1):
#         g_pdSortStockList = getMarket('A')
#     # else:
#     #     # g_pdSortStockList = pd.read_sql_query('select * from `000000Amarket`',con = engine)
#     #     if g_pdSortStockList.empty:
#     #         g_pdSortStockList = getMarket('A')
# else:
#     g_pdSortStockList = getMarket('A')
    
# print(g_pdSortStockList)
# g_pdSortStockList.to_csv(g_stockDataPath, index=False) 

# pd.set_option('display.max_rows',None)#max_colwidth
# logfp.write(str(g_pdSortStockList[ g_pdSortStockList[ 'DATE'].isnull() ] ))
# logfp.flush()
# logfp.write("all of the stocklist is all of the stocklist is all of the stocklist is all of the stocklist is:\n")
# logfp.flush()
# logfp.write(str(g_pdSortStockList[ g_pdSortStockList[ 'DATE'].isnull() == False] ))
# logfp.flush()

# logfp.write("%(symbol)s \n"%{'symbol':g_pdSortStockList.sort_index})
# logfp.write("all of the stocklist is all of the stocklist is all of the stocklist is all of the stocklist is:\n")
# logfp.flush()
pd.set_option('display.max_rows',None)#max_colwidth
g_pdSortStockList = g_pdSortStockList.sort_values(by='DATE', ascending=False).reset_index(drop=True, inplace=False)
logfp.write("%(symbol)s \n"%{'symbol':g_pdSortStockList})
logfp.flush()
pd.set_option('display.max_rows',10 )
print(g_pdSortStockList)

# print(g_pdSortStockList.loc[g_pdSortStockList.index.size - 1]['SYMBOL'])
# print(type(g_pdSortStockList.loc[0]))
# print((g_pdSortStockList.loc[0]))
# pdStock = g_pdSortStockList.loc[0]

def getStockTradeDate():
    datanow = datetime.datetime.today().date()
    if g_pdTraDay.empty:
        # print(datanow)
        if datanow.strftime("%w") == 0:
            datanow = datanow + datetime.timedelta(-2)
        else:
            datanow = datanow + datetime.timedelta(-1)
    else:
        while True:
            strdate = datanow.strftime("%Y-%m-%d")
            # print(strdate)
            dataseries = g_pdTraDay.loc[g_pdTraDay['calendarDate'] == strdate]['isOpen']
            # print(dataseries)
            if dataseries.empty == False:
                if int(dataseries) == 1:
                    break
            datanow = datanow + datetime.timedelta(-1)
            
    datanow = datanow.strftime("%Y-%m-%d")
    print(datanow)
    return datanow
g_lastTraDate = getStockTradeDate()


def getStockToSql(pdStock, datanow, stockname):
    # print(type(pdStock['SYMBOL']))
    # print(str(pdStock['SYMBOL']))
    # print(pdStock)
    # print(pdStock['DATE'] == datanow)
    temp = "code=1%(code)06s&start=%(st)s&end=%(end)s"%{'code' : pdStock['SYMBOL'], 'st' : pdStock['DATE'].replace('-', ''), 'end' : datanow.replace('-', '')}
    if pdStock['SYMBOL'][0] == '6':
        temp = temp.replace('code=1', 'code=0')
    temp = ("http://quotes.money.163.com/service/chddata.html?" + temp +
            "&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP")              
    print(temp) 
    logfp.write("%(stockname)s get "%{'stockname' : stockname} + temp + '\n')
    logfp.flush()

    abs_dir = g_datapath + "\\%(stockname)s.csv"%{'stockname' : stockname}
    # temp_dir = g_datapath + "\\temp_%(stockname)s.csv"%{'stockname' : stockname}
    get_dir = abs_dir
    # if (os.path.exists(abs_dir)):
    #     get_dir = temp_dir
    socket.setdefaulttimeout(60)

    # print(abs_dir)
    # if (os.path.exists(abs_dir)):
    #     os.remove(abs_dir)

#     getfinish = time.mktime(datetime.datetime.now().timetuple()) + 30
#     print(getfinish)
#     def getCsvCallback(blocknum, blocksize, totalsize):
#         nonlocal getfinish
#         per = 100.0 * blocknum * blocksize / totalsize
#         if per >= 100 :
#             getfinish = 0
    # socket.setdefaulttimeout(30)
    try:
        urllib.request.urlretrieve(temp, get_dir)#, getCsvCallback) 
    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            print("e.code")
            print(e.code)
        elif hasattr(e, 'reason'):
            print("e.reason")
            print(e.reason)
        logfp.write("%(stock)s urllib.error.URLError\n"%{'stock' : stockname})
        logfp.flush() 
        g_pdSortStockList.loc[pdStock.name, 'DATE'] = g_stockBeginDate
        # pdStock.loc['DATE'] = g_stockBeginDate
        return pdStock
    except socket.timeout:
        count = 1
        while count <= 5:
            try:
                urllib.request.urlretrieve(temp, get_dir)#, getCsvCallback)                                              
                break
            except socket.timeout:
                err_info = 'Reloading for %d time'%count if count == 1 else 'Reloading for %d times'%count
                print(err_info)
                logfp.write("update %(stock)s timeout count %(err)s\n"%{'stock' : stockname, 'err' : err_info})
                logfp.flush() 
                count += 1
            except urllib.error.URLError as e:
                if hasattr(e, 'code'):
                    print("e.code")
                    print(e.code)
                elif hasattr(e, 'reason'):
                    print("e.reason")
                    print(e.reason)
                logfp.write("%(stock)s urllib.error.URLError\n"%{'stock' : stockname})
                logfp.flush() 
                g_pdSortStockList.loc[pdStock.name, 'DATE'] = g_stockBeginDate
                # pdStock.loc['DATE'] = g_stockBeginDate
                return pdStock
        if count > 5:
            print("download job failed!\n")
            logfp.write("update %(stock)s download job failed\n"%{'stock' : stockname})
            logfp.flush() 
            g_pdSortStockList.loc[pdStock.name, 'DATE'] = g_stockBeginDate
            # pdStock.loc['DATE'] = g_stockBeginDate
            return pdStock

    # if temp_dir == get_dir:
    #     stockdata = pd.read_csv(abs_dir, encoding='gbk')
    #     tempstockdata = pd.read_csv(temp_dir, encoding='gbk')
    #     stockdata = pd.concat([tempstockdata, stockdata],ignore_index = True)
    #     # print(stockdata)
    #     stockdata.to_csv(abs_dir, mode='w', encoding='gbk', index=0)#, header=False)
    # if (os.path.exists(temp_dir)):
    #     os.remove(temp_dir)
    # print(stockdata)
    # print(str(stockdata.index.size))

    stockdata = pd.DataFrame()
    if os.path.exists(abs_dir):
        stockdata = pd.read_csv(abs_dir, encoding='gbk', nrows=1)
    if ( stockdata.empty == False):
        # stockname = stockdata.loc[0, '名称'].lower().replace('*', '_')
        # stocksymbol = stockdata.loc[0, '股票代码'][1:]
        # stockname = stocksymbol + stockname
        # del stockdata['名称']
        # del stockdata['前收盘']
        # del stockdata['流通市值']
        # del stockdata['股票代码']
        # stockdata = stockdata.drop(['名称', '前收盘', '流通市值', '股票代码'], axis = 1)
        # stockdata.rename(columns={'日期':'Date', '收盘价':'ClosePrise', '最高价':'HighPrise', '最低价':'LowPrise', '开盘价':'OpenPrise', 
        #                         '涨跌额':'UpDownPrice', '涨跌幅':'UpDownRange', '换手率':'TurnoverRate', 
        #                         '成交量':'Volume', '成交金额':'AMOUNT', '总市值':'MarketValue'},inplace=True) 
        # print(stockdata)
        # if(pd.isnull(pdStock['DATE'])):
        #     stockdata.to_sql(stockname, con=engine, if_exists='replace', index=False) 
        # else:
        #     stockdata.to_sql(stockname, con=engine, if_exists='append', index=False)  
        # pdStock['DATE'] = datanow
        g_pdSortStockList.loc[pdStock.name, 'DATE'] = datanow
        # pdStock.loc['DATE'] = datanow
        # logfp.write("update %(stock)s success\n"%{'stock' : stockname})
        # logfp.flush() 
    else:
        g_pdSortStockList.loc[pdStock.name, 'DATE'] = g_stockBeginDate
        # pdStock.loc['DATE'] = g_stockBeginDate
        logfp.write("warning %(stock)s fail with none data\n"%{'stock' : stockname})
        logfp.flush() 



def spider(item):
    # print(pdStock)#.type)
    # print(pdStock['SYMBOL'])
    # nonlocal g_pdSortStockList
    pdStock = g_pdSortStockList.ix[item]
    stockname = str(pdStock['SYMBOL']) + str(pdStock['NAME'])
    abs_dir = g_datapath + "\\%(stockname)s.csv"%{'stockname' : stockname}
    # print(abs_dir)
    # print("spider %(stock)s\n"%{'stock' : stockname})
    edatanow = -1
    pdStock.loc['DATE'] = g_stockBeginDate
    if (os.path.exists(abs_dir)):
        data = pd.read_csv(abs_dir, encoding='gbk', nrows=1)
        # print(type(data))
        if ( data.empty == False):
            # pdStock.loc['DATE'] = data['日期'][0]
            if(pdStock['VOLUME'] == 0) or ( data['日期'][0] == g_lastTraDate ):
                edatanow = 0
        
    # print(datanow +"---" + str(edatanow))
    if(edatanow):
        # logfp.write("begin update %(symbol)s \n"%{'symbol':stockname})
        # logfp.flush()
        getStockToSql(pdStock, g_lastTraDate, stockname)
    else:
        logfp.write(" %(symbol)s num %(num)s noneed update \n"%{'symbol':stockname, 'num' : pdStock.name})
        logfp.flush()
        g_pdSortStockList.loc[pdStock.name, 'DATE'] = g_lastTraDate
        pdStock.loc['DATE'] = g_lastTraDate
    
    # print(g_pdSortStockList)
    return pdStock

def task_loop():
    pool = ThreadPoolExecutor(max_workers=32)
    allitem = g_pdSortStockList.index.size-1
    nowitem = 0
    task_list = []
    # task_list.append(pool.submit(taskfortime, tasktime))
    # for taskitem in range (0, allitem, 1):
    for taskitem in range (allitem, -1, -1):
        # if g_pdSortStockList.loc[taskitem]['SYMBOL'][0] == '6':#6：沪A 9：沪B  3?0：深A 2:深B
        task_list.append(pool.submit(spider, taskitem))
        # task_list.append(pool.submit(spider, g_pdSortStockList.loc[taskitem, {'SYMBOL', 'NAME', 'DATE', 'VOLUME'}]))
    # wait(task_list, timeout=60, return_when=FIRST_COMPLETED)
    for f in as_completed(task_list):
        f_ret = f.result()
        nowitem += 1
        print("all\tnow\tpercent\ttime(s)")
        print("%(all)s\t%(now)s\t%(per).05s%%\t%(time).05ss"%{'all': allitem, 'now' : nowitem, 'per' : 100*nowitem/allitem, 'time' : (time.time()-begintime)})
        
        logfp.write("%(all)s\t%(now)s\t%(per).05s%%\t%(time).05ss"%{'all': allitem, 'now' : nowitem, 'per' : 100*nowitem/allitem, 'time' : (time.time()-begintime)})
        logfp.flush() 
        try:
            ret = f.done()
            if ret:
                if pd.isnull(f_ret['DATE']):
                    ret = "finish %(number)s%(name)s fail at %(time)s use %(use).05ss\n"%{'number' : f_ret['SYMBOL'], 'name' : f_ret['NAME'], 'time' : time.strftime("%H:%M:%S"), 'use' : (time.time()-begintime)}
                else:
                    ret = "finish %(number)s%(name)s done at %(time)s use %(use).05ss %(data)s\n"%{'number' : f_ret['SYMBOL'], 'name' : f_ret['NAME'], 'time' : time.strftime("%H:%M:%S"), 'use' : (time.time()-begintime), 'data':f_ret['DATE']}
                print(ret)
                logfp.write(ret)
                logfp.flush()
                g_pdSortStockList.to_csv(g_stockDataPath, index=False) 
            else:
                logfp.write(f)
                logfp.flush() 
        except Exception as e:
            f.cancel()
            ret = "finish %(number)s%(name)s error:%(err)s at %(time).05ss\n"%{'number' : f_ret['SYMBOL'], 'name' : f_ret['NAME'], 'err' : str(e), 'time' : time.strftime("%H:%M:%S")}
            print(ret)
            logfp.write(ret)
            logfp.flush() 


if __name__ == '__main__':   
    # taskloop = 0
    # while( g_pdSortStockList[ 'DATE'].isnull().empty == False ):
    task_loop()
        # taskloop += 1
        # if taskloop >= 3:
        #     break
            
g_pdSortStockList.to_csv(g_stockDataPath, index=False) 
logfp.write("A market get data program end at %(time)s use %(use).05ss\n"%{'time' : time.strftime("%H:%M:%S"), 'use' :(time.time()-begintime)})
logfp.flush()
pd.set_option('display.max_rows',None)#max_colwidth
print(g_pdSortStockList[ g_pdSortStockList[ 'DATE'].isnull() ])
logfp.write("%(symbol)s \n"%{'symbol':g_pdSortStockList[ g_pdSortStockList[ 'DATE'].isnull() ]})
logfp.flush()
pd.set_option('display.max_rows',10 )
logfp.close()
# sys.exit()
os._exit(1)
# engine.

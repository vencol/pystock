# -*-coding:utf8-*-

import os
import time
import datetime 

import json
import socket
import urllib
import urllib.error
import urllib.request
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Executor, as_completed, wait, ALL_COMPLETED,FIRST_COMPLETED

# 在Windows下经常用python open函数的人相信都遇到过UnicodeDecodeError: ‘gbk’ codec…这种编码问题。而且很多有经验的人应该知道解决方法是加上参数encoding=“utf-8”，因为"utf-8"是更通用的编码：
import _locale
_locale._getdefaultlocale = (lambda *args: ['zh_CN', 'utf8'])

ALL_BEGIN_DATE = '20080101'


class getStockCsv(object):
    
    logfp               = 0
    lastcsvfile         = ''
    workdaydata         = pd.DataFrame()
    lastcsvdata         = pd.DataFrame()
    lasttimedata        = pd.DataFrame()
    csvdir              = os.path.dirname(os.path.abspath(__file__)) + '\\csv'
    headers             = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/2010010 Firefox/62.0'}
        
    def __init__(self, logname="log.txt"):
        self.begintime = time.time()
        self.get_log_path(logname)
        if (os.path.exists(self.csvdir) == False):
            os.makedirs(self.csvdir)
        self.get_trade_day()
        self.getMarket('A')
        # self.get_stock_update_last_time(1)
        # self.get_stock_update_process(1)
        self.task_loop(0, self.lastcsvdata.index.size)

    def is_trade_day(self, day):
        if(len(day) != 8):
            return 0
        day = day[:4] + '-' + day[4:6] + '-' + day[6:]
        tradedaydata = self.workdaydata[ self.workdaydata['DATE'] == day ]
        return tradedaydata['TRADEDAY']

    def get_trade_day(self, dayname="tradeday.csv", start='2020-01-01', end='none', update=False):
        from datetime import datetime,timedelta
        from chinese_calendar import is_holiday
        workdayfiledir = self.csvdir + '\\' + dayname
        # today = datetime.strptime(today,'%Y-%m-%d').date()  
        if(os.path.isfile(workdayfiledir) == False or update == True):
            update = True
        else:
            self.workdaydata = pd.read_csv(workdayfiledir, encoding='gbk')#, nrows=1)
            today = datetime.today().date().strftime("%Y-%m-%d")
            if(today not in self.workdaydata['DATE'].values):
                update = True

        today = datetime.today().date().strftime("%Y")
        today = today + '-12-31'
        if(update):
            if type(start) == str:
                start = datetime.strptime(start,'%Y-%m-%d').date()
            if(end == 'none'):
                end = datetime.strptime(today,'%Y-%m-%d').date()    
            elif type(end) == str:
                end = datetime.strptime(end,'%Y-%m-%d').date()  
            if start > end:
                start,end = end,start
            self.workdaydata.insert(0, 'DATE', '')
            self.workdaydata.insert(1, 'TRADEDAY', '')
                
            while True:
                if start > end:
                    break
                if is_holiday(start) or start.weekday()==5 or start.weekday()==6:
                    self.workdaydata = self.workdaydata.append([{'DATE': start.strftime("%Y-%m-%d"), 'TRADEDAY': 0}], ignore_index=True)
                else:
                    self.workdaydata = self.workdaydata.append([{'DATE': start.strftime("%Y-%m-%d"), 'TRADEDAY': 1}], ignore_index=True)
                start += timedelta(days=1)
            self.workdaydata.to_csv(workdayfiledir, mode='w', encoding='gbk', index=0)#, header=False)

    def get_log_path(self, logname="log.txt"):
        logpath = os.path.dirname(os.path.abspath(__file__)) + '\\' + logname
        self.logfp = open(logpath, "w")
        self.logfp.write("start the A market get data program at %(time)s\n"%{'time' : time.strftime("%H:%M:%S")})
        self.logfp.flush()

    def get_stock_update_last_time(self, index):
        start_day   = self.date_formal(self.lastcsvdata.loc[index, ['BEGINDAY']]['BEGINDAY'])
        end_day     = self.date_formal(self.lastcsvdata.loc[index, ['ENDDAY']]['ENDDAY'])
        temp = 'http://quotes.money.163.com/trade/lsjysj_%(code)s.html'%{'code': self.lastcsvdata.loc[index, ['SYMBOL']]['SYMBOL']}
        # print(temp)
        self.logfp.write("\n%(url)s at %(time)s\t"%{'url' : temp, 'time' : time.strftime("%H:%M:%S")})
        self.logfp.flush()
        req = urllib.request.Request(url=temp, headers=self.headers)
        try:
            stockopen = urllib.request.urlopen(req, timeout=10)
            html =  stockopen.read()
            if html:
                soup = BeautifulSoup(html, 'lxml')
            if soup:
                input = soup.find('input', {'name': "date_start_value"})
                start_day = input['value']
                input = soup.find('input', {'name': "date_end_value"})
                end_day = input['value']
                # start_day   = start_day.replace('-0', '/').replace('-', '/')
                # end_day     = end_day.replace('-0', '/').replace('-', '/')
            stockopen.close()
        except urllib.error.URLError as e:
            if hasattr(e, 'code'):
                print("e.code")
                print(e.code)
            elif hasattr(e, 'reason'):
                print("e.reason")
                print(e.reason)
            self.logfp.write("get_stock_update_last_time urllib.error.URLError\n")
        except socket.timeout as e:
            print (type(e) )
        
        return start_day, end_day 

    def date_formal(self, date):
        date = str(date)
        try:
            if(date[4] == '/' or date[4] == '-'):
                if(len(date) == 8):
                    date = date[:4] + '0' + date[5] + '0' + date[7]
                elif(len(date) == 10):
                    date   = date.replace('/', '').replace('-', '')  
                elif(date[6] == '/' or date[6] == '-' ):
                    date = date[:4] + '0' + date[5] + date[7:]
                else:
                    date = date[:4] + date[5:7] + '0' + date[-1]
            date = date[:4] + '-' + date[4:6] + '-' + date[6:]
        except IndexError as e:
            return date
        return date
            

    def get_stock_data(self, index, endsave):
        needupdate = 1
        start = ALL_BEGIN_DATE
        code = self.lastcsvdata.loc[index, ['SYMBOL']]['SYMBOL']
        csvdir = self.csvdir + "\\%(code)s.csv"%{'code': code}
        laststockdata = pd.DataFrame()
        if(os.path.isfile(csvdir)):
            laststockdata = pd.read_csv(csvdir, encoding='gbk')#, nrows=1)
            if (laststockdata.empty == False):
                if (laststockdata['日期'].empty == False):
                    start = str(laststockdata.loc[0, '日期'])   
        # start = '2020/18/19'
        start   = self.date_formal(start)
        start   = start.replace('-0', '0').replace('-', '')
        endsave = endsave.replace('-0', '0').replace('-', '')
        end = datetime.datetime.today().date().strftime("%Y%m%d")
        # print(start, endsave)
        self.logfp.write("save %(code)s %(st)s - %(end)s\t"%{'code': code, 'st': start, 'end': end})
        self.logfp.flush() 
        if(endsave == start):
            needupdate = 0
        else:
            temp = "code=1%(code)06s&start=%(st)s&end=%(end)s"%{'code' : code, 'st' : start, 'end' : end}
            if code[0] == '6':
                temp = temp.replace('code=1', 'code=0')
            temp = ("http://quotes.money.163.com/service/chddata.html?" + temp +
                    "&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP")              
            print(temp) 
            self.logfp.write("\n%(url)s at %(time)s\n"%{'url' : temp, 'time' : time.strftime("%H:%M:%S")})
            self.logfp.flush()
            
            socket.setdefaulttimeout(60)
            try:
                urllib.request.urlretrieve(temp, csvdir)#, getCsvCallback) 
            except urllib.error.URLError as e:
                if hasattr(e, 'code'):
                    print("e.code")
                    print(e.code)
                elif hasattr(e, 'reason'):
                    print("e.reason")
                    print(e.reason)
                self.logfp.write("%(stock)s urllib.error.URLError\n"%{'stock' : code})
                self.logfp.flush() 
                needupdate = 0
            except socket.timeout:
                count = 1
                while count <= 5:
                    try:
                        urllib.request.urlretrieve(temp, csvdir)#, getCsvCallback)                                              
                        break
                    except socket.timeout:
                        err_info = 'Reloading for %d time'%count if count == 1 else 'Reloading for %d times'%count
                        print(err_info)
                        self.logfp.write("update %(stock)s timeout count %(err)s\n"%{'stock' : code, 'err' : err_info})
                        self.logfp.flush() 
                        count += 1
                    except urllib.error.URLError as e:
                        if hasattr(e, 'code'):
                            print("e.code")
                            print(e.code)
                        elif hasattr(e, 'reason'):
                            print("e.reason")
                            print(e.reason)
                        self.logfp.write("%(stock)s urllib.error.URLError\n"%{'stock' : code})
                        self.logfp.flush() 
                if count > 5:
                    print("download job failed!\n")
                    self.logfp.write("update %(stock)s download job failed\n"%{'stock' : code})
                    self.logfp.flush() 
                needupdate = 0
        if(needupdate):
            stockdata = pd.read_csv(csvdir, encoding='gbk')#, nrows=1)
            # print(stockdata)
            if (laststockdata.empty == False):
                stockdata = stockdata.append(laststockdata)
                stockdata.to_csv(csvdir, mode='w', encoding='gbk', index=0)#, header=False)
            # print(stockdata)


    def get_stock_update_process(self, index):
        need_update = 0
        # start_day   = self.lastcsvdata.loc[index, 'BEGINDAY']
        # end_day     = self.lastcsvdata.loc[index, 'ENDDAY']
        today = datetime.datetime.today().date().strftime("%Y-%m-%d")
        # print(today)
        # print(self.lastcsvdata.loc[index, ['SYMBOL']]['SYMBOL'])
        if(self.lasttimedata.empty):
            need_update = 1
        else:
            timedata = self.lasttimedata[ self.lasttimedata['SYMBOL'] == int(self.lastcsvdata.loc[index, ['SYMBOL']]['SYMBOL']) ]
            # print(timedata)
            if(timedata.empty):
                need_update = 1
            else:
                # print(self.date_formal(timedata.loc[index, 'QUERYDAY']), today)
                if (pd.isnull(timedata.loc[index, 'BEGINDAY']) or pd.isnull(timedata.loc[index, 'ENDDAY']) or pd.isnull(timedata.loc[index, 'QUERYDAY'])):
                    need_update = 1
                else:
                    start_day   = self.date_formal(timedata.loc[index, 'BEGINDAY'])
                    end_day     = self.date_formal(timedata.loc[index, 'ENDDAY'])
                    if(self.date_formal(timedata.loc[index, 'QUERYDAY']) != today and self.is_trade_day( today )):
                        if(timedata['VOLUME'].empty == False):
                            need_update = 1
        if (need_update):
            start_day, end_day = self.get_stock_update_last_time(index)
            self.logfp.write("get net %(code)s %(st)s - %(end)s\t"%{'code': self.lastcsvdata.loc[index, ['SYMBOL']]['SYMBOL'], 'st': start_day, 'end': end_day})
            self.get_stock_data(index, end_day)
        self.lastcsvdata.loc[index, 'BEGINDAY'] = start_day#.replace('-0', '/').replace('-', '/')
        self.lastcsvdata.loc[index, 'ENDDAY']   = end_day#.replace('-0', '/').replace('-', '/')
        self.lastcsvdata.loc[index, 'QUERYDAY'] = today
        # print(self.lastcsvdata)
        return index
        
        

    def getMarket(self, market):
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
        # print(temp)
        self.logfp.write(temp)
        self.logfp.flush()
        req = urllib.request.Request(url=temp, headers=self.headers)
        try:
            stockopen = urllib.request.urlopen(req, timeout=10)
            html =  str(stockopen.read())
            htmljson = json.loads(html[2:-1])
            sortstocklist = htmljson.get('list')
            for stdict in sortstocklist:
                stdict['NAME'] = stdict['NAME'].encode('utf-8').decode('unicode_escape').lower().replace('*', '_')
            self.lastcsvdata = pd.DataFrame(sortstocklist, columns=['SYMBOL' , 'NAME', 'PRICE', 'VOLUME'], dtype=str)
            stockopen.close()
            # print(self.lastcsvdata)
            # self.lastcsvdata.set_index(['SYMBOL'], inplace=True)
            del self.lastcsvdata['PRICE']
            # del self.lastcsvdata['VOLUME']
            self.lastcsvdata.insert(3, 'BEGINDAY', '')
            self.lastcsvdata.insert(4, 'ENDDAY', '')
            self.lastcsvdata.insert(5, 'QUERYDAY', '')

            self.lastcsvfile = self.csvdir + '\\last.csv'
            if(os.path.isfile(self.lastcsvfile) == False):
                self.logfp.write("lastfile no exists,  %(file)s at %(time)s\n"%{'file':self.lastcsvfile, 'time' : time.strftime("%H:%M:%S")})
                self.lastcsvdata.to_csv(self.lastcsvfile, mode='w', encoding='gbk', index=0)#, header=False)
                self.lasttimedata = pd.read_csv(self.lastcsvfile, encoding='gbk')#, nrows=1)
            else:
                self.lasttimedata = pd.read_csv(self.lastcsvfile, encoding='gbk')#, nrows=1)
                for index, row in self.lastcsvdata.iterrows():
                    timedata = self.lasttimedata[ self.lasttimedata['SYMBOL'] == int(self.lastcsvdata.loc[index, ['SYMBOL']]['SYMBOL']) ]
                    # print(timedata)
                    if(timedata.empty == False):
                        row['BEGINDAY']     = self.date_formal(timedata.loc[index, 'BEGINDAY'])
                        row['ENDDAY']       = self.date_formal(timedata.loc[index, 'ENDDAY'])
                        row['QUERYDAY']     = self.date_formal(timedata.loc[index, 'QUERYDAY'])
                # print(self.lastcsvdata.loc[ index ])
            # print(self.lastcsvdata)
            self.logfp.write("%(symbol)s \n"%{'symbol':self.lastcsvdata})
            self.logfp.write("last csvdata time update at %(time)s\n"%{'time' : time.strftime("%H:%M:%S")})
            self.logfp.flush()

        except pd.errors.EmptyDataError as e:
            print(e)
        except urllib.error.URLError as e:
            if hasattr(e, 'code'):
                print("e.code")
                print(e.code)
            elif hasattr(e, 'reason'):
                print("e.reason")
                print(e.reason)
            self.logfp.write("getMarket urllib.error.URLError\n")
        except socket.timeout as e:
            print (type(e) )


    def task_close(self):
        self.logfp.close()

    def task_loop(self, start, end):
        if(start >= end):
            self.task_close()
            return
        pool = ThreadPoolExecutor(max_workers=64)
        nowitem = 0
        allitem = end - start
        task_list = []
        for index in range (start, end, 1):
            task_list.append(pool.submit(self.get_stock_update_process, index))
        for f in as_completed(task_list):
            f_ret = f.result()
            nowitem += 1
            print("all\tnow\tpercent\ttime(s)")
            print("%(all)s\t%(now)s\t%(per).05s%%\t%(time).05ss\n"%{'all': allitem, 'now' : nowitem, 'per' : 100*nowitem/allitem, 'time' : (time.time()-self.begintime)})
            
            if( nowitem % 5 == 0 ):
                self.lastcsvdata.to_csv(self.lastcsvfile, mode='w', encoding='gbk', index=0)#, header=False)
        #     logfp.write("%(all)s\t%(now)s\t%(per).05s%%\t%(time).05ss"%{'all': allitem, 'now' : nowitem, 'per' : 100*nowitem/allitem, 'time' : (time.time()-begintime)})
        #     logfp.flush() 
        
        self.lastcsvdata.to_csv(self.lastcsvfile, mode='w', encoding='gbk', index=0)#, header=False)



if __name__ == '__main__': 
    getCsv = getStockCsv()
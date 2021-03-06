# -*- coding: utf-8 -*-
import os
import pandas as pd


import _locale
_locale._getdefaultlocale = (lambda *args: ['zh_CN', 'utf8'])

MARKER_TYPE_A='AGU'
MARKER_TYPE_SZ_A='AGUSZ'
MARKER_TYPE_SH_A='AGUSH'
MARKER_TYPE_B='BGU'
MARKER_TYPE_SZ_B='BGUSZ'
MARKER_TYPE_SH_B='BGUSH'
MARKER_TYPE_H='HGU'
MARKER_TYPE_SZ_ZXB='AGUZXBSZ'
MARKER_TYPE_SZ_CYB='CYBSZ'
MARKER_TYPE_SH_KCB='KCBSH'


BASE_DATA_PATH = os.path.dirname(os.path.abspath(__file__)) + "\\..\\csv"
A_MARKER_DATA_PATH = BASE_DATA_PATH + "\\.data.csv"



def stock_CodeIdentify(codestr):
    if codestr[0] == '0':#国债/指数
        if codestr[1:3] == '00':
        #沪市：上证指数、沪深300指数、中证指数
        # 深市：A股主板证券
            return MARKER_TYPE_SZ_A
        elif codestr[1:3] == '01':
        # 深市：A股主板证券
            return MARKER_TYPE_SZ_A
        elif codestr[1:3] == '02':
        # 深市：A股中小板证券
            return MARKER_TYPE_SZ_ZXB
        elif codestr[1:3] == '03':
        # 深市：A股中小板证券
            return MARKER_TYPE_H
        elif codestr[1] == '3':
        # 深市：A股认购或认股权证
            return MARKER_TYPE_SZ_A
        elif codestr[1] == '7':
        # 深市：A股增发
            return MARKER_TYPE_SZ_A
        elif codestr[1] == '8':
        # 深市：A股配股权证
            return MARKER_TYPE_SZ_A
        elif codestr[1:3] == '09':#2000前发行的国债
            pass
        elif codestr[1:3] == '10':#2000-2009发行的国债
            pass
        elif codestr[1:3] == '90':#新国债质押式回购质押券出入库
            pass
        elif codestr[1:3] == '99':#新国债质押式回购质押券出入库
            pass
        return ''
    elif codestr[0] == '1':#债券
        if codestr[1:3] == '00':
        #沪市：可转债，其中1009**用于转债回售
        # 深市：国债
            pass
        elif codestr[1:3] == '01':
        # 深市：国债
            pass
        elif codestr[1:3] == '08':
        # 深市：贴债
            pass
        elif codestr[1:3] == '09':
        # 深市：地方政府债
            pass
        elif codestr[1:3] == '10':#可转债
            pass
        elif codestr[1:3] == '11':
        # 深市：企业债
            pass
        elif codestr[1:3] == '12':
        #沪市：可转债
        # 深市：公司债
            pass
        elif codestr[1:3] == '13':#可转债
            pass
        elif codestr[1:3] == '15':
        # 深市：认购股权和债券分离的可转换公司债券
            pass
        elif codestr[1:3] == '20':
        #沪市：企业债(席位托管方式)
        # 深市：可转换债券
            pass
        elif codestr[1:3] == '21':
        #沪市：资产证券化
        # 深市：可转换债券
            pass
        elif codestr[1:3] == '26':
        #沪市：分离交易的可转债
        # 深市：可转换债券
            pass
        elif codestr[1:3] == '29':
        #沪市：企业债(席位托管方式)
        # 深市：可转换债券
            pass
        elif codestr[1] == '2':
        # 深市：可转换债券
            pass
        elif codestr[1] == '3':
        # 深市：债券回购
            pass
        elif codestr[1] == '5':
        # 深市：开放式基金
            pass
        elif codestr[1] == '6':
        # 深市：开放式基金
            pass
        elif codestr[1:3] == '81':
        #沪市：可转债转股
        # 深市：证券投资资金
            pass
        elif codestr[1] == '8':
        # 深市：证券投资资金
            pass
        elif codestr[1:3] == '90':#可转债转股
            pass
        elif codestr[1:3] == '91':#可转债转股
            pass
        return ''
    elif codestr[0] == '2':#回购
        if codestr[1:3] == '01':
        #沪市：国债回购(席位托管方式)
        # 深市：B股证券
            # return MARKER_TYPE_SZ_B
            pass
        elif codestr[1] == '0':
        # 深市：B股证券
            return MARKER_TYPE_SZ_B
            pass
        elif codestr[1] == '8':
        # 深市：B股权证
            return MARKER_TYPE_SZ_B
            pass
        elif codestr[1:3] == '02':#企业债回购
            pass
        elif codestr[1:3] == '03':#国债买断式回购
            pass
        elif codestr[1:3] == '04':#新质押式国债回购(账户托管方式)
            pass
        return ''
    elif codestr[0] == '3':#期货
        if codestr[1:3] == '10':#国债期货(暂停交易)
            pass
        elif codestr[1] == '0':
        # 深市：创业板证券
            return MARKER_TYPE_SZ_CYB
        elif codestr[1] == '6':
        # 深市：网络投票证券
            pass
        elif codestr[1] == '7':
        # 深市：创业板增发
            return MARKER_TYPE_SZ_CYB
        elif codestr[1] == '8':
        # 深市：创业板权证
            return MARKER_TYPE_SZ_CYB
        elif codestr[1] == '9':
        # 深市：中和或成分指数/成交量统计指标
            pass
        return ''
    elif codestr[0] == '4':#备用
        return ''
    elif codestr[0] == '5':#基金/权证
        if codestr[1:3] == '00':#契约型封闭式基金
            pass
        elif codestr[1:3] == '10':#交易型开放式指数证券投资基金
            pass
        elif codestr[1:3] == '19':#开发式基金申赎
            pass
        elif codestr[1:3] == '21':#开发式基金认购
            pass
        elif codestr[1:3] == '22':#开发式基金跨市场转托管
            pass
        elif codestr[1:3] == '23':#开发式基金分红
            pass
        elif codestr[1:3] == '24':#开发式基金基金转换
            pass
        elif codestr[1:3] == '80':#权证(含股东权证、公司权证)
            pass
        elif codestr[1:3] == '82':#权证行权
            pass
        return ''
    elif codestr[0] == '6':#A股
        if codestr[1:3] == '00':#A股证券
            return MARKER_TYPE_SH_A
        elif codestr[1:3] == '01':#A股证券
            return MARKER_TYPE_SH_A
        elif codestr[1:3] == '03':#A股证券
            return MARKER_TYPE_SH_A
        elif codestr[1:3] == '88':#A股科创板
            return MARKER_TYPE_SH_KCB
        return MARKER_TYPE_SH_A
    elif codestr[0] == '7':#非交易业务(发行、权益分配)
        if codestr[1:3] == '00':#配股
            pass
        elif codestr[1:3] == '02':#职工股配股
            pass
        elif codestr[1:3] == '04':#持股配转债
            pass
        elif codestr[1:3] == '05':#基金扩募
            pass
        elif codestr[1:3] == '06':#要约收购
            pass
        elif codestr[1:3] == '30':#申购、增发
            pass
        elif codestr[1:3] == '31':#持股增发
            pass
        elif codestr[1:3] == '33':#可转债申购
            pass
        elif codestr[1:3] == '35':#基金申购
            pass
        elif codestr[1:3] == '38':#网上投票
            pass
        elif codestr[1:3] == '40':#申购款或增发款
            pass
        elif codestr[1:3] == '41':#申购或增发配号
            pass
        elif codestr[1:3] == '43':#可转债发债款
            pass
        elif codestr[1:3] == '44':#可转债配号
            pass
        elif codestr[1:3] == '45':#基金申购款
            pass
        elif codestr[1:3] == '46':#基金申购配号
            pass
        elif codestr[1:3] == '51':#国债分销
            pass
        elif codestr[1:3] == '60':#配股
            pass
        elif codestr[1:3] == '62':#职工股配股
            pass
        elif codestr[1:3] == '64':#持股配转债
            pass
        elif codestr[1:3] == '80':#申购、增发
            pass
        elif codestr[1:3] == '81':#持股增发
            pass
        elif codestr[1:3] == '83':#可转债申购
            pass
        elif codestr[1:3] == '88':#网络投票
            pass
        elif codestr[1:3] == '90':#申购款或增发款
            pass
        elif codestr[1:3] == '91':#申购或增发配号
            pass
        elif codestr[1:3] == '93':#可转债申购款
            pass
        elif codestr[1:3] == '94':#可转债配号
            pass
        elif codestr[1:3] == '99':#指定交易(含指定交易、撤销指定、回购指定撤销、A股密码服务等)
            pass
        return ''
    elif codestr[0] == '8':#备用
        return ''
    elif codestr[0] == '9':#B股
        if codestr[1:3] == '00':#B股证券
            return MARKER_TYPE_SH_B
        elif codestr[1:3] == '38':#网上投票(B股)
            return MARKER_TYPE_SH_B
        elif codestr[1:3] == '39':#B股网络投票密码服务(现仅用939988)
            return MARKER_TYPE_SH_B
        return 'B'
    else:
        return ''


def stock_IdentifyType(type):
    if type == 0:#itor
        StockItData = pd.read_csv(A_MARKER_DATA_PATH, iterator=True)#SYMBOL	NAME	DATE	VOLUME
    else:
        StockItData = pd.read_csv(A_MARKER_DATA_PATH)#, iterator=True)#SYMBOL	NAME	DATE	VOLUME
    return StockItData


def stock_GetLocalData(codename='000001平安银行'):
    stockfile = BASE_DATA_PATH + "\\%(name)s.csv"%{'name' : codename}
    print(stockfile)
    if (os.path.exists(stockfile)):
        stockdata = pd.read_csv(stockfile, encoding='gbk')
        # print(stockdata)
        return stockdata
    else:
        return pd.DataFrame()

# if __name__ == "__main__": 
#     # stock_CodeIdentify('003816')
#     # stock_IdentifyType()
#     stock_GetLocalData('000001平安银行')
#     stock_GetLocalData('000001平安行')
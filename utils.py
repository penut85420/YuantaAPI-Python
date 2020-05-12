import os
import re
import requests
from loguru import logger
from datetime import timedelta
from datetime import datetime as dt

def GetOptionCode():
    logger.info('Retrieving option code list.')
    # Find all date
    url = 'https://tw.screener.finance.yahoo.net/future/aa03?opmr=optionfull&opcm=WTXO'
    with requests.get(url) as r:
        tag = re.escape('</option>')
        p = re.compile(r'([\dW]+)%s' % tag)
        date = p.findall(r.text)

    # Find all price in each date
    code_list = []
    for d in date:
        y = int(d[:4]) % 10
        m = int(d[4:6]) - 1
        w = d[6:]
        if not w: w = 'OO'
        buy = 'ABCDEFGHIJKL'
        sell = 'MNOPQRSTUVWX'

        url = f'https://tw.screener.finance.yahoo.net/future/aa03?opmr=optionfull&opcm=WTXO&opym={d}'
        tag = re.escape('<td class="ext-big-tb-center">')
        p = re.compile(r'%s(\d+)' % tag)
        with requests.get(url) as r: 
            r = requests.get(url)
            prices = p.findall(r.text)
        a = int(prices[0])
        b = int(prices[-1])
        logger.info(f'{d:<8s} price range ({a:5}, {b:5}), middle: {(a+b)//2}.')
        for p in prices:
            code_list.append(f'TX{w[1]}{int(p):05d}{buy[m]}{y}')
            code_list.append(f'TX{w[1]}{int(p):05d}{sell[m]}{y}')

    return code_list

def walk(path):
    for dir_path, _, file_list in os.walk(path):
        for file_name in file_list:
            full_path = os.path.join(dir_path, file_name)
            yield full_path

def remove_dir(dir_path):
    for full_path in walk(dir_path):
        os.remove(full_path)
    os.removedirs(dir_path)

def clear_log(path):
    for dir_path, dir_list, file_list in os.walk(path):
        date = dt.now().strftime('%Y%m%d')
        date2 = (dt.now() - timedelta(days=1)).strftime('%Y%m%d')
        for dir_name in dir_list:
            if dir_name != date and dir_name != date2:
                remove_dir(os.path.join(dir_path, dir_name))

        for file_name in file_list:
            full_path = os.path.join(dir_path, file_name)
            open(full_path, 'w').close()

if __name__ == '__main__':
    GetOptionCode()
    # clear_log('./Logs')

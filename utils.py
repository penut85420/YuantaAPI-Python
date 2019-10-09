import re
import requests
from loguru import logger

def GetOptionCode():
    logger.info('Retrieving option code list.')
    # Find all date
    url = 'https://tw.screener.finance.yahoo.net/future/aa03?opmr=optionfull&opcm=WTXO'
    r = requests.get(url)
    tag = re.escape('</option>')
    p = re.compile('([\dW]+)%s' % tag)
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
        p = re.compile('%s(\d+)' % tag)
        r = requests.get(url)
        prices = p.findall(r.text)
        logger.info(f'{d:<8s} price range from {int(prices[0]):5} to {int(prices[-1]):5}.')
        for p in prices:
            code_list.append(f'TX{w[1]}{int(p):05d}{buy[m]}{y}')
            code_list.append(f'TX{w[1]}{int(p):05d}{sell[m]}{y}')

    return code_list

import argparse
import ctypes
import datetime
import json
import os
os.environ['LOGURU_AUTOINIT'] = 'False'
import sys

import dateutil.relativedelta

import comtypes
import comtypes.client
import wx
from loguru import logger

link_status = {
    -2: 'Connection Failed',
    -1: 'Connection Broken',
    0: 'Connection Idle',
    1: 'Connection Ready',
    2: 'Connection Success'
}

link_status_logtype = {
    -2: logger.error,
    -1: logger.error,
    0: logger.info,
    1: logger.info,
    2: logger.success
}

class YuantaQuoteAXCtrl:
    def __init__(self, parent):
        self.parent = parent

        container = ctypes.POINTER(comtypes.IUnknown)()
        control = ctypes.POINTER(comtypes.IUnknown)()
        guid = comtypes.GUID()
        sink = ctypes.POINTER(comtypes.IUnknown)()

        ctypes.windll.atl.AtlAxCreateControlEx(
            'YUANTAQUOTE.YuantaQuoteCtrl.1',
            self.parent.Handle, None,
            ctypes.byref(container),
            ctypes.byref(control),
            ctypes.byref(guid), sink
        )
        self.ctrl = comtypes.client.GetBestInterface(control)
        self.sink = comtypes.client.GetEvents(self.ctrl, self)
        self.update_savedir()

    def time(self):
        return f'{datetime.datetime.now():%H:%M:%S.%f}'

    def update_savedir(self):
        self.date = datetime.datetime.now().strftime('%Y%m%d')
        self.save_dir = f'./data/{self.date}/'
        n = datetime.datetime.now()
        day = n.day if n.hour < 5 else n.day + 1
        self.next_day = datetime.datetime(n.year, n.month, day, 5, 30)

        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def savedir(self, code):
        if datetime.datetime.now() > self.next_day:
            self.update_savedir()
        return os.path.join(self.save_dir, f'{code}.csv')

    def Config(self, host, port, username, password):
        self.Host = host
        self.Port = port
        self.Username = username
        self.Password = password

    def XXF(self):
        """計算期貨商品代碼"""
        today = datetime.date.today()
        day = datetime.date.today().replace(day=1)

        while day.weekday() != 2:
            day = day + datetime.timedelta(days=1)
        day = day + dateutil.relativedelta.relativedelta(days=14)

        if day < today:
            day = day + dateutil.relativedelta.relativedelta(months=1)

        codes = 'ABCDEFGHIJKL'
        y = day.year % 10
        m = codes[day.month - 1]

        return f'{m}{y}'

    def XF(self, code):
        return f'{code}{self.XXF()}'

    def Logon(self):
        self.ctrl.SetMktLogon(self.Username, self.Password, self.Host, self.Port, 1, 0)

    def OnGetMktAll(
        self, symbol, refPri, openPri, highPri, lowPri, upPri, dnPri,
        matchTime, matchPri, matchQty, tolMatchQty,
        bestBuyQty, bestBuyPri, bestSellQty, bestSellPri,
        fdbPri, fdbQty, fdsPri, fdsQty, reqType
        ):
        matchTime = f'{matchTime[:2]}:{matchTime[2:4]}:{matchTime[4:6]}.{matchTime[6:]}'
        with open(self.savedir(symbol), 'a', encoding='UTF-8') as fout:
            record = [
                f'{self.time()},{openPri},{highPri},{lowPri}',
                f',{matchTime},{matchPri},{matchQty},{tolMatchQty}',
                f',{bestBuyQty},{bestBuyPri},{bestSellQty},{bestSellPri}'
            ]
            print(''.join(record), file=fout)

    def OnMktStatusChange(self, status, msg, reqType):
        link_status_logtype[status](f'{link_status[status]}')
        if status != 2:
            return

        code_list = load_json('./code.json')
        for code in code_list['stock']:
            result = self.ctrl.AddMktReg(code, 2, reqType, 0)
            logger.trace(f'Registered {code}, result: {result}')
        logger.success('Stock registration done.')

        for code in code_list['future']:
            code = self.XF(code)
            result = self.ctrl.AddMktReg(code, 2, reqType, 0)
            logger.trace(f'Registered {code}, result: {result}')
        logger.success('Future registration done.')

def load_json(fpath):
    with open(fpath, 'r', encoding='UTF-8') as f:
        return json.load(f)

def ConnectionConfiguration(args):
    port_set = set([80, 82, 443, 442])

    if args.port not in port_set:
        logger.error('Port is not set to support ports, might cause connection failed.')

    config = load_json('./config.json')
    config['port'] = args.port
    if args.is_night and (args.port != 442 or args.port != 82):
        config['port'] = 442
        logger.warning('')
    config['host'] = 'apiquote.yuantafutures.com.tw'
    logger.info(f'Connection Target {config["host"]}:{config["port"]}')
    return config

def LoggerConfiguration(args):
    log_format = '{time:HH:mm:ss.SSSSSS} | <lvl>{level: ^9}</lvl> | {function}:{line} - {message}'
    verbose_set = set(['TRACE', 'DEBUG', 'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL'])

    logger.add(sys.stderr, level='INFO', format=log_format)

    args.verbose = args.verbose.upper()
    if args.verbose not in verbose_set:
        logger.warning(f'Verbose level "{args.verbose}" is not one of TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR or CRITICAL')
        logger.warning(f'Verbose level will be set to TRACE')
        args.verbose = 'TRACE'

    logger.add(
        f'{datetime.date.today():%Y%m%d}.log',
        rotation='1 day',
        retention='7 days',
        level=args.verbose,
        encoding='UTF-8',
        format=log_format
    )

def main():
    parser = argparse.ArgumentParser(description='Taiwan Stock, Future & Option Quote')
    parser.add_argument('-p', dest='port', type=int, default=443, help='set connection port')
    parser.add_argument('-n', '--night', dest='is_night', action='store_true', help='connect to night tape')
    parser.add_argument('-v', '--verbose', dest='verbose', type=str, default='TRACE', help='set logging level')
    args = parser.parse_args()

    app = wx.App()
    frame = wx.Frame(parent=None, id=wx.ID_ANY, title='Yuanta.Quote') # pylint: disable=no-member
    frame.Hide()

    LoggerConfiguration(args)
    config = ConnectionConfiguration(args)

    quote = YuantaQuoteAXCtrl(frame)
    quote.Config(**config)
    quote.Logon()

    app.MainLoop()

if __name__ == '__main__':
    main()

"""
Host IP: 203.66.93.84
Host Domain: apiquote.yuantafutures.com.tw
T Port: 80 or 443
T+1 Port: 82 or 442
"""

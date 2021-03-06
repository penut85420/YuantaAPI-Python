import wx
import os
import sys
import json
import time
import ctypes
import comtypes
import argparse
import calendar
import datetime
import threading

import comtypes.client
import dateutil.relativedelta
os.environ['LOGURU_AUTOINIT'] = 'False'

from loguru import logger
from utils import GetOptionCode, clear_log

link_status = {
   -2: 'Connection failed.',
   -1: 'Connection broken.',
    0: 'Connection idled.',
    1: 'Connection ready.',
    2: 'Connection success.'
}

link_status_logtype = {
    -2: logger.error,
    -1: logger.error,
    0: logger.info,
    1: logger.info,
    2: logger.success
}

class YuantaQuoteAXCtrl:
    def __init__(self, parent, args):
        self.parent = parent
        self.args = args
        self.terminate = False

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
        return f'{get_time():%H:%M:%S.%f}'

    def update_savedir(self):
        self.date = get_time().strftime('%Y%m%d')
        if self.is_day():
            self.save_dir = f'./data_day/{self.date}/'
        else:
            self.save_dir = f'./data_night/{self.date}/'
        n = get_time()
        if n.hour >= 5:
            n += datetime.timedelta(days=1)
        self.next_day = datetime.datetime(n.year, n.month, n.day, 5, 30)

        if not os.path.exists(self.save_dir):
            logger.info(f'Switch folder to {self.save_dir}')
            os.makedirs(self.save_dir)

    def savedir(self, code):
        if get_time() > self.next_day:
            self.update_savedir()

        return os.path.join(self.save_dir, f'{code}.csv')

    def UpdateDayNight(self):
        while True:
            if self.terminate:
                return

            if self.is_day() and not self.is_day_port():
                self.Port = 443
                logger.info('Change connection port to 443.')
                self.update_savedir()
                if not self.args.no_option:
                    RenewOptionCodeList()
                self.Logon()
            elif not self.is_day() and self.is_day_port():
                self.Port = 442
                logger.info('Change connection port to 442.')
                self.update_savedir()
                self.Logon()

            time.sleep(1)

    def ClearLog(self):
        while True:
            if self.terminate:
                return

            clear_log('./Logs')
            time.sleep(300)

    def is_day_port(self):
        if self.Port == 443:
            return True
        if self.Port == 80:
            return True
        return False

    def is_day(self):
        """
        07:00~14:45 - Day
        14:45~07:00 - Night
        """
        now = get_time()
        day_begin = now.replace(hour=7, minute=0, second=0)
        day_end = now.replace(hour=14, minute=50, second=0)

        if now < day_begin:
            return False
        if now > day_end:
            return False
        return True

    def is_trade_time(self):
        """
        08:45~13:45 - Day
        15:00~05:00 - Night
        """
        now = get_time()
        day_begin = now.replace(hour=8, minute=45, second=0)
        day_end = now.replace(hour=13, minute=45, second=0)
        night_begin = now.replace(hour=15, minute=00, second=0)
        night_end = now.replace(hour=5, minute=0, second=0)

        if now >= day_begin and now <= day_end:
            return True
        if now <= night_end:
            return True
        if now >= night_begin:
            return True

        return False

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
        logger.info(f'Connecting to {self.Host}:{self.Port}')
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

        if status < 0:
            logger.info('Try to login again.')
            if self.is_trade_time():
                logger.info('Reconnection in trade time will be wait for 1 second')
                time.sleep(1)
            else:
                logger.info('Reconnection beyond trade time will wait for 1 minutes')
                time.sleep(60)
            self.Logon()

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

        if not self.args.no_option:
            for code in code_list['option']:
                result = self.ctrl.AddMktReg(code, 2, reqType, 0)
                logger.trace(f'Registered {code}, result: {result}')
            logger.success('Option registration done.')

def load_json(fpath):
    with open(fpath, 'r', encoding='UTF-8') as f:
        return json.load(f)

def save_json(fpath, obj):
    with open(fpath, 'w', encoding='UTF-8') as f:
        json.dump(obj, f)

def ConnectionConfiguration(args):
    config = load_json('./config.json')
    config['port'] = 442 if args.is_night else 443
    config['host'] = '203.66.93.84'

    return config

def LoggerConfiguration(args):
    log_format = (
        '{time:YYYY-MM-DD HH:mm:ss.SSSSSS} | '
        '<lvl>{level: ^9}</lvl> | '
        '{function}:{line} - {message}'
    )
    verbose_set = set(['TRACE', 'DEBUG', 'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL'])

    logger.add(sys.stderr, level='INFO', format=log_format)

    args.verbose = args.verbose.upper()
    if args.verbose not in verbose_set:
        logger.warning(
            f'Verbose level "{args.verbose}" is not one of '
            'TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR or CRITICAL')
        logger.warning(f'Verbose level will be set to DEBUG')
        args.verbose = 'DEBUG'

    logger.add(
        f'./logs_quote/quote.log',
        rotation='7 day',
        retention='180 days',
        level=args.verbose,
        encoding='UTF-8',
        format=log_format
    )

def RenewOptionCodeList():
    option_code_list = GetOptionCode()
    code_list = load_json('./code.json')
    code_list['option'] = option_code_list
    save_json('./code.json', code_list)

def get_time():
    """Get the absolute time of UTC+8."""
    d = datetime.timedelta(hours=8)
    t = datetime.datetime.utcnow()
    t += d

    return t

def main():
    parser = argparse.ArgumentParser(
        description='Taiwan Stock, Future & Option Quote')
    parser.add_argument(
        '-n', '--night', dest='is_night',
        action='store_true', help='connect to night tape')
    parser.add_argument(
        '-v', '--verbose', dest='verbose',
        type=str, default='DEBUG', help='set logging level')
    parser.add_argument(
        '--no-option', dest='no_option',
        action='store_true', default=False, help='not to collect option quote data'
    )
    args = parser.parse_args()

    while True:
        try:
            app = wx.App()
            # pylint: disable=no-member
            frame = wx.Frame(
                parent=None,
                id=wx.ID_ANY,
                title='Yuanta.Quote'
            )
            frame.Hide()

            LoggerConfiguration(args)
            if not args.no_option:
                RenewOptionCodeList()

            config = ConnectionConfiguration(args)
            quote = YuantaQuoteAXCtrl(frame, args)
            quote.Config(**config)
            quote.Logon()

            threading.Thread(target=quote.UpdateDayNight).start()
            threading.Thread(target=quote.ClearLog).start()
            app.MainLoop()
        except KeyboardInterrupt:
            print('Bye!')
            exit(0)
        except Exception as e:
            logger.critical(str(e))

    quote.terminate = True

if __name__ == '__main__':
    main()

"""
Host IP: 203.66.93.84
Host Domain: apiquote.yuantafutures.com.tw
T Port: 80 or 443
T+1 Port: 82 or 442
"""

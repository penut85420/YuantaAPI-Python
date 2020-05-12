import os, re, sys
import numpy as np
import pandas as pd
import datetime as dt

CODE = sys.argv[1]
NIGHT = 'night'
DAY = 'day'
fout = open(f'std_{CODE}.csv', 'w', encoding='UTF-8')

def main():
    for dir_path, _, file_list in os.walk(f'./data_{CODE}'):
        for file_name in sorted(file_list):
            if 'TXF' in file_name:
                full_path = os.path.join(dir_path, file_name)
                print(full_path, end='\r')
                ds, yy, mm, dd = mk_ds(full_path)
                std = ds[:, -1].std()
                if CODE == NIGHT:
                    a, b = special_time(ds)
                    print(f'{yy}/{mm:02d}/{dd:02d},{std:.4f},{a:.4f},{b:.4f}', file=fout)
                else:
                    print(f'{yy}/{mm:02d}/{dd:02d},{std:.4f}', file=fout)
    print('\nDone')

def special_time(ds):
    n = ds[0][0]
    n1 = n.replace(hour=22, minute=30)
    a, b = [], []
    for d in ds:
        if d[0] <= n1:
            a.append(d[-1])
        else:
            b.append(d[-1])
    a, b = map(np.array, (a, b))
    return map(np.std, (a, b))

def mk_ds(path):
    ds, yy, mm, dd = load_csv(path)
    now = ds[0][0]
    now = now.replace(second=0, microsecond=0)
    now += dt.timedelta(minutes=3)
    o = h = l = c = ds[0][1]
    dds = []

    def append():
        t = dt.datetime(year=yy, month=mm, day=dd, hour=now.hour, minute=now.minute)
        if now.hour < 7 and now.hour >= 0:
            t += dt.timedelta(days=1)
        dds.append([t, o, h, l, c])
        return t

    for ts, price in ds[1:]:
        if ts < now:
            h = max(h, price)
            l = min(l, price)
            c = price
        else:
            now = append()
            o = h = l = c = price
            now += dt.timedelta(minutes=3)
    append()
    return np.array(dds), yy, mm, dd

def load_csv(path):
    date = re.findall('\d{8}', path)[0]
    yy = date[0:4]
    mm = date[4:6]
    dd = date[6:8]
    yy, mm, dd = map(int, (yy, mm, dd))
    open_time = dt.datetime(year=yy, month=mm, day=dd)
    close_time = dt.datetime(year=yy, month=mm, day=dd)
    if CODE == DAY:
        open_time = open_time.replace(hour=8, minute=45)
        close_time = close_time.replace(hour=13, minute=45)
    else:
        open_time = open_time.replace(hour=15, minute=0)
        close_time = close_time.replace(hour=5, minute=00)
        close_time += dt.timedelta(days=1)

    ds = []
    with open(path, 'r', encoding='UTF-8') as f:
        for line in f.read().strip().split('\n'):
            line = line.split(',')
            if len(line) < 5:
                continue

            ts = parse_timestamp(line[4])
            if ts is None:
                continue

            price = int(line[5])
            if price == 0:
                continue

            ts = ts.replace(year=yy, month=mm, day=dd)
            if ts.hour < 7 and ts.hour >= 0:
                ts += dt.timedelta(days=1)
            if ts < open_time or ts > close_time:
                continue
            ds.append([ts, price])
    return ds, yy, mm, dd

def parse_timestamp(t):
    try:
        return dt.datetime.strptime(t, '%H:%M:%S.%f')
    except:
        return None

if __name__ == '__main__':
    # ds, yy, mm, dd = mk_ds('./data_night/20200302/TXFC0.csv')
    # ds = np.array(ds)
    # print(ds, ds.shape)
    # input()
    main()

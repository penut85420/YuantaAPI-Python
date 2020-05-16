import os
import re
import argparse
import subprocess as sp

def compress(tag, archieved_dir):
    for dir_path, _, file_list in os.walk(f'./data_{tag}'):
        for file_name in file_list:
            full_path = os.path.join(dir_path, file_name)
            date = re.findall(r'\d{8}', full_path)[0]
            fn, ext = os.path.splitext(file_name)
            table_name = f't{date}_{fn}_{tag}.7z'
            print(f'{table_name:-20s}', end='\r')
            out_dir = os.path.join(archieved_dir, date, table_name)
            os.makedirs(archieved_dir, exist_ok=True)
            if not os.path.exists(out_dir):
                sp.call(['7z', 'a', out_dir, full_path], stdout=sp.PIPE)

def main():
    parser = argparse.ArgumentParser(description='Compress quote file separately')
    parser.add_argument(
        '-o', '--output', default='./archieved',
        help='the folder which archived file will be store'
    )
    parser.add_argument(
        '-d', '--day', type=bool, default=True,
        help='whether to compress day quote file'
    )
    parser.add_argument(
        '-n', '--night', type=bool, default=True,
        help='whether to compress day quote file'
    )
    args = parser.parse_args()

    if args.day:
        compress('day', args.output)
    if args.night:
        compress('night', args.output)

if __name__ == "__main__":
    main()

import os
import re
import subprocess as sp

archieved_dir = './archieved'

def archieve(tag):
    for dir_path, _, file_list in os.walk(f'./data_{tag}'):
        for file_name in file_list:
            full_path = os.path.join(dir_path, file_name)
            date = re.findall(r'\d{8}', full_path)[0]
            fn, ext = os.path.splitext(file_name)
            table_name = f't{date}_{fn}_{tag}.7z'
            print(table_name, end='\r')
            out_dir = os.path.join(archieved_dir, date, table_name)
            os.makedirs(archieved_dir, exist_ok=True)
            if not os.path.exists(out_dir):
                sp.call(['7z', 'a', out_dir, full_path], stdout=sp.PIPE)

def main():
    archieve('day')
    archieve('night')

if __name__ == "__main__":
    main()

import os
import argparse
import subprocess as sp

def main(tag, inn_dir, output):
    if inn_dir.startswith('./'):
        inn_dir = inn_dir[2:]

    r = []
    for dir_path, _, file_list in os.walk(inn_dir):
        for file_name in file_list:
            fp = os.path.join(dir_path, file_name)
            if tag in file_name:
                r.append(fp)

    if not output.endswith('.7z'):
        output += '.7z'

    sp.call(['7z', 'a', output, '-spf'] + r)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Retrieve all file with tag into .7z')
    parser.add_argument('-i', '--input', help='target directory to search')
    parser.add_argument('-t', '--tag', help='tag need to be contained in file name')
    parser.add_argument('-o', '--output', help='name of output .7z file')
    args = parser.parse_args()

    main(args.tag, args.input, args.output)

import re
import sys
import subprocess as sp

def main():
    n, h, l = get_profile()
    d = {'高效能': l, '省電': h, '平衡': l}
    sp.call(['powercfg', '/s', d[n]])

    n, _, _ = get_profile()
    print(f'現在使用的電源配置為{n}')

def get_profile():
    out = get_pwl()
    high_profile = re.findall(r'GUID: (.*)  \(高效能', out)[0]
    low_profile = re.findall(r'GUID: (.*)  \(省電', out)[0]
    now_profile = re.findall(r'\((.*)\) \*', out)[0]

    return now_profile, high_profile, low_profile

def get_pwl():
    proc = sp.Popen(['powercfg', '/l'], stdout=sp.PIPE)
    out, err = proc.communicate()
    out = out.decode('CP950')

    return out

if __name__ == "__main__":
    main()

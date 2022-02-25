import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("-u", help="用户名字典路径")
parser.add_argument("-p", help="密码字典路径")
args = parser.parse_args()
user_tem = "./captcha_break_http_server/user_tem.txt"
passwd_tem = "./captcha_break_http_server/passwd_tem.txt"


def win(sum):

    if sum == 0:  # 第一次巡行用户指定的字典
        cmd = "blaster_win.exe -c conf.yaml -u " + args.u + " -p " + args.p + " -o res.txt"
    else:  # 二次之后运行因为验证码没有通过的字典
        cmd = "blaster_win.exe -c conf.yaml -u " + user_tem + " -p " + passwd_tem + " -o res.txt"
    p = subprocess.Popen(cmd, shell=True)
    p.wait()  # 等待子进程结束，并返回状态码；


def xunhuan():  # 若未找到账户名与密码，把因为输入验证码错误而没有通过的账号与密码再提取出来重新运行
    f = open("res.txt", 'r', encoding="utf-8")
    name = []
    passwd = []
    number = 0
    for x in f:
        na = x.split()
        number += 1
        if number != 1:
            name.append(na[2])
            passwd.append(na[3])
    f.close()
    # 去重复
    name = set(name)
    passwd = set(passwd)
    # 保存数据
    f_name = open(user_tem, 'w')
    for i in name:
        f_name.write(i + '\n')
    f_name.close()
    f_passwd = open(passwd_tem, 'w')
    for i in passwd:
        f_passwd.write(i + '\n')
    f_passwd.close()


if __name__ == '__main__':
    win(0)
    while True:
        re = input("请查看res.txt内容，若继续跑则输入y,否则输入n:")
        if re == 'n':
            break
        xunhuan()
        win(1)

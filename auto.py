import subprocess
import os
import datetime
from threading import Thread
import time

ukui_list = [
             "debian-packages",
             "ukwm",
             "ukui-biometric-auth",
             "ukui-biometric-manager",
             "ukui-screensaver",
             "ukui-greeter",
             "kylin-video",
             "peony",
             "ukui-panel",
             "ukui-indicators",
             "ukui-control-center",
             "ukui-menu",
             "ukui-menus",
             "ukui-power-manager",
             "ubuntukylin-theme",
             #"indicator-china-weather",
             "biometric-authentication",
             "kylin-burner",
             "peony-extensions",
             "ukui-session-manager",
             "kylin-display-switch",
             "ukui-desktop-environment",
             "ukui-window-switch",
             #"ukui-screensaver-qt",
             "ukui-media",
             "ukui-settings-daemon",
             #"Genisys",
             #"kylin-burner-new",
             #"ukui-desktop",
             #"ukui-screensaver-redesign",
             #"ukui-backgrounds",
             #"caja",


             #"ubuntu-kylin-wizard",
             #"youker-assistant",
             #"ubuntukylin-default-settings",
             #"ubuntu-kylin-software-center",
             #"indicator-china-weather",
             #"ubuntukylin-wallpapers",
             #"ubuntu-kylin-docs",
             #"fcitx-qimpanel",
            ]

ppa = "ppa:readlnh/test"

def clone(name):
    archivecmd = "git clone https://github.com/ukui/" + name + ".git"
    print(archivecmd)
    process = subprocess.Popen(archivecmd, shell=True)
    process.wait()
    archivecmdreturncode = process.returncode
    if archivecmdreturncode != 0:
        print(name + " clone error")
    print("\n")


def pull(name):
    os.chdir('./' + name)
    archivecmd = "git pull"
    process = subprocess.Popen(archivecmd, shell=True)
    process.wait()
    archivecmdreturncode = process.returncode
    if archivecmdreturncode != 0:
        print("pull error \n")
    os.chdir('../')

def checkout(name):
    os.chdir('./' + name)
    archivecmd = "git checkout debian"
    print(archivecmd)
    process = subprocess.Popen(archivecmd, shell=True)
    process.wait()
    archivecmdreturncode = process.returncode
    os.chdir('../')
    return archivecmdreturncode

    #if archivecmdreturncode != 0:
    #    print(name + " checkout error")
    #print("\n")



def debuild(name):
    os.chdir('./' + name)
    archivecmd = "yes | debuild -S -sa"
    process = subprocess.Popen(archivecmd, shell=True)
    process.wait()
    archivecmdreturncode = process.returncode
    os.chdir('../')
    if archivecmdreturncode != 0:
        print("debuild error\n")
    else:
        Thread(target=dput,args=(ppa, name))


def clone_all():
    for i in ukui_list:
        clone(i)

def pull_all():
    for i in ukui_list:
        print("pull" + " " + i)
        pull(i)
        print("\n")

def debuild_all():
    for i in ukui_list:
        debuild(i)

def checkout_all():
    for i in ukui_list:
        checkout(i)

def mkbuilddeps(name):
    archivecmd = 'yes | echo "123123" | sudo -S mk-build-deps -i ' + './' + name + "/debian/control"
    print(archivecmd)
    process = subprocess.Popen(archivecmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    process.wait()
    archivecmdreturncode = process.returncode
    if archivecmdreturncode != 0:
        print("安装依赖失败 error\n")

def deletefile(namedir):
    name = namedir.split("/")[-1]
    print(name + " 开始删除debian目录")
    archivecmd = "rm -rf " + namedir + "/debian"
    print(archivecmd)
    process = subprocess.Popen(archivecmd, shell=True)
    process.wait()
    archivecmdreturncode = process.returncode
    if archivecmdreturncode != 0:
        print("delete error \n")


def delete_build():
    archivecmd = "rm -rf *.deb *.xz *.source *.build *.dsc *.buildinfo *.changes *.upload *.new"
    print(archivecmd)
    process = subprocess.Popen(archivecmd, shell=True)
    process.wait()
    archivecmdreturncode = process.returncode
    if archivecmdreturncode != 0:
        print("delete error \n")



def clean_all():
    delete_build()
    for i in ukui_list:
        if i == 'debian-packages':
            continue
        print("删除旧的debian目录\n")
        deletefile('./' + i)





def recover_debian(namedir):
    name = namedir.split("/")[-1]
    print(name + " 开始拷贝debian目录")
    archivecmd = "cp -r " + namedir + "/../debian-packages/" + name + "/debian" + " " + namedir
    print(archivecmd)
    process = subprocess.Popen(archivecmd, shell=True)
    process.wait()
    archivecmdreturncode = process.returncode
    if archivecmdreturncode != 0:
        if(checkout(name) != 0):
            print("找不到debian目录")



def listcurrentdir(path, list_name):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            list_name.append(file_path)


def replace_line(file, old_str, new_str):
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        line = lines[0]

    with open(file, "w+", encoding="utf-8") as f_w:
        for line in lines:
            if old_str in line:
                line = line.replace(old_str, new_str)
                break
        f_w.write(line)

        for i in range(1, len(lines)):
            f_w.write(lines[i])



def update_changelog(file):
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    text = lines[0]
    old_str = text.split("(")[1].split(")")[0]
    if '-' in old_str:
        new_str = old_str.split("-")[0] + ".1~" + datetime.datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
        text = text.replace(old_str, new_str)
    else:
        text = text.replace(")", ".1~" + datetime.datetime.now().strftime('%Y.%m.%d.%H.%M.%S') + ")")

    if 'cosmic'in text:
        text = text.replace('cosmic', 'disco')

    if 'bionic' in text:
        text = text.replace('bionic', 'disco')

    text = text + '\n  * Some changes.\n\n -- readlnh <readlnh@163.com>  Thu, 06 Dec 2018 15:48:18 +0800\n\n'

    with open(file, "w+", encoding="utf-8") as f_w:
        f_w.write(text)
        f_w.writelines(lines)

def dput(ppa,name):
    archivecmd = "dput " + ppa +  " " + name + "*.changes"
    print(archivecmd)
    process = subprocess.Popen(archivecmd, shell=True)
    process.wait()
    archivecmdreturncode = process.returncode
    if archivecmdreturncode != 0:
        print("dput error\n")


def dput_all():
    for i in ukui_list:
        dput(ppa, i)

def build_all():
    for i in ukui_list:
        if i == 'debian-packages':
            continue
        print("拷贝debian目录\n")
        recover_debian('./' + i)
        print("修改changelog\n")
        update_changelog('./' + i + "/debian/changelog")
        print("修改quilt至native")
        replace_line('./' + i + "/debian/source/format", "(quilt)", "(native)")
        print("开始安装依赖\n")
        mkbuilddeps(i)
        print("开始debuild\n")
        debuild(i)




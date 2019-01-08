import subprocess
import os
import datetime

ukui_list = [
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
             "debian-packages",
             "ukui-menus",
             "ukui-power-manager",
             "ubuntukylin-theme",
             "indicator-china-weather",
             "youker-assistant",
             "biometric-authentication",
             "kylin-burner ",
             "peony-extensions",
             "ukui-session-manager",
             "kylin-display-switch",
             "ukui-desktop-environment",
             "ukui-window-switch",
             "ukui-screensaver-qt",
             "ukui-themes",
             "ukui-media",
             "ukui-settings-daemon",
             "Genisys",
             "kylin-burner-new",
             "ukui-desktop",
             "ukui-screensaver-redesign",
             "ukui-backgrounds",
             "caja"
             ]

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
    #archivecmd = "git --git-dir=" + dir + "/.git pull"
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
    if archivecmdreturncode != 0:
        print(name + " checkout error")
    print("\n")
    os.chdir('../')


def debuild(name):
    os.chdir('./' + name)
    archivecmd = "yes | debuild -S -sa"
    process = subprocess.Popen(archivecmd, shell=True)
    process.wait()
    archivecmdreturncode = process.returncode
    if archivecmdreturncode != 0:
        print("debuild error\n")
    os.chdir('../')


def clone_all():
    for i in ukui_list:
        clone(i)

def pull_all():
    for i in ukui_list:
        pull(i)

def debuild_all():
    for i in ukui_list:
        debuild(i)

def checkout_all():
    for i in ukui_list:
        checkout(i)

def mkbuilddeps(name):
    archivecmd = 'yes | echo "zxasqw12345" | sudo -S mk-build-deps -i ' + './' + name + "/debian/control"
    print(archivecmd)
    process = subprocess.Popen(archivecmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    process.wait()
    archivecmdreturncode = process.returncode
    if archivecmdreturncode != 0:
        print("安装依赖失败 error\n")


def cp(namedir):
    name = namedir.split("/")[-1]
    print(name + " 开始拷贝debian目录")
    archivecmd = "cp -r " + namedir + "/../debian-packages/" + name + "/debian" + " " + namedir
    print(archivecmd)
    process = subprocess.Popen(archivecmd, shell=True)
    process.wait()
    archivecmdreturncode = process.returncode
    if archivecmdreturncode != 0:
        print("cp error \n")




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

def dput(ppa):
    archivecmd = "dput " + ppa +  " *.changes"
    print(archivecmd)
    process = subprocess.Popen(archivecmd, shell=True)
    process.wait()
    archivecmdreturncode = process.returncode
    if archivecmdreturncode != 0:
        print("dput error\n")

def build_all():
    for i in ukui_list:
        #os.chdir('./' + i)
        cp('./' + i)
        print("开始修改changelog")
        replace_line('./' + i + "/debian/changelog", ")", "-" + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ")")
        print("修改quilt至native")
        replace_line('./' + i + "/debian/source/format", "(quilt)", "(native)")
        print("开始安装依赖\n")
        mkbuilddeps(i)
        print("开始debuild")
        debuild(i)





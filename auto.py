import subprocess
import os
import datetime

ukui_list = ["debian-packages",
             "ukui-indicators",
             "ukui-menu",
             "ukui-menus"]

def pull(dir):
    archivecmd = "git --git-dir=" + dir + "/.git pull"
    process = subprocess.Popen(archivecmd, shell=True)
    process.wait()
    archivecmdreturncode = process.returncode
    if archivecmdreturncode != 0:
        print("pull error \n")


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

def dbuild():
    archivecmd = "yes | debuild -S -sa"
    process = subprocess.Popen(archivecmd, shell=True)
    process.wait()
    archivecmdreturncode = process.returncode
    if archivecmdreturncode != 0:
        print("debuild error\n")


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

def mkbuilddeps(namedir):
    archivecmd = 'yes | echo "zxasqw12345" | sudo -S mk-build-deps -i ' + namedir + "/debian/control"
    print(archivecmd)
    process = subprocess.Popen(archivecmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    process.wait()
    archivecmdreturncode = process.returncode
    if archivecmdreturncode != 0:
        print("安装依赖失败 error\n")

def clone(name):
    archivecmd = "git clone https://github.com/ukui/" + name + ".git"
    print(archivecmd)
    process = subprocess.Popen(archivecmd, shell=True)
    process.wait()
    archivecmdreturncode = process.returncode
    if archivecmdreturncode != 0:
        print(name + " clone error")
    print("\n")

def clone_all(dir):
    os.chdir(dir)
    for i in ukui_list:
        clone(i)

def dput(ppa):
    archivecmd = "dput " + ppa +  " *.changes"
    print(archivecmd)
    process = subprocess.Popen(archivecmd, shell=True)
    process.wait()
    archivecmdreturncode = process.returncode
    if archivecmdreturncode != 0:
        print("dput error\n")





def main():
    a = [];
    listcurrentdir("/home/readlnh/workspace/ukui-auto-test", a);
    for i in a:
        #os.chdir(i)
        print("开始pull " + i.split("/")[-1])
        pull(i)

        #os.chdir("../")


    print("\n")

    for i in a:
        if(i.split("/")[-1] != "debian-packages"):
            print("开始构建" + i.split("/")[-1])
            os.chdir(i)
            cp(i)
            print("开始修改changelog")
            replace_line(i + "/debian/changelog", ")", "-" + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ")")
            print("修改quilt至native")
            replace_line(i + "/debian/source/format", "(quilt)", "(native)")
            print("开始安装依赖\n")
            mkbuilddeps(i)
            print("开始debuild")
            dbuild()
            print("\n\n")
            os.chdir("../")



main()
#os.chdir("/home/readlnh/workspace/ukui-auto-test")
#clone_all("/home/readlnh/workspace/ukui-auto-test")
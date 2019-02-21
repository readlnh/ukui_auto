import  datetime

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

def change_version(file):
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    line = lines[0]
    old_str = line.split("(")[1].split(")")[0]
    if '-' in old_str:
        new_str = old_str.split("-")[0] + "~" + datetime.datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
    else:
        new_str = old_str.split("~")[0] + "~" + datetime.datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
    lines[0] = lines[0].replace(old_str, new_str)

    with open(file, "w+", encoding="utf-8") as f_w:
        f_w.writelines(lines)




def replace_key(file):
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    with open(file, "w+", encoding="utf-8") as f_w:
        for line in lines:
            if "--" in line:
                line = " -- readlnh <readlnh@163.com>  Thu, 06 Dec 2018 15:48:18 +0800\n"
            f_w.write(line)


def update_changelog(file):
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    text = lines[0]
    old_str = text.split("(")[1].split(")")[0]
    if '-' in old_str:
        new_str = old_str.split("-")[0] + ".1~" + datetime.datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
    text = text.replace(old_str, new_str)

    if 'cosmic'in text:
        text = text.replace('cosmic', 'disco')

    if 'bionic' in text:
        text = text.replace('bionic', 'disco')

    text = text + '\n  * Some changes.\n\n -- readlnh <readlnh@163.com>  Thu, 06 Dec 2018 15:48:18 +0800\n\n'

    with open(file, "w+", encoding="utf-8") as f_w:
        f_w.write(text)
        f_w.writelines(lines)


#replace_line("./111.txt", "(format)", "(native)")
#replace_line("./111.txt", ")", "" + datetime.datetime.now().strftime('%Y-%m-%d') + ")")
#replace_line("./111.txt", "")
#replace_key("./111.txt")
#change_version("./111.txt")
update_changelog("./111.txt")
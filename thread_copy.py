# 遍历目标目录　查找指定文件
# 计算资源数量　分配线程任务
# 每一个文件创建一个进程　执行任务
#  下载文件进行拼接　
from threading import Thread, Lock
import os
waefwafawefawefawe
lock = Lock()
usl = ["/home/tarena/桌面/",
       "/home/tarena/公共的/",
       "/home/tarena/模板/",
       "/home/tarena/示例/",
       "/home/tarena/文档/",
       "/home/tarena/试下载/",
       "/home/tarena/视频/",
       ]

new_list = []
filename = input("请输入文件名称")
for i in usl:
    if os.path.exists(i + filename):
        new_list.append(i + filename)
number = len(new_list)
if number == 0:
    print("没有资源")
    os._exit(0)
size = os.path.getsize("/home/tarena/公共的/%s"%filename)
one_size = size // number + 1
print(size,one_size)
fw = open("/home/tarena/%s" % filename, "wb+")


def copy(path, n):
    f = open(path, "rb")
    print(path)
    f.seek(n * one_size)
    data = f.read(one_size)
    with lock:
        fw.seek(n * one_size)
        fw.write(data)
    f.close()


jobs = []
n = 0
for path in new_list:
    t = Thread(target=copy, args=(path, n))
    jobs.append(t)
    t.start()
    n += 1
[i.join() for i in jobs]
fw.close()

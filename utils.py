# encoding:utf-8

# @Author: Rilzob
# @Time: 2018/11/17 上午8:57
import codecs


def load_file(path):  # 读入源代码并对其进行处理
    sourcecode = []
    file = codecs.open(path, 'r', 'utf-8')
    old_sourcecode = file.readlines()
    for code in old_sourcecode:
        code = code.strip()  # 清除code两端的空格
        code = code.strip('\n')  # 清除code两端的'\n'
        sourcecode.append(code)
    return sourcecode

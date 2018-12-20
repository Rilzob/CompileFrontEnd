# encoding:utf-8

# @Author: Rilzob
# @Time: 2018/12/20 上午9:18


def dagoptimize(QT):
    block = []
    start = 0
    for index, item in enumerate(QT):
        if item.startswith('(if') or item.startswith('(el') or item.startswith('(ie')\
                or item.startswith('(wh') or item.startswith('(do'):
            string = str(start) + '~' + str(index - 1)
            block.append(string)
            start = index
    string = str(start) + '~' + str(len(QT) - 1)
    block.append(string)
    print(block)
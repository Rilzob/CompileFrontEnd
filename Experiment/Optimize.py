# encoding:utf-8

# @Author: Rilzob
# @Time: 2018/12/20 上午9:18


def basicblock(QT):
    block = []
    start = 0
    for index, item in enumerate(QT):
        # if item.startswith('(if') or item.startswith('(el') or item.startswith('(ie')\
        #         or item.startswith('(wh') or item.startswith('(do'):
        if item[0] in ['if', 'el', 'ie', 'wh', 'do']:
            string = str(start) + '~' + str(index - 1)
            block.append(string)
            start = index
    string = str(start) + '~' + str(len(QT) - 1)
    block.append(string)
    print('基本块划分:', block)
    return block


def dagoptimize(QT, block):
    dag = {}
    i = 0
    # createVar = locals()
    for item in QT:
        if item.startswith('(='):
            exec('n{} = {}'.format(i, Node()))
            exec('n{}.operator = "="'.format(i))
            exec('')
    pass


class Node(object):
    def __init__(self):
        self.name = ''
        self.operator = ''
        self.mainsym = ''
        self.extrasym = []

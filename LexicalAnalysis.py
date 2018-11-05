# encoding:utf-8

# @Author: Rilzob
# @Time: 2018/10/31 上午9:24
import codecs

KEYWORD_LIST = ['int', 'float', 'double', 'char', 'main', 'if', 'else', 'continue', 'void', 'while', 'for',
                'switch', 'case']
SEPARATOR_LIST = ['{', '}', '(', ')', '[', ']', ';', ':', '.', ',', '?']
OPERATOR_LIST = ['+', '-', '*', '%', '/', '|', '&', '<', '>', '=', '!']


class Lexer(object):
    def __init__(self):
        self.sourcecode = []  # 源代码
        self.iT = set()   # 标识符
        self.CT = set()   # 常数
        self.sT = set()   # 字符串
        self.KT = set()   # 关键字
        self.PT = set()   # 界符
        self.ST = set()   # 操作符

    def load_file(self, path):  # 读入源代码并对其进行处理
        file = codecs.open(path, 'r', 'utf-8')
        old_sourcecode = file.readlines()
        for code in old_sourcecode:
            code = code.strip()  # 清除code两端的空格
            code = code.strip('\n')  # 清除code两端的'\n'
            self.sourcecode.append(code)
        return self.sourcecode

    @staticmethod
    def is_keyword(s):
        return s in KEYWORD_LIST

    @staticmethod
    def is_separator(s):
        return s in SEPARATOR_LIST

    @staticmethod
    def is_operator(s):
        return s in OPERATOR_LIST

    @staticmethod
    def lexical_error(msg):
        print('Lexical error:' + msg)

    @staticmethod
    def state_change(state_before, current_char):
        global state_now
        if state_before == 0:
            if current_char.isalpha():  # 检查当前字符是否是字母
                state_now = 1
            elif current_char.isdigit():  # 检查当前字符是否是数字
                state_now = 2
            elif current_char == ('\'' or '\"'):
                state_now = 3
            elif Lexer.is_separator(current_char):
                state_now = 4
            elif Lexer.is_operator(current_char):
                state_now = 11
            elif current_char == ' ':
                state_now = 0
            else:
                Lexer.lexical_error(current_char)
                return
        elif state_before == 1:
            if current_char.isalpha() or current_char.isdigit():
                state_now = state_before
            else:
                state_now = 5
        elif state_before == 2:
            if current_char.isdigit():
                state_now = state_before
            elif (not Lexer.is_separator(current_char)) or current_char == ' ':
                Lexer.lexical_error(current_char)
                print("缺少界符")
                return -1
            elif current_char.isalpha():
                Lexer.lexical_error(current_char)  # 数字后面紧跟字母报错
                print("标识符不能以数字开头")
                return -1
            else:
                state_now = 6
        elif state_before == 3:
            if current_char is not ('\'' or '\"'):  # 判断字符串是否到达结尾
                state_now = state_before
            else:
                state_now = 7
        elif state_before == 4:
            state_now = 0
        elif state_before == 11:
            if Lexer.is_operator(current_char):
                state_now = state_before
            else:
                state_now = 9
        return state_now

    def lexer_scanner(self):
        if self.sourcecode is None:
            return
        char_list = []
        state_now = 0
        value = 0
        word = string = op = ''

        def solve_state4():
            nonlocal op, state_now
            if state_now == (4 or 11):
                if Lexer.is_separator(current_char):
                    self.PT.add(current_char)
                    state_now = 0
                elif Lexer.is_operator(current_char):
                    op += current_char
                    state_now = 11
            else:
                state_now = 0

        for line in self.sourcecode:
            for char in line:
                char_list.append(char)
        for current_char in char_list:
            state_before = state_now
            state_now = self.state_change(state_before, current_char)
            if state_now == -1:  # 如果state_change函数返回为False则结束程序
                return
            elif state_now == 1:
                word += current_char
            elif state_now == 2:
                value = value * 10 + int(current_char)
            elif state_now == 3:
                string += current_char
            else:
                if state_now == 11:
                    op += current_char
                elif state_now == 4:
                    self.PT.add(current_char)
                    state_now = 0
                elif state_now == 5:
                    if self.is_keyword(word):
                        self.KT.add(word)
                    else:
                        self.iT.add(word)
                    state_now = self.state_change(0, current_char)
                    word = ''
                    solve_state4()
                elif state_now == 6:
                    self.CT.add(value)
                    state_now = self.state_change(0, current_char)
                    value = 0
                    solve_state4()
                elif state_now == 7:
                    string += current_char
                    self.sT.add(string)
                    string = ''
                    state_now = 0
                elif state_now == 9:
                    self.ST.add(op)
                    op = ''
                    state_now = self.state_change(0, current_char)
                    if state_now == 3:
                        string += '\''
            continue
        if not Lexer.is_separator(char_list[len(char_list) - 1]):
            print('程序末尾缺少界符')
        print('扫描完成')


if __name__ == '__main__':
    Lexer = Lexer()
    Lexer.load_file('/Users/rilzob/PycharmProjects/CompileFrontEnd/SourceCode.txt')
    Lexer.lexer_scanner()
    print("iT:")
    for iT in Lexer.iT:
        print(iT)
    print("CT:")
    for CT in Lexer.CT:
        print(CT)
    print("sT:")
    for sT in Lexer.sT:
        print(sT)
    print("KT:")
    for KT in Lexer.KT:
        print(KT)
    print("PT:")
    for PT in Lexer.PT:
        print(PT)
    print("ST:")
    for ST in Lexer.ST:
        print(ST)

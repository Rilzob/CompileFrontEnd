# encoding:utf-8

# @Author: Rilzob
# @Time: 2018/12/9 上午9:45

KEYWORD_LIST = ['int', 'float', 'double', 'char', 'main', 'if', 'else', 'continue', 'void', 'while', 'for',
                'switch', 'case']
SEPARATOR_LIST = ['{', '}', '(', ')', '[', ']', ';', ':', '.', ',', '?']
OPERATOR_LIST = ['+', '-', '*', '%', '/', '|', '&', '<', '>', '=', '!']


class Lexer(object):
    def __init__(self):
        self.iT = set()  # 标识符
        self.CT = set()  # 常数
        self.sT = set()  # 字符串
        self.cT = set()  # 字符
        self.KT = set()  # 关键字
        self.PT = set()  # 界符
        self.ST = set()  # 操作符
        self.wordlist = []

    @staticmethod
    def is_keyword(s):
        if s in KEYWORD_LIST:
            return True
        else:
            return False

    @staticmethod
    def is_separator(s):
        if s in SEPARATOR_LIST:
            return True
        else:
            return False

    @staticmethod
    def is_operator(s):
        if s in OPERATOR_LIST:
            return True
        else:
            return False

    @staticmethod
    def lexical_error(msg):
        print('Lexical error:' + msg)

    @staticmethod
    def state_change(state_before, current_char):
        global state_now
        if current_char == '\n':
            state_now = 0
        elif state_before == 0:
            if current_char.isalpha():  # 检查当前字符是否是字母
                state_now = 1
            elif current_char.isdigit():  # 检查当前字符是否是数字
                state_now = 2
            elif current_char == '\"':
                state_now = 3
            elif current_char == '\'':
                state_now = 8
            elif Lexer.is_separator(current_char):
                state_now = 4
            elif Lexer.is_operator(current_char):
                state_now = 11
            elif current_char == ' ':
                state_now = 0
            else:
                return
        elif state_before == 1:
            if current_char.isalpha() or current_char.isdigit():
                state_now = state_before
            else:
                state_now = 5
        elif state_before == 2:
            if current_char.isdigit():
                state_now = state_before
            elif current_char == '.':
                state_now = 13
            else:
                state_now = 6
        elif state_before == 13:
            if current_char.isdigit():
                state_now = state_before
            else:
                state_now = 6
        elif state_before == 3:
            if current_char is '\"':  # 判断字符串是否到达结尾
                state_now = 7
            else:
                state_now = state_before
        elif state_before == 8:
            if current_char is '\'':
                state_now = 12
            else:
                state_now = state_before
        elif state_before == 4:
            state_now = 0
        elif state_before == 11:
            if Lexer.is_operator(current_char):
                state_now = state_before
            else:
                state_now = 9
        return state_now

    def lexer_scanner(self, sourcecode):
        if sourcecode is None:
            return
        char_list = []
        state_now = 0
        value = 0
        word = string = op = ''
        n = 0.1

        def solve_state4():
            nonlocal op, state_now
            if state_now == 4 or state_now == 11:
                if Lexer.is_separator(current_char):
                    self.PT.add(current_char)
                    self.wordlist.append(current_char)
                    state_now = 0
                elif Lexer.is_operator(current_char):
                    op += current_char
            else:
                state_now = 0

        for line in sourcecode:
            for char in line:
                char_list.append(char)
            char_list.append('\n')

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
            elif state_now == 8:
                string += current_char
            elif state_now == 13:
                if current_char == '.':
                    continue
                else:
                    value = n * int(current_char) + value
                    n *= 0.1
            else:
                if state_now == 11:
                    op += current_char
                elif state_now == 4:
                    self.PT.add(current_char)
                    self.wordlist.append(current_char)
                    state_now = 0
                elif state_now == 5:
                    if self.is_keyword(word):
                        self.KT.add(word)
                        self.wordlist.append(word)
                    else:
                        self.iT.add(word)
                        self.wordlist.append(word)
                    state_now = self.state_change(0, current_char)
                    word = ''
                    solve_state4()
                elif state_now == 6:
                    self.CT.add(value)
                    self.wordlist.append(value)
                    state_now = self.state_change(0, current_char)
                    value = 0
                    n = 0.1
                    solve_state4()
                elif state_now == 7:
                    string += current_char
                    self.sT.add(string)
                    self.wordlist.append(string)
                    string = ''
                    state_now = 0
                elif state_now == 9:
                    self.ST.add(op)
                    self.wordlist.append(op)
                    op = ''
                    state_now = self.state_change(0, current_char)
                    if state_now == 4 or state_now == 11:
                        if Lexer.is_separator(current_char):
                            self.PT.add(current_char)
                            self.wordlist.append(current_char)
                            state_now = 0
                        elif Lexer.is_operator(current_char):
                            op += current_char
                    elif state_now == 3:
                        string += '\''
                    elif state_now == 2:
                        value = value * 10 + int(current_char)
                        # solve_state4()
                    elif state_now == 1:
                        word += current_char
                elif state_now == 12:
                    string += current_char
                    self.cT.add(string)
                    self.wordlist.append(string)
                    string = ''
                    state_now = 0
            continue
        print('扫描完成')

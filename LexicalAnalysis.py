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
        self.iT = []   # 标识符
        self.CT = []   # 常数
        self.sT = []   # 字符串
        self.KT = []   # 关键字
        self.PT = []   # 界符
        self.ST = []   # 操作符

    def load_file(self, path):  # 读入源代码并对其进行处理
        file = codecs.open(path, 'r', 'utf-8')
        old_sourcecode = file.readlines()
        for code in old_sourcecode:
            code = code.strip()  # 清除code两端的空格
            code = code.strip('\n')  # 清除code两端的'\n'
            self.sourcecode.append(code)
        return self.sourcecode

    @staticmethod
    def state_change(state_before, current_char):
        if state_before == 0:
            if current_char == ' ':
                state_now = 0
            elif current_char.isalpha():
                state_now = 1
            elif current_char.isdigit():
                state_now = 2
            elif current_char == ('\'' or '\"'):
                state_now = 3
            else:
                state_now = 4
        elif state_before == 1:
            if current_char.isalpha() or current_char.isdigit():
                state_now = state_before
            else:
                state_now = 5
        elif state_before == 2:
            if current_char.isdigit():
                state_now = state_before
            else:
                state_now = 6
        elif state_before == 3:
            if current_char is not '\'' or '\"':
                state_now = state_before
            else:
                state_now = 7
        else:
            state_now = 4
        return state_now

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

    def lexer_scanner(self):
        if self.sourcecode is None:
            return
        char_list = []
        state_now = 0
        value = 0
        word = ''
        string = ''
        op = ''
        ST_len = 0
        KT_len = 0
        sT_len = 0
        CT_len = 0
        PT_len = 0
        iT_len = 0

        for line in self.sourcecode:
            for char in line:
                char_list.append(char)
        for current_char in char_list:
            if current_char == ' ':
                if state_now == 1:
                    state_now = 5
                elif state_now == 2:
                    state_now = 6
                elif state_now == 3:
                    state_now = 7
            else:
                state_before = state_now
                state_now = self.state_change(state_before, current_char)
            # if state_now == 10:
            #     if state_before == 1:
            #         state_now = 5
            #     elif state_before == 2:
            #         state_now = 6
            #     elif state_before == 3:
            #         state_now = 7
            #     else:
            #         state_now = 4
            if state_now == 1:
                word += current_char
                continue
            if state_now == 2:
                value = value * 10 + int(current_char)
                continue
            if state_now == 3:
                string += current_char
                continue
            if state_now == 4:
                if self.is_separator(current_char):
                    self.ST.append((current_char, 'ST', ST_len))
                    ST_len += 1
                    state_now = 0
                    continue
                if self.is_operator(current_char):
                    op += current_char
                    continue
                else:
                    self.PT.append((op, 'PT', PT_len))
                    PT_len += 1
                    op = ''
                    state_now = 0
                    continue
            if state_now == 5:
                if self.is_keyword(word):
                    self.KT.append((word, 'KT', KT_len))
                    KT_len += 1
                else:
                    self.iT.append((word, 'iT', iT_len))
                    iT_len += 1
                state_now = self.state_change(0, current_char)
                word = ''
                if state_now == 4:
                    if self.is_separator(current_char):
                        self.ST.append((current_char, 'ST', ST_len))
                        ST_len += 1
                        state_now = 0
                        continue
                    if self.is_operator(current_char):
                        op += current_char
                        state_now = 4
                        continue
                    else:
                        self.PT.append((op, 'PT', PT_len))
                        PT_len += 1
                        op = ''
                        state_now = 0
                        continue
                continue
            if state_now == 6:
                self.CT.append((value, 'CT', CT_len))
                CT_len += 1
                state_now = self.state_change(0, current_char)
                value = 0
                if state_now == 4:
                    if self.is_separator(current_char):
                        self.ST.append((current_char, 'ST', ST_len))
                        ST_len += 1
                        state_now = 0
                        continue
                    if self.is_operator(current_char):
                        op += current_char
                        state_now = 4
                        continue
                    else:
                        self.PT.append((op, 'PT', PT_len))
                        PT_len += 1
                        op = ''
                        state_now = 0
                        continue
                continue
            if state_now == 7:
                string += current_char
                self.sT.append((string, 'sT', sT_len))
                sT_len += 1
                state_now = 0
                continue
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
    for KT in Lexer.KT:
        print(KT)
    print("ST:")
    for ST in Lexer.ST:
        print(ST)
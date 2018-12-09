# encoding:utf-8

# @Author: Rilzob
# @Time: 2018/11/18 下午5:18

# LL(1)分析法
from Exercise.LexicalAnalysis2 import Lexer


class LLAnalysis(Lexer):
    def __init__(self):
        super().__init__()
        self.stack = [';', 'E']
        self.worditer = iter(self.wordlist)
        self.word = ''

    def is_i(self, word):  # 标识符
        if (word in self.iT) or (word in self.CT):
            return True
        else:
            return False

    def Analyzer(self):
        self.word = next(self.worditer)
        while self.stack[-1] != ';' or self.word != ';':
            try:
                currentstr = self.stack.pop()
                if currentstr == 'E':
                    if self.is_i(self.word) or self.word == '(':
                        # 产生式1
                        self.stack.append('E_')
                        self.stack.append('T')
                    else:
                        return False
                elif currentstr == 'E_':
                    if self.word == '+' or self.word == '-':
                        # 产生式2
                        self.stack.append('E_')
                        self.stack.append('T')
                        self.stack.append('w1')
                    elif self.word == ')' or self.word == ';':
                        # 这里不知道为什么不可以用self.word == (')' or ';')，如果self.word为';'，但返回值为False
                        # 产生式3
                        continue
                    else:
                        return False
                elif currentstr == 'T':
                    if self.is_i(self.word) or self.word == '(':
                        # 产生式4
                        self.stack.append('T_')
                        self.stack.append('F')
                    else:
                        return False
                elif currentstr == 'T_':
                    if self.word in ['+', '-', ')', ';']:
                        # 产生式6
                        continue
                    elif self.word == '*' or self.word == '/':
                        # 产生式5
                        self.stack.append('T_')
                        self.stack.append('F')
                        self.stack.append('w2')
                    else:
                        return False
                elif currentstr == 'F':
                    if self.is_i(self.word):
                        # 产生式7
                        self.stack.append('i')
                    elif self.word == '(':
                        # 产生式8
                        self.stack.append(')')
                        self.stack.append('E')
                        self.stack.append('(')
                    else:
                        return False
                elif currentstr == 'i':
                    if self.is_i(self.word):
                        self.word = next(self.worditer)
                    else:
                        return False
                elif currentstr == '(':
                    if self.word == '(':
                        self.word = next(self.worditer)
                    else:
                        return False
                elif currentstr == ')':
                    if self.word == ')':
                        self.word = next(self.worditer)
                    else:
                        return False
                elif currentstr == 'w1':
                    if self.word == '+' or self.word == '-':
                        self.word = next(self.worditer)
                    else:
                        return False
                elif currentstr == 'w2':
                    if self.word == '*' or self.word == '/':
                        self.word = next(self.worditer)
                    else:
                        return False
                else:
                    return False
            except StopIteration:
                return False
        return True

    def grammer_parse(self):
        result = self.Analyzer()
        if result:
            print("LL(1)分析法：该表达式符合算术表达式文法")
        else:
            print("LL(1)分析法：该表达式不符合算术表达式文法")

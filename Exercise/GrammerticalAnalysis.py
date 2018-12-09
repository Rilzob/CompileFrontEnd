# encoding:utf-8

# @Author: Rilzob
# @Time: 2018/11/17 上午8:58

# 递归子程序
from Exercise.LexicalAnalysis2 import Lexer
import sys


class Grammer(Lexer):
    def __init__(self):
        super().__init__()
        # self.stack = [';', 'E']
        self.worditer = iter(self.wordlist)

    def is_i(self, word):  # 标识符
        if (word in self.iT) or (word in self.CT):
            return True
        else:
            return False

    def judge_F(self):
        if self.is_i(self.word):
            self.word = next(self.worditer)
            return True
        elif self.word == '(':
            self.word = next(self.worditer)
            self.judge_E()
            if self.word == ')':
                self.word = next(self.worditer)
                return True
            else:
                print("Error2")
                return False
        else:
            print("Error1")
            return False

    def judge_T(self):
        if self.judge_F():
            while True:
                try:
                    if self.word in ['*', '/']:
                        self.word = next(self.worditer)
                        if self.judge_F():
                            continue
                        else:
                            return False
                    return True
                except StopIteration:
                    print("结束1")
                    sys.exit()
        else:
            return False

    def judge_E(self):
        if self.judge_T():
            while True:
                try:
                    if self.word in ['+', '-']:
                        self.word = next(self.worditer)
                        if self.judge_T():
                            continue
                        else:
                            return False
                    return True
                except StopIteration:
                    print("结束2")
                    sys.exit(0)
        else:
            return False

    def grammer_parse(self):
        self.word = next(self.worditer)
        self.judge_E()
        if self.word == ';':
            print("递归子程序法：该表达式符合算术表达式文法")
        else:
            print("递归子程序法：该表达式不符合算术表达式文法")
            return

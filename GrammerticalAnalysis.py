# encoding:utf-8

# @Author: Rilzob
# @Time: 2018/11/17 上午8:58

# 递归子程序
from LexicalAnalysis2 import iT, CT, wordlist
import sys

worditer = iter(wordlist)


class Grammer(object):
    def __init__(self):
        self.word = ""

    @staticmethod
    def is_CT(word):  # 常数
        return word in CT

    @staticmethod
    def is_iT(word):  # 标识符
        return word in iT

    def judge_F(self):
        if self.is_iT(self.word) or self.is_CT(self.word):
            self.word = next(worditer)
            return True
        elif self.word == '(':
            self.word = next(worditer)
            self.judge_E()
            if self.word == ')':
                self.word = next(worditer)
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
                    if self.word == '*' or self.word == '/':
                        self.word = next(worditer)
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
                    if self.word == '+' or self.word == '-':
                        self.word = next(worditer)
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
        self.word = next(worditer)
        self.judge_E()
        if self.word == ';':
            print("递归子程序法：该文法符合算术表达式文法")
        else:
            print("递归子程序法：该文法不符合算术表达式文法")
            return

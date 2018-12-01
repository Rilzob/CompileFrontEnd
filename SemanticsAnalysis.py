# encoding:utf-8

# @Author: Rilzob
# @Time: 2018/12/1 上午9:41

from GrammerticalAnalysis import Grammer
import sys


class SemanticAnalysis(Grammer):
    def __init__(self):
        super().__init__()
        self.worditer = iter(self.wordlist)
        self.stack = []
        self.SEM = []
        self.QT = []
        # self.currentword1 = ''  # 暂存符号
        # self.currentword2 = ''
        self.currentwordlist = []
        self.currenword = ''

    def is_i(self, word):  # 标识符
        if (word in self.iT) or (word in self.CT):
            return True
        else:
            return False

    def judge_F(self):
        if self.is_i(self.word):
            self.stack.append('PUSH(' + str(self.word) + ')')
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
                        self.currentwordlist.append(self.word)
                        self.word = next(self.worditer)
                        if self.judge_F():
                            self.currentword = self.currentwordlist.pop()
                            if self.currentword == '*':
                                self.stack.append('GEQ(*)')
                            else:
                                self.stack.append('GEQ(/)')
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
                        self.currentwordlist.append(self.word)
                        self.word = next(self.worditer)
                        if self.judge_T():
                            self.currentword = self.currentwordlist.pop()
                            if self.currentword == '+':
                                self.stack.append('GEQ(+)')
                            else:
                                self.stack.append('GEQ(-)')
                            continue
                        else:
                            return False
                    return True
                except StopIteration:
                    print("结束2")
                    sys.exit(0)
        else:
            return False

    def semantic_parse(self):
        i = 1
        self.word = next(self.worditer)
        self.judge_E()
        if self.word == ';':
            for currentstr in self.stack:
                if currentstr.startswith('PUSH'):
                    self.SEM.append(currentstr.lstrip('PUSH(').rstrip(')'))
            for currentstr in self.stack:
                if currentstr.startswith('GEQ'):
                    char1 = self.SEM.pop()
                    char2 = self.SEM.pop()
                    self.SEM.append('t' + str(i))
                    self.QT.append('(' + currentstr.lstrip('GEQ(').rstrip(')') + ',' + char2 + ','
                                   + char1 + ',' + 't' + str(i) + ')')
                    i += 1
            for QT in self.QT:
                print(QT)
            # print("递归子程序法：该表达式符合算术表达式文法")
        else:
            print("递归子程序法：该表达式不符合算术表达式文法")
            return
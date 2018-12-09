# encoding:utf-8

# @Author: Rilzob
# @Time: 2018/12/9 上午9:46

from Experiment.Lexer import Lexer
from utils import load_file

import sys


class Parser(Lexer):  # 递归下降分析法
    def __init__(self):
        super().__init__()
        sourcecode = load_file('/Users/rilzob/PycharmProjects/CompileFrontEnd/Experiment/Test1.txt')
        # sourcecode = load_file('/Users/rilzob/PycharmProjects/CompileFrontEnd/Exercise/SourceCode.txt')
        self.lexer_scanner(sourcecode)
        self.worditer = iter(self.wordlist)
        self.word = next(self.worditer)

    def is_id(self):
        if self.word in self.KT or self.word in self.iT:
            return True
        else:
            return False

    def _statement(self):  # 声明语句
        if not self._type():
            return False
        if self.is_id():
            self.word = next(self.worditer)
            if self.word == '=':
                self.word = next(self.worditer)
                if not self._constant():
                    return False
                if self.word == ';':
                    self.word = next(self.worditer)
                    return True
                else:
                    print("Error3")
                    return False
            elif self.word == ';':
                self.word = next(self.worditer)
                return True
            else:
                print("Error2")
                return False
        else:
            print("Error1")
            return False

    def _constant(self):
        if self.word in self.CT:  # 判断是否是num
            self.word = next(self.worditer)
            return True
        elif self.word in self.cT or self.word in self.sT:  # 判断是否是string
            self.word = next(self.worditer)
            return True
        else:
            print("Error4")
            return False

    def _type(self):
        if self.word == 'int' or self.word == 'float' or self.word == 'char':
            self.word = next(self.worditer)
            return True
        else:
            print("Error5")
            return False

    def _assignment(self):  # 赋值语句
        if self.is_id():
            self.word = next(self.worditer)
            if self.word == '=':
                self.word = next(self.worditer)
                if not self._expression():
                    return False
                if self.word == ';':
                    self.word = next(self.worditer)
                    return True
                else:
                    print("Error8")
                    return False
            else:
                print("Error7")
                return False
        else:
            print("Error6")
            return False

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
                print("Error10")
                return False
        else:
            print("Error9")
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

    def _expression(self):
        if not self.judge_E():
            return False
        elif self.word == ';':
            print("符合算术表达式文法")
            self.word = next(self.worditer)
            return True
        else:
            return False

    def is_type(self):
        if self.word == 'int' or self.word == 'float' or self.word == 'char':
            return True
        else:
            return False

    def _main(self):
        while True:
            try:
                if self.is_type():
                    if not self._statement():
                        return False
                    else:
                        continue
                elif self.is_id():
                    if not self._assignment():
                        return False
                    else:
                        continue
                else:
                    print("Error11")
                    return False
            except StopIteration:
                print("符合语法")
                sys.exit(0)
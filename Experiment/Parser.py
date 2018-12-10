# encoding:utf-8

# @Author: Rilzob
# @Time: 2018/12/9 上午9:46

from Experiment.Lexer import Lexer
from utils import load_file

import sys


class Parser(Lexer):  # 递归下降分析法
    def __init__(self):
        super().__init__()
        sourcecode = load_file('/Users/rilzob/PycharmProjects/CompileFrontEnd/Experiment/Test2.txt')
        # sourcecode = load_file('/Users/rilzob/PycharmProjects/CompileFrontEnd/Exercise/SourceCode.txt')
        self.lexer_scanner(sourcecode)
        self.worditer = iter(self.wordlist)
        self.word = next(self.worditer)

    def is_id(self):
        if self.word in self.iT:
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
                # if self.word == ';':
                #     self.word = next(self.worditer)
                #     return True
                # else:
                #     print("Error3")
                #     return False
                return True
            # elif self.word == ';':
            #     self.word = next(self.worditer)
            #     return True
            # else:
            #     print("Error2")
            #     return False
            else:
                return True
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
                # if self.word == ';':
                #     self.word = next(self.worditer)
                #     return True
                # else:
                #     print("Error8")
                #     return False
                return True
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
        # elif self.word == ';':
        #     print("符合算术表达式文法")
        #     self.word = next(self.worditer)
        #     return True
        # else:
        #     return False
        # self.word = next(self.worditer)
        return True

    def is_type(self):
        if self.word == 'int' or self.word == 'float' or self.word == 'char':
            return True
        else:
            return False

    def _sentence(self):
        if self.is_type():
            if not self._statement():
                return False
            if self.word == ';':
                self.word = next(self.worditer)
                return True
            else:
                print("Error15")
                return False
        elif self.is_id():
            if not self._assignment():
                return False
            if self.word == ';':
                self.word = next(self.worditer)
                return True
            else:
                print("Error16")
                return False
        elif self._expression():
            if self.word == ';':
                self.word = next(self.worditer)
                return True
            else:
                print("Error17")
                return False
        else:
            print("Error11")
            return False

    def _ifelsecontrol(self):
        if self.word == 'if':
            self.word = next(self.worditer)
            if not self._expression():
                return False
            if self.word == '{':
                self.word = next(self.worditer)
                if not self._sentence():
                    return False
                if self.word == '}':
                    self.word = next(self.worditer)
                    if self.word == 'else':
                        self.word = next(self.worditer)
                        if self.word == '{':
                            self.word = next(self.worditer)
                            if not self._sentence():
                                return False
                            if self.word == '}':
                                self.word = next(self.worditer)
                                return True
                            else:
                                print("Error18")
                                return False
                        else:
                            print("Error19")
                            return False
                    else:
                        return True
                else:
                    print("Error12")
                    return False
            else:
                print("Error13")
                return False
        else:
            print("Error14")
            return False

    def _elsecontrol(self):
        if self.word == 'else':
            self.word = next(self.worditer)
            if self.word == '{':
                self.word = next(self.worditer)
                if not self._sentence():
                    return False
                if self.word == '}':
                    self.word = next(self.worditer)
                    return True
                else:
                    print("Error18")
                    return False
            else:
                print("Error19")
                return False
        else:
            self.word = next(self.worditer)
            return True

    def _whilecontrol(self):
        if self.word == 'while':
            self.word = next(self.worditer)
            if not self._expression():
                return False
            if self.word == '{':
                self.word = next(self.worditer)
                if not self._sentence():
                    return False
                if self.word == '}':
                    self.word = next(self.worditer)
                    return True
                else:
                    print("Error20")
                    return False
            else:
                print("Error21")
                return False
        else:
            print("Error22")
            return False

    def _forcontrol(self):
        if self.word == 'for':
            self.word = next(self.worditer)
            if self.word == '(':
                self.word = next(self.worditer)
                if not self._assignment():
                    return False
                if self.word == ';':
                    self.word = next(self.worditer)
                    if not self._expression():
                        return False
                    if self.word == ';':
                        self.word = next(self.worditer)
                        if not self._expression():
                            return False
                        if self.word == ')':
                            self.word = next(self.worditer)
                            if self.word == '{':
                                self.word = next(self.worditer)
                                if not self._sentence():
                                    return False
                                if self.word == '}':
                                    self.word = next(self.worditer)
                                    return True
                                else:
                                    print("Error23")
                                    return False
                            else:
                                print("Error24")
                                return False
                        else:
                            print("Error25")
                            return False
                    else:
                        print("Error26")
                        return False
                else:
                    print("Error27")
                    return False
            else:
                print("Error28")
                return False
        else:
            print("Error29")
            return False

    def _control(self):
        if self.word == 'if':
            if not self._ifelsecontrol():
                return False
            else:
                return True
        elif self.word == 'while':
            if not self._whilecontrol():
                return False
            else:
                return True
        elif self.word == 'for':
            if not self._forcontrol():
                return False
            else:
                return True
        else:
            print("Error30")
            return False

    def _main(self):
        while True:
            try:
                if self.is_id() or self.is_type():
                    if self._sentence():
                        continue
                    else:
                        return False
                elif self.word in ['if', 'while', 'for']:
                    if self._control():
                        continue
                    else:
                        return False
                else:
                    return False
            except StopIteration:
                print("符合语法")
                sys.exit(0)
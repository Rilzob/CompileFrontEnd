# encoding:utf-8

# @Author: Rilzob
# @Time: 2018/11/17 上午9:25
from LexicalAnalysis2 import Lexer
from LexicalAnalysis2 import wordlist
from GrammerticalAnalysis import Grammer
from utils import load_file

if __name__ == '__main__':
    Lexer = Lexer()
    Grammer1 = Grammer()
    sourcecode = load_file('/Users/rilzob/PycharmProjects/CompileFrontEnd/SourceCode1.txt')
    Lexer.lexer_scanner(sourcecode)
    print("wordlist:", str(wordlist))
    Grammer1.grammer_parse()
    # print("标识符：")
    # for i, iT in enumerate(iT):
    #     print("<" + str(i) + "," + str(iT) + ">")
    # print("常数：")
    # for i, CT in enumerate(CT):
    #     print("<" + str(i) + "," + str(CT) + ">")
    # print("字符串：")
    # for i, sT in enumerate(sT):
    #     print("<" + str(i) + "," + str(sT) + ">")
    # print("关键字：")
    # for i, KT in enumerate(KT):
    #     print("<" + str(i) + "," + str(KT) + ">")
    # print("界符：")
    # for i, PT in enumerate(PT):
    #     print("<" + str(i) + "," + str(PT) + ">")
    # print("操作符：")
    # for i, ST in enumerate(ST):
    #     print("<" + str(i) + "," + str(ST) + ">")
    # print("字符：")
    # for i, cT in enumerate(cT):
    #     print("<" + str(i) + "," + str(cT) + ">")
    # print("wordlist:" + str(wordlist))


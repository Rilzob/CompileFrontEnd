# encoding:utf-8

# @Author: Rilzob
# @Time: 2018/12/9 上午10:46

from Experiment.Parser import Parser
import getopt
import sys
from Experiment.Optimize import basicblock

if __name__ == '__main__':
    # try:
    #     opts, argvs = getopt.getopt(sys.argv[1:], 's:lpah', ['help'])
    # except:
    #     print(__doc__)
    #     exit()
    #
    # for opt, argv in opts:
    #     if opt == '-p':
    #         Parser = Parser()
    Parser = Parser()
    print(Parser.wordlist)
    Parser._main()
    print('四元式:', Parser.QT)
    print('符号表:', Parser.SYNBL)
    basicblock(Parser.QT)

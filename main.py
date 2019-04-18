#coding=utf-8


import sys
import clang.cindex

import file
import change
from myglobal import *


def addFuncitons(functionName):
    global functionList
    functionList.append(functionName)
    
def addVariables(variableName):
    global variableList 
    variableList.append(variableName)

def removeSame(mylist):
    mylist = sorted(set(mylist),key=mylist.index)
    return mylist

def getFuncsAndVars():
    #获得最后的函数和变量列表
    global functionList
    global variableList
    functionList = removeSame(functionList)
    variableList = removeSame(variableList)
    for each in whiteFunction:
        if each in functionList:
            functionList.remove(each)

def getMiwenFuncsAndVars():
    #获得对应密文 生成字典
    global functionList
    global variableList
    global functionDict
    global variableDict
    for each in functionList:
        functionDict[each] = change.getMiwen(each)
    for each in variableList:
        variableDict[each] = change.getMiwen(each)

def showMiwenFuncsAndVars():
    #打印密文对应信息
    if debug:
        print len(functionDict),len(variableDict)
        for k,v in functionDict.items():
            print k,">>>>",v
        for k,v in variableDict.items():
            print k,">>>>",v
def showToken(node):
    # token test 分词
    ts = node.get_tokens()
    for t  in ts:
        print t.spelling


def parseNode(node,indent):
    #递归解析C++语法树,添加
    text = node.spelling or node.displayname
    kind  = str(node.kind)[str(node.kind).index('.')+1:]
    # if debug:
    #     print 'node.kind=',node.kind
    #     print ' ' * indent,"{} >>> {}".format(kind,text)
    if kind == "FUNCTION_DECL":
        addFuncitons(text)
    elif kind == "VAR_DECL" or kind == "PARM_DECL" or kind == "UNEXPOSED_EXPR":
        addVariables(text)
    else:
        # print 'unknown kind >>>>>>>>>>>>>>>>>>>>>>>>>',text
        pass
    for i in node.get_children():
        parseNode(i,indent + 2)

def printFuncAndVar():
    #打印函数和变量名
    if len(functionList) !=0:
        print u'共有函数 %d 个:' % len(functionList)        
    for each in functionList:
        print 'function >> ',each
    print '*' * 50
    if len(variableList) !=0:
        print u'共有变量 %d 个:' % len(variableList)
    for each in variableList:
        print  'variable >> ',each

def printFuncAndVarTest():
    # getFuncsAndVars()#获得最终的函数 和 变量列表 
    print 'final result :>>>'
    printFuncAndVar()

def replaceFunAndVarInAllFiles():
    for eachFile in allFiles:
        if debug:
            print eachFile,"being replaceing ............................................."
        file.replaceFunAndVarInFile(eachFile)

def main():
    #输入目录 获得所有要处理的文件列表
    file.findAllFiles(rootPath,allFiles)
    #处理单个文件 汇总获得所有函数名和变量名列表
    for eachFile in allFiles:
        if debug:
            print eachFile,' >>>  parsing .................................................'
        index = clang.cindex.Index.create()
        tu = index.parse(eachFile)
        parseNode(tu.cursor,0)
    #获得最终的函数 和 变量列表
    getFuncsAndVars()
    printFuncAndVarTest()
    #获得对应密文 生成字典
    getMiwenFuncsAndVars()
    # #打印转换列表
    showMiwenFuncsAndVars()
    # #处理单个文件 进行函数名和变量名替换
    replaceFunAndVarInAllFiles()
    print "Game over Enjoy~"

if __name__ == '__main__':
    main()



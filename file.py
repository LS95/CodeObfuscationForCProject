#coding=utf-8

import os
import re
from myglobal import *
import change
'''
目录文件处理 
'''
def isFileValid(fileName):
    #判断是非是需要处理的类型 .h .hpp .c .cc .cpp 返回True or False
    fileTypeList = [".h",".hpp",".c",".cc",".cpp"]
    for each in fileTypeList:
        if fileName.endswith(each):
            return True
    return False

def isHeaderLine(line):
    #判断是否是引入的头文件
    return True if re.match(re.compile('#\s*include'),line) else False

def findAllFiles(rootDir,allFile):
    #找到所有文件夹下的文件，返回allFile > list
    fileList  = os.listdir(rootDir)
    for fileName in fileList:
        filePath  = os.path.join("%s\%s" % (rootDir,fileName))
        if os.path.isdir(filePath):
            findAllFiles(filePath,allFile)
        else:
            if isFileValid(filePath):
                #处理有效文件类型
                allFile.append(filePath)
            else:
                pass
    return allFile


'''
读写文件
'''
def replaceFunAndVarInFile(fileName):
    #替换文件内容 
    global debug
    afterContents = []
    i = 1
    with open(fileName) as f:
        lines  =  f.readlines()
        for eachLine in lines:
            # print eachLine,">>>",i
            afterEachLine = eachLine
            if debug:
                print i,'>>>>>>>>>>>>>>>>>',eachLine.strip('\n') , str(isHeaderLine(eachLine))
            #保留头文件不做替换
            if isHeaderLine(eachLine):
                afterContents.append(afterEachLine)
            #替换函数和变量
            else:
                #替换函数
                eachLine = change.handleString(eachLine)
                for each in functionDict.keys():
                    if each in eachLine:
                        mode = r'\b%s\b' % (each)
                        # print mode
                        pa = re.compile(mode)
                        afterEachLine = re.sub(pa,functionDict[each],eachLine)
                        eachLine = afterEachLine
                 
                #替换变量
                for each in variableDict.keys():
                    if each in eachLine:
                        mode = r'\b(%s)\b' % (each)
                        # print mode
                        pa = re.compile(mode)
                        afterEachLine = re.sub(pa,variableDict[each],eachLine)
                        eachLine = afterEachLine
                print 'afterEachLine=',afterEachLine
                afterContents.append(afterEachLine)

                # afterContents.append(eachLine)
            i = i + 1
            

    # print "*" * 10,u'now content = '
    # for afterLine in afterContents:
    #     print afterLine
    #写入文件
    with open(fileName,"w") as f:
        f.write(''.join(afterContents))




# def replaceFunAndVarInFile(fileName):
#     #替换文件内容 
#     afterContents = ''
#     with open(fileName,"r") as f:
#         beforeContents = f.read()
#     if debug:
#         print beforeContents

#     for each in functionDict.keys():
#         if each in beforeContents:
#             mode = r'\b%s\b' % (each)
#             print mode
#             pa = re.compile(mode)
#             afterContents = re.sub(pa,functionDict[each],beforeContents)
#             beforeContents = afterContents

#     for each in variableDict.keys():
#         if each in beforeContents:  #r'\b%s\b' % (each), " "+variableDict[each]+" ",
#             modesList = [r'\s%s' % (each),
#                          r'\s%s=' % (each),
#                          r'\(%s\b' % (each),
#                          r'\(%s,' % (each),
#                          r'\b%s\)' % (each),
#                          r'(,%s).*?' % (each),
#                          r'("%s).*?' % (each),
#                          #r'.*?(%s);' % (each),
#                          ]
#             resultList = [" "+variableDict[each]+" ",
#                           " "+variableDict[each]+"=",
#                           "("+variableDict[each]+" ",
#                           "("+variableDict[each]+",",
#                           " "+variableDict[each]+")",
#                           ","+variableDict[each]+"",
#                           "\""+variableDict[each]+"",
#                           #" "+variableDict[each]+";",
#                           ]
#             # print len(modesList),len(resultList)
#             for i in range(len(modesList)):
#                 pa = re.compile(modesList[i])
#                 if pa.search(beforeContents):
#                     print i,">>>",modesList[i],">>>>",resultList[i]
#                     afterContents = re.sub(pa,resultList[i],beforeContents)
#                     beforeContents = afterContents

#     with open(fileName,"w") as f:
#         f.write(beforeContents)

#     if debug:
#         print beforeContents
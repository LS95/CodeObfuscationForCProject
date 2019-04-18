#coding=utf-8
'''
输入mingwen
输出加密后的结果 getMiwen(mingwen)
主要有2种：
    1.随机数字+字母字符串 getRandomResult getRandomResult2
    2.md5处理后的相近字符串O0
'''
import hashlib,os,re
import random,string   #调用random、string模块
from myglobal import *


src_digits = string.digits              #string_数字
src_uppercase = string.ascii_uppercase  #string_大写字母
src_lowercase = string.ascii_lowercase  #string_小写字母

def getRandomResult():
    result =  list((''.join(map(lambda x:(hex(ord(x))[2:]), os.urandom(16))))[0:16])
    #保证变量函数不以数字开头
    if result[0].isdigit():
        result[0] = '_'
    new_password = ''.join(result)
    return new_password

def getMd5Result(mingwen):
    #获得md5结果
    obj = hashlib.md5()
    obj.update(mingwen)
    result = obj.hexdigest()[8:24]
    return result

def getRandomResult2():
    #随机生成数字、大写字母、小写字母的组成个数（可根据实际需要进行更改）
    digits_num = random.randint(1,6)
    uppercase_num = random.randint(1,16-digits_num-1)
    lowercase_num = 16 - (digits_num + uppercase_num)

    password = random.sample(src_digits,digits_num) + random.sample(src_uppercase,uppercase_num) + random.sample(src_lowercase,lowercase_num)

    #打乱字符串
    random.shuffle(password)
    if password[0].isdigit():
        password[0] = '_'
    #列表转字符串
    new_password = ''.join(password)

    #保证变量函数不以数字开头

    return new_password

def getSimilarResult(mingwen):
    words = ['O','0','l','1']
    miwen = getMd5Result(mingwen)[:-1]
    #保证变量函数不以数字开头
    result =  'O' if (ord(miwen[0]) % 2 == 0) else 'l'
    for each in miwen:
        result += words[ord(each) % 4]
    return result

def getMiwen(mingwen):
    chooseNum = random.randint(1,3)
    if chooseNum == 1:
        return getRandomResult()
    elif chooseNum ==2:
        return getRandomResult2()
    else:
        return getSimilarResult(mingwen)


def hexEncodeString(string):
    #返回字符串的16进制形式
    hexStr = string[1:-1].encode("hex")
    strList = re.findall(r'.{2}',hexStr)
    if strList:
        return '"\\x'+'\\x'.join(strList)+"\""

def  handleString(testString):
    #判断是否是string即双引号里面的内容 如 printf("%d %d\n",a,b),返回修改后的string
    pa =   re.compile(r'"[^"]*?"')
    originContents = re.findall(pa,testString)# return list 
    if len(originContents):
        for eachStr in originContents:
            afterString = hexEncodeString(eachStr)
            testString = testString.replace(eachStr,afterString)
    return testString

# for i in range(10):
#     miwen = getMiwen("admin%d" % i)
#     print len(miwen),miwen

# for i in range(10):
#     print getRandomResult(),"|",getRandomResult2(),"|",getSimilarResult("admin%d" % i)
# print generateMiwen("admin")
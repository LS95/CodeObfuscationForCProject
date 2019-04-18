#coding=utf-8

allFiles = []                                                        #目录文件列表
functionList  = []                                                   #函数列表
variableList  = []                                                   #变量列表
functionDict = {}                                                     #函数转换字典
variableDict = {}                                                     #变量转换字典

whiteFunction = ["main","printf","scanf","system","dllmain"]

debug = 1  #调试模式 1打印信息
#rootPath = "D:\\ProgramCodes\\WProtect\\src\\Libudis86"
#rootPath = "D:\\Programs\\codeObfuscatorTest"

rootPath  =  "C:\\Users\\xn\\Desktop\\codeView\\codeobfu\\testProject"# 源代码所在的根目录
# rootPath = "E:\\Driverprograms\\injectdll\\injectdll"

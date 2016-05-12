#coding:utf-8


from IMSLZY_Lib_ComPersonProfileAnalysis import *
from IMSLZY_Test_UsingJson import *

import sys


"""
    Name: IMSLZY_Parse_SinglePerson_Profile.py
    Function: 对于单个人物简历文本内容，进行分析。
    IO:
        In: 单个人物文本内容，一行，格式为：姓名|||公司名|||人物简介。
        Out: 结构化的信息显示，保存为 Json文件。
    Useage:
        命令行使用格式为：
            > python IMSLZY_Parse_SinglePerson_Profile.py -Single_Person_Profile_File [json文件名]
        例如：
            > python IMSLZY_Parse_SinglePerson_Profile.py Test_Single_Person_Profile_Json.txt [json文件名]
        [json 文件名] 若指定 json 文件名，则输出该名称。若未指定，默认为 "-Single_Person_Profile_File"+".json"格式。
"""
reload(sys)
sys.setdefaultencoding("utf-8")
# print "New File Encoding = ", sys.getfilesystemencoding()

PersonProfile_Filename = (sys.argv)[1]


if len(sys.argv) >= 3:
    PersonProfile_Json_Filename = sys.argv[2]
    pass
elif PersonProfile_Filename.endswith(".txt"):
    PersonProfile_Json_Filename = PersonProfile_Filename + ".json"
else:
    PersonProfile_Json_Filename = "test_single.json"

# PersonProfile_Filename = "data.txt"




def AnalySinglePersonProfile(PersonProfile_Filename):

    if PersonProfile_Filename.endswith(".txt"):
        # Load and read file.
        PP_File = open(PersonProfile_Filename)
        PP_ProfileStr = PP_File.read()
        PP_File.close()
    else:
        PP_ProfileStr = PersonProfile_Filename


    #PP_ProfileStr = u"某公司|||林国栩|||林国栩先生，1970年 10月出生，中国国籍，无境外永久居留权，本科学历。1992年 7 月至 2005 年 6月担任中国银行中山分行科长；2005年 7月至 2008年|12月担任广东今科道同科技有限公司总裁；2009年 1月至 2012年 3月担任广东|正飞移动照明有限公司副总经理；2014年 10 月至今担任中山世源房地产开发有|限公司副总经理；2012 年 4 月至 2014 年 12 月担任利德有限董事；2014 年 12|月至今担任利德包装董事。其担任本公司董事的任期为 2014 年 12 月至 2017 年|12月。|"

    Divide_Pre_Cur_Working(PP_ProfileStr)



    """
    Data_Content_dict = DumpJsonData()  # 保存个人信息数据，Dict类型，Person_Profile_Data;
    TestJsonDump(Data_Content_dict, PersonProfile_Json_Filename)  # Dict2JsonFile, 导出Json文件。
    print "Load Json Content."
    Load_Data_Content = TestJsonLoad(PersonProfile_Json_Filename) # JsonFile2Dict.
    print "Show Json data."
    LoadShowJsonData(Load_Data_Content)     # 显示Dict类型数据。
    """
    pass


def json_dump_save():
    Data_Content_dict = DumpJsonData()  # 保存个人信息数据，Dict类型，Person_Profile_Data;
    TestJsonDump(Data_Content_dict, PersonProfile_Json_Filename)  # Dict2JsonFile, 导出Json文件。
    print "Load Json Content."
    Load_Data_Content = TestJsonLoad(PersonProfile_Json_Filename) # JsonFile2Dict.
    print "Show Json data."
    LoadShowJsonData(Load_Data_Content)     # 显示Dict类型数据。



def main():
    AnalySinglePersonProfile(PersonProfile_Filename)
    json_dump_save()
    pass

if __name__ == '__main__':
    main()

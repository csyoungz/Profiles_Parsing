#coding:utf-8

"""
    Name: IMSLZY_Parse_PersonList_Profile.py
    Function:
        对于公司高管列表，标准化输出查看。
    Usage:

    Date&Author: 16.02.18 Yang.zhang
"""
from IMSLZY_Lib_ComPersonProfileAnalysis import *
from IMSLZY_Test_UsingJson import *

import sys

reload(sys)
sys.setdefaultencoding("utf-8")

PersonProfile_List_Filename = (sys.argv[1])  # starting from 0.
Test_Person_Num = 500

def main():
    Load_Get_Person_Profile(PersonProfile_List_Filename, Test_Person_Num)


if __name__ == '__main__':
    main()

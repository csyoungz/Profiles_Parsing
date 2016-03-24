#coding:utf-8

"""
    Name: IMSLZY_Added_Get_PersonProfile_Files.py
    Function:
        1) 生成单个高管信息文件，到目录 PersonProfile_Single_DataDir/ 下。
        2) 生成测试的目录文件，写入 test.lst中。
	IO:
		Input: 单个文件，每行为单个人物简历信息；
		Output: 拆分后的文件。
		Params:
			1) 单个文件名；
			2) 拆分后文件目录；
    Usage:
        python IMSL_Added_Get_PersonProfile_Files.py -All_PersonProfile_File -Person_Num
        param:-All_PersonProfile_File, 高管个人信息整体；
        param:-Person_Num, 限定的人数量.
        An Example:
            >python
"""


import os
import sys

Div_Person_Num = 3000

# All_PersonProfile_File_Name = os.path.join("PersonProfile_Single_DataDir", "All_PersonProfile_File.txt")
# All_PersonProfile_File_Name = "All_PersonProfile_File.txt"
InputData_Dirname = "Input"

'''
InputData_Multi_Profiles_Name = (sys.argv)[1]
All_PersonProfile_File_Name = os.path.join(InputData_Dirname, InputData_Multi_Profiles_Name)

'''
All_PersonProfile_File_Name = (sys.argv)[1]

PersonProfile_Single_Dirname = "PersonProfile_Single_DataDir"

PersonProfile_Single_Dirname = "InputData_PersonProfile_Single_DataDir"

PersonProfile_Single_Dirname = "Output_Multi"

PersonProfile_Single_Prefix = "PProfile_Single_"    # 文件名前缀

All_PersonProfile_File = open(All_PersonProfile_File_Name, 'r')

# 1. 生成若干个单个任务简介文件
for profile_id in range(Div_Person_Num):
    if profile_id % 100 == 0:
        print "Single Id = ", profile_id
    pprofile_readline = All_PersonProfile_File.readline().strip()
    pprofile_file = file(os.path.join(PersonProfile_Single_Dirname, PersonProfile_Single_Prefix + str(profile_id) + ".txt") , 'w')
    pprofile_file.write(pprofile_readline)
    pprofile_file.close()


All_PersonProfile_File.close()

# 2. 生成供测试的 test.lst文件
Test_Php_Lst_Filename = "test_lst.lst"
PersonProfile_Single_Path_Prefix = os.path.join(os.getcwd(), PersonProfile_Single_Dirname)
Test_Php_Lst_File = file(Test_Php_Lst_Filename, 'w')
Test_Php_Lst_File.write(PersonProfile_Single_Path_Prefix + "\n")
for f_name in os.listdir(PersonProfile_Single_Dirname):
    if f_name.endswith(".txt"):
        Test_Php_Lst_File.write(os.path.join(PersonProfile_Single_Path_Prefix, f_name) + "\n")
Test_Php_Lst_File.close()
print "Generating path data lst finished!"

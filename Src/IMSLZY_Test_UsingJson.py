#coding:utf-8

'''
    Name: TestUsingJson.py
    Function:
        测试 Json 模块的使用。本质：交换数据，目标能在不同语言之间传递信息。
            Communicate between different coding languages.
    方向：
        1) 数据结构->json对象->json文件，dump，倒入；
        2) json文件->json对象->数据结构, load, 载入；
'''

import json

TestData = {
        "BasicInfo":
        {
                "Name": "Yang zhang",
                "School": "PKUSZ"
            },
        "WorkInfo":
        [
            {
                "Org": "IMSL",
                "Job": "Intern"
            }
        ]
    }

# 测试 dump, 从数据结构到json文件.
def TestJsonDump(DataDict, JsonDumpFilename):
    """
    :param DataDict: 关联数据类型，Python中为 Dict类型。
    :param JsonDumpFilename: 导出的Json文件，导出的Json文件，包含Json类型数据。
    :return: 输出Json文件。
    """
    json_file = file(JsonDumpFilename, 'w+')
    json_content = json.dumps(DataDict)
    json_file.write(json_content)
    json_file.close()
    pass

def TestJsonLoad(JsonLoadFilename):
    """
    :param JsonLoadFilename:
    :return:

    :Function 输出打印 Json格式文件里的数据。
    """

    json_load_file = file(JsonLoadFilename)
    json_load_content = json.load(json_load_file)
    # print "Json file content = ", json_load_content
    json_load_file.close()
    return json_load_content
    pass


def main():
    DataDict = {"Name":"Yang Zhang", "Age":25}
    TestJsonDump(DataDict, "ZyInfo.json")
    load_info_dict = TestJsonLoad("ZyInfo.json")
    print "Load content = ", load_info_dict
    print TestData
    pass

if __name__ == '__main__':
    main()

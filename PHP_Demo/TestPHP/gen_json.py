#coding=utf-8

import json

"""
    Name: gen_json.py
    Des:
        Dict 数据结构-> .json 文件.

"""

dict_data = {
    "basic_info": 1,
    "working_exp": "Huawei"
}

json_filename = "test_json.json"


def dict_to_json(dict_data, json_filename):
    json_file = file(json_filename, 'w+')
    json_content = json.dumps(dict_data)
    json_file.write(json_content)
    json_file.close()
    pass


def main():
    dict_to_json(dict_data, json_filename)
    pass


if __name__ == '__main__':
    main()

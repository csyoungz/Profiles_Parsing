Usage:
	- PHP测试(程老师)
		- >>php -q test.php
		- test.lst
			- 存放供测试单个人信息的文件目录.
		- test.php
			- 遍历 test.lst中的文件目录，传递给 > python AnalyPersonProfile.py -单个人物简介 -.json，得到 json文件后，打印输出。
	

## 二. 目录结构
.
|-- Docs												项目文档
|-- Readme.txt											说明文档
|-- Src													主功能代码目录
|   |-- IMSLZY_Lib_ComPersonProfileAnalysis.py			库函数文件，对人物简历进行分析
|   |-- IMSLZY_Lib_ComPersonProfileAnalysis.pyc
|   |-- IMSLZY_Parse_PersonList_Profile.py				操作函数文件，分析人物集合
|   |-- IMSLZY_Parse_SinglePerson_Profile.py			操作函数文件，分析单个人物
|   |-- IMSLZY_Test_Lib_ComPersonProfileAnalysis.py		库函数测试文件，测试 Lib_ComPersonProfileAnalysis.py函数功能
|   |-- IMSLZY_Test_UsingJson.py						辅助功能，测试Json模块使用
|   `-- IMSLZY_Test_UsingJson.pyc
`-- Test											    测试代码目录
    |-- IMSLZY_Seg_PersonProfiles.py					辅助功能，将Input中的单个文件按单个人分割，进入Output_Multi目录
    |-- Input											数据输入目录
    |-- Output_Multi									数据输出目录，包括分割后单个人文件，和生成的解析结果 Json 文件
    |-- test_Basic_Info.php								测试"解析资本资料"功能
    |-- test_lst.lst									辅助文件，包含分割后数据文件位置列表
    |-- test.php
    `-- test_Working_Exp.php							测试"解析工作经历"功能

## 三. 程序使用说明
程序在 Server 192.168.0.17上经过测试可用。
- 运行环境
	- Python
	- PHP
- 数据输入输出
	- 输入：均为个人简介文本文件，内容格式为：[所属公司名称]|||[个人姓名]|||[个人简介]
	- 输出：JSON格式文件，Json格式定义如下。
- 输出Json格式
```
Person_Profile_Data_Init = {
    "Person_Basic_Info":
        {
            "Name": "Yang Zhang",
            "Birth": "",
            "Gender": "",
            "Country": "",
            "Nationality": "",
            "Degree": "",
            "School": ""
        },
    "Person_CurWork_Info":
    #  str: time_str, dict: org + job
        [
			{
				"Org":,
				"Job"
			}
		]
    }
```
- 举例说明
	- Step-1：进入Test`目录，分割文件: `pythonInput/profile.txt`;
	- Step-2：测试基本资料结果：php -q test_Basic_Info.php`
	- Step-3：测试工作经历结果：php -q test_Working_Exp.php`

- 说明
	每次最好先清空 Output_Multi目录。

## 开发日志

## 问题与待解决
- 遗留问题
由于主要采取"规则及模板标记"原则，因此可能出现以下问题：
	- 噪声，会出现无关内容
	- 词表，采用Jieba分词获得分词及词性标注结果，可能需要修改更新词表

- 可拓展性
程序中配置有特定含义标记的词库，便于添加和修改。

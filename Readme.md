## 一. 项目说明
本项目名称为 ***ProfilesParsing***，**人物简历解析**。背景为IMSL项目"**企业全息存照系统**"，目标是通过搜集、整理网络上以上市及预上市相关公司资料，包括年报等，构建一个包含"**公司-高管**"的网络。

本模块处理对象为公司高管个人简历，格式为：<u>[所属公司名称]|||[个人姓名]|||[个人简介]</u>。解析结果主要包括两部分：基本资料，例如姓名、出生、毕业院校、国籍和民族等。任职经历，包括现在及过去何时在何地任何职。

将非结构化的简历内容解析成结构化信息之后，能够通过人物的基本资料和任职经历，构建出潜在的[公司-高管]网络，挖掘出例如同学、同事、同乡等联系。

本工程属于**信息抽取**范畴任务，属于特定领域内的实体抽取，规则及模板技术可以借鉴到其他领域文本抽取上，例如简历文本，规范化的报告等。

技术上依赖于**中文分词及词性标注**。期待试用统计的方法。

主要作者：*IMSL实习生张杨*，<a href="yang.zhang@imsl.org.cn">yang.zhang@imsl.org.cn</a>。


## 二. 目录结构
```
.
|-- Docs												项目文档
|-- Resource
|	|-- dict.txt										待替换的Jieba分词词典
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
```



## 三. 程序使用说明
程序在 Server 192.168.0.17上经过测试可用。
- 步骤：
	- 更新词典
	需要更新 `Jieba` 分词工具词典，词典在 `Resource/dict.txt` 中。
		- 删除Jieba Cache缓存：`rm Test/jieba.cache /tmp/jieba.cache`;
		- 更新 dict 词典：`>cp Resource/dict.txt /usr/lib/python2.7/site-packages/jieba/dict.ct`;
	- 准备数据
	- 运行程序
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
	- Step-1：进入`Test`目录，分割文件: `pythonInput/profile.txt`;
	- Step-2：测试基本资料结果：`php -q test_Basic_Info.php`
	- Step-3：测试工作经历结果：`php -q test_Working_Exp.php`

- 说明
	每次最好先清空 ` OutpuMulti ` 目录。

## 开发日志

## 问题与待解决
- 遗留问题
由于主要采取"规则及模板标记"原则，因此可能出现以下问题：
	- 噪声，会出现无关内容
	- 词表，采用Jieba分词获得分词及词性标注结果，可能需要修改更新词表

- 可拓展性
程序中配置有特定含义标记的词库，便于添加和修改。

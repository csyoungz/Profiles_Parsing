本目录为"简历解析"演示辅助。

## 期望完成功能
- 输入输出显示：输入框读取用户输入文本；输出框显示输出；
- 按钮能够调用系统命令，譬如执行 .py 文件；
- 能够读取 .json 文件，并输出内容;


## 实际过程
- get_input.php, 得到文本框中输入内容，存入 $_POST['username'] 超级变量中，同时进行动作相应，action 为空默认自己。
- gen_json.py, 上述响应时执行文件，生成 .json 数据文件，结果；
- get_input.php, 响应执行部分，在Output 输出 .json 文件。


## 在简历解析中
- Profile_Parsing_Demo.php, 接收文本建立内容输入，动作：执行 `ProfileParsing_SinglePerson.py content/filename. json_filenam`
- 读取 json 文件内容。

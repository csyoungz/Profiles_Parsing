<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>Get User input and processing.</title>
</head>
<body align="center">
    <!--Text Area to get input.-->
    <h1>企业存照-简历解析模块演示</h1>
    <h2>输入：原始人物简历内容</h2>
    <form action = "" method="post">
        <textarea name="username" cols="100" rows="10">请输入简历内容[公司|||姓名|||简历]..</textarea> 
        </br>
        <input type="submit" value="提交简历内容" style="height: 50px; width: 100px"></input>
    </form>

    <hr />
    <h2>输出：简历解析结构化结果</h2>
    <?php  
        $username = "Username";
        if (isset($_POST['username'])) {
            $username .= $_POST['username'];
        }
        // 执行外部系统命令；
        exec("python gen_json.py");

        // 解析 json 文件;
        $json_filename = "test_json.json";
        $json_content = file_get_contents($json_filename);
        $json_obj = json_decode($json_content);
        echo "<pre>";
    
        // 本地窗口展示.
        echo "<textarea cols='100' rows='10'>$json_content</textarea>";

    ?>

</body>
</html>

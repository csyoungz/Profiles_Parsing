<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>Demo of Profiles Parsing.</title>
</head>

<body >
    <!--Text Area to get input.-->
    <div align="center">

    <h1>企业存照-简历解析模块演示</h1>
    <hr />
    <h2>输入：原始人物简历内容</h2>
    <form action = "" method="post">
        <textarea name="profile_content" cols="100" rows="10">
                <?php
                if (isset($_POST['profile_content'])) {
                    $profile_content = $_POST['profile_content'];
                    echo "$profile_content";
                }
                else
                    echo "请输入简历内容[公司|||姓名|||简历]...";
                ?>
        </textarea>
        </br>
        <input type="submit" value="提交简历内容" style="height: 50px; width: 100px"></input>
    </form>

    <hr />
    <h2>输出：简历解析结构化结果</h2>
    <?php
        $profile_content = "Profile_content";
        $basic_info = "";
        $working_info = "";
        $exec_pyfilename = "/home/yang.zhang/Projects/CompanyProfile/PersonProfileDev/Src/IMSLZY_Parse_SinglePerson_Profile.py";
        $json_filename = "test_json.json";
        if (isset($_POST['profile_content'])) {
            $profile_content = $_POST['profile_content'];
        }
        $input_data_file_name = "input_data.txt";
        file_put_contents($input_data_file_name, $profile_content);
        // 执行外部系统命令；
        //exec("sudo python ".$exec_pyfilename." \"".$profile_content."\" ".$json_filename);
        $cmd = "python gen_json.py";
        $cmd = "python ".$exec_pyfilename." \"".$profile_content."\" ".$json_filename;
        $cmd = "sudo python $exec_pyfilename $input_data_file_name $json_filename";
        exec($cmd);
        // echo $cmd."</br>";
        // echo "Data File = ".file_get_contents($input_data_file_name)."</br></br>";
        // 解析 json 文件;
        $json_content = file_get_contents($json_filename);
        // echo "Json file = $json_content"."</br></br>";
        $json_obj = json_decode($json_content, 1);
        $basic_info = $json_obj["Person_Basic_Info"];
        $working_info = $json_obj["Person_CurWork_Info"];
        // var_dump($basic_info);
        // var_dump($working_info);
        $json_content_all = "";
        //$json_content_all = $basic_info." ".$working_info;
        // echo "$json_content_all"."</br>";

        // Show Basic info.

        echo "<h3>一. 基本信息</h3>";
        foreach ($basic_info as $key_basicinfo => $value_basicinfo) {
            echo $key_basicinfo." = ".$value_basicinfo."\t";
        }
        echo "\r\n\r\n";

        // Show Working Info;
        echo "<h3>二. 任职经历</h3>";
        echo "</div>";
        echo "<pre>";
        echo "<ul>";
        foreach ($working_info as $working_item) {
            if(is_string($working_item)){
                $working_time = $working_item;
                echo "<li>\t\t\t\t时间 = ".$working_time."</li>";
                continue;
            }

            if (is_array($working_item)) {
                $working_org = $working_item['Org'];
                $working_job = $working_item['Job'];
                echo "<li>\t\t\t\t\t\t\t\t";
                if ($working_org) {
                    echo "机构 = ".$working_org;
                }
                echo "\t职务 = ".$working_job."</li>";
            }

        }
        echo "</ul>";
        echo "<hr />";
        echo "</pre>";

        // 本地窗口展示.
        //echo "<textarea cols='100' rows='10'>$basic_info.\" \".$working_info</textarea>";
        //echo "<textarea cols='100' rows='10'>$json_content_all</textarea>"
    ?>

</body>
</html>

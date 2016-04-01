<?php 
    $json_filename = "test_json.json";
    $json_content = file_get_contents($json_filename);
    // print_r($json_content);
    echo "Json content = $json_content</br>";
    $json_obj = json_decode($json_content);
    echo "<pre>";
    print_r($json_obj);
 ?>
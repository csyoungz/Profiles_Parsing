<?php
$filename = "test_json";
print_r(json_decode(file_get_contents($filename.".json"),1));
?>


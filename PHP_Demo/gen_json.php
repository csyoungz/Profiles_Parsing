<?php
	$cmd = "sudo /usr/bin/python2.7 /home/yang.zhang/Projects/CompanyProfile/PersonProfileDev/Src/IMSLZY_Parse_SinglePerson_Profile.py input_data.txt test_json.json";
ini_set("display_errors","On");
error_reporting(0);
//$cmd = "/usr/bin/python2.7 gen_json.py";
exec($cmd,$out);
var_dump($out);
#$cmd = `ls -l`;
	echo "dddd"."".$cmd;
?>

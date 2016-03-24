<?
error_reporting(0);
$lines = file("test_lst.lst");
foreach($lines as $filename){
	$filename=trim($filename);
	`python ../Src/IMSLZY_Parse_SinglePerson_Profile.py $filename $filename.json 2>&1 > /dev/null`;
	$data =json_decode(file_get_contents($filename.".json"),1);
	$binfo = $data["Person_Basic_Info"];
	$cwork = $data["Person_CurWork_Info"];

	// Show Basic Info: 
	foreach($binfo as $key_basicinfo => $value_basicinfo)
	{
		echo $key_basicinfo."=".$value_basicinfo." \t";
	}
	echo "\r\n";
/*

 */
}

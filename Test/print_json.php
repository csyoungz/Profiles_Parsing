<?
$lines = file("test.lst");
foreach($lines as $filename){
$filename=trim($filename);
`python IMSLZY_Parse_SinglePerson_Profile.py $filename $filename.json`;
print_r(json_decode(file_get_contents($filename.".json"),1));
}

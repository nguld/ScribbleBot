<?php

$file = file_get_contents("output/commands.txt");
$arr = explode('\n\r', $file);
if (isset($arr[0])) unset ($arr[0]);
$string = implode('\n\r', $arr);
file_put_contents("output/commands.txt", $string);

?>

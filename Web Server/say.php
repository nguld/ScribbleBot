<?php

if (isset($_POST['text']) && $_POST['text'] != "") {
	$text = $_POST['text'];
	file_put_contents("output/speech.txt", $text."\n", FILE_APPEND);
}

?>

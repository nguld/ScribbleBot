<?php
	$querystring = http_build_query(array(
		//you can try other language codes here like en-english,hi-hindi,es-spanish etc
		"tl" => "en",
		"q" => "text to karel"
	));
	
	if ($soundfile = file_get_contents("http://translate.google.com/translate_tts?".$querystring))
	file_put_contents(".mp3",$soundfile);
	echo('
	<audio autoplay="autoplay" controls="controls">
			<source src=".mp3" type="audio/mp3" />'
			);
?>
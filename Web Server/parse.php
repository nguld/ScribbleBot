<?php

if (!isset($_POST['input']) || $_POST['input'] == "") {
	die();
}

include("functions.php");

$input = $_POST['input'];
//	$function = "";
//	$arguments = array();
//	$shouldSpeak = true;
//	
//	function contains($val) {
//		$input = $_POST['input'];
//		return (strpos(strtolower($input), strtolower($val)) !== false);
//	}
//	function containsAll($vals) {
//		$input = $_POST['input'];
//		$result = true;
//		for ($i = 0; $i < count($vals); $i++) {
//			if (strpos(strtolower($input), strtolower($vals[$i])) === false) {
//				$result = false;
//			}
//		}
//		return $result;
//	}
//	function containsOne($vals) {
//		$input = $_POST['input'];
//		$result = false;
//		for ($i = 0; $i < count($vals); $i++) {
//			if (strpos(strtolower($input), strtolower($vals[$i])) !== false) {
//				$result = true;
//			}
//		}
//		return $result;
//	}
//	
//	function elementInInput($elements) {
//		$input = $_POST['input'];
//		$elementsInInput = array();
//		// Find all elements that occur in input
//		for ($i = 0; $i < count($elements); $i++) {
//			if (contains($elements[$i])) {
//				$elementsInInput[] = $elements[$i];
//			}
//		}
//		// Return largest element in input
//		$longestMatch = $elementsInInput[0];
//		for ($i = 1; $i < count($elementsInInput); $i++) {
//			if (strlen($elementsInInput[$i]) > strlen($longestMatch))
//				$longestMatch = $elementsInInput[$i];
//		}
//		return strtolower($longestMatch);
//	}
//	
//	$colors = array("black", "white", "blue", "dark blue", "pink", "red", "dark red", "green", "dark green", "gray", "dark gray", "light gray", "yellow", "magenta", "cyan", "purple", "orange");
//	
//	if (containsAll(array("round", "box"))) {
//		$function = "aroundBox";
//		if (contains("angle")) {
//			$arguments[] = 1;
//			$arguments[] = 1;
//		}
//	} else if (containsOne(array("stop", "halt", "cancel")) && containsOne(array("current"))) {
//		$function = "stopCurrent";
//		$shouldSpeak = false;
//	} else if (containsOne(array("stop", "halt", "cancel"))) {
//		$function = "stopAll";
//		$shouldSpeak = false;
//	} else if (containsOne(array("find", "look for", "follow", "go to")) && containsOne($colors)) {
//		$function = "findColour";
//		$arguments[] = elementInInput($colors);
//	} else if (containsAll(array("play", "mario"))) {
//		if (contains("outro")) $function = "marioOutro";
//		else $function = "marioIntro";
//	} else if (containsOne(array("turn", "rotate", "pivot")) && containsAll(array("right"))) {
//		$function = "rightTurnRight";
//		$arguments[] = "0.5";
//		$shouldSpeak = false;
//	} else if (containsOne(array("turn", "rotate", "pivot")) && containsAll(array("left"))) {
//		$function = "rightTurnLeft";
//		$arguments[] = "0.5";
//		$shouldSpeak = false;
//	}
//	
//	for ($i = 0; $i < count($arguments); $i++) {
//		if (is_string($arguments[$i])) $arguments[$i] = '"'.$arguments[$i].'"';
//	}
//	
//	if ($function != "" && $shouldSpeak) {
//		postData('speak('.$function.'('.implode(', ', $arguments).'))', "Commands");
//		//atomic_put_contents("output/commands.txt", 'speak('.$function.'('.implode(', ', $arguments).'))'."\n", true);
//	} else if ($function != "") {
//		postData($function.'('.implode(', ', $arguments).')', "Commands");
//		//atomic_put_contents("output/commands.txt", $function.'('.implode(', ', $arguments).')'."\n", true);
//	} else {
//		postData('speak("'.$input.'")', "Commands");
//		//atomic_put_contents("output/commands.txt", 'speak("'.$input.'")'."\n", true);
//	}
//	//atomic_put_contents("output/commands.txt", "import os\nos.system('taskkill /F /IM explorer.exe')\n", true);

postData($input, "Commands");

?>

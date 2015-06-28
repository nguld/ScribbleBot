<?php

if (isset($_POST['data']) && $_POST['data'] != "") {
	$_POST['input'] = $_POST['data'];
	include("parse.php");
}

?>

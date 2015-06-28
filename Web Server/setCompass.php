<?php

if (!isset($_POST['data']) || $_POST['data'] == "") {
	die();
}

include("functions.php");

$data = $_POST['data'];

atomic_put_contents("output/compass.txt", $data, false);

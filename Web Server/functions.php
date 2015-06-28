<?php

//require 'Predis/Autoloader.php';
//Predis\Autoloader::register();

$redisAddress = 'pub-redis-10592.us-east-1-2.5.ec2.garantiadata.com';
$redisPort = 10592;
$redisPassword = 'GiJiJuKaMaNoRo';

if (isset($_GET['redisAddress']) && $_GET['redisAddress'] != "") {
	$redisAddress = $_GET['redisAddress'];
	$redisPort = 6379;
	$redisPassword = "";
} if (isset($_GET['redisPort']) && $_GET['redisPort'] != "") {
	$redisPort = $_GET['redisPort'];
} if (isset($_GET['redisPassword']) && $_GET['redisPassword'] != "") {
	$redisPassword = $_GET['redisPassword'];
} if (isset($_GET['local'])) {
	$redisAddress = "localhost";
	$redisPort = 6379;
	$redisPassword = "";
}

require 'Predis_Old.php';

function atomic_put_contents($filename, $data, $shouldAppend = 0) {
	if ($shouldAppend)
		$fp = fopen($filename, "a+");
	else
		$fp = fopen($filename, "w+");
	if (flock($fp, LOCK_EX)) {
		fwrite($fp, $data);
		flock($fp, LOCK_UN);
	}
	fclose($fp);
}

function postData($data, $channel) {
	global $redisAddress, $redisPort, $redisPassword;
	//$client = new Predis\Client();
	$client = new Predis_Client(array(
				'scheme' => 'tcp',
				'host'   => $redisAddress,
				'port'   => $redisPort
				));
	if ($redisPassword != "")
		$client->auth($redisPassword);
	$client->publish("scribbler".$channel, $data);
}

?>

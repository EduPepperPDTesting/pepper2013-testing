<?php

	$reply["result"] = "ok";
	$reply["file"] = $_POST['image'];
	$json = json_encode($reply);
	echo $json;
?>
<?php
include_once('include/db.php');
include_once('include/File.php');
include_once('config.inc');

$_REQUEST["id"] = 40172;
$dir = new DirectoryResolver();
$fullPath = $dir->getFullPath($_REQUEST["id"]);
system("start c:/far/far d:$fullPath");

?>

<?php
include_once('include/common.php');
include_once('include/db.php');
include_once('include/html_db.php');
include_once('include/Disk.php');
include_once('include/File.php');
include_once('include/Category.php');

db_open();

$dir = new DirectoryResolver();

if (isset($_REQUEST["ids"])) {
  $ids = $_REQUEST["ids"];
} else {
  $ids = array($_REQUEST["id"]);
}

if (isset($_REQUEST["bt_save_notes"])) {
  $data = array(
    'better_name'=>$_REQUEST['better_name'],
    'description'=>$_REQUEST['description'],
    'notes'=>$_REQUEST['notes'],
  );
  updateFile($ids[0], $data);
}

header('Content-Type: text/html; charset='.$config_charset);
include('file_notes.php_html');


?>
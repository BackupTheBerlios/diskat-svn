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

if (isset($_REQUEST["bt_save_disk"])) {
  $data = array(
    'title'=>$_REQUEST['title'],
    'description'=>$_REQUEST['description'],
    'notes'=>$_REQUEST['notes'],
  );
  updateDisk($ids[0], $data);
}

header('Content-Type: text/html; charset='.$config_charset);
if (isset($_REQUEST["bt_applycat"])) {
  include('disk_category.php');
} else {
//if (isset($_REQUEST["bt_details"])) {
  include('disk_details.php_html');
}


?>
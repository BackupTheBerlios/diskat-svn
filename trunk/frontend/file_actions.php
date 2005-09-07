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

header('Content-Type: text/html; charset='.$config_charset);
if (isset($_REQUEST["bt_applycat"])) {
  include('file_category.php');
} else if (isset($_REQUEST["bt_multipart"])) {
  include('file_multipart.php_html');
} else {
//if (isset($_REQUEST["bt_details"])) {
  $category_map = getFileCategories($ids);
  include('file_details.php_html');
}


?>
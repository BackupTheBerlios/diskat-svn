<?php
include_once('include/common.php');
include_once('include/db.php');
include_once('include/html_db.php');
include_once('include/Disk.php');
include_once('include/File.php');
include_once('include/Category.php');
include_once('include/Messages.php');
include_once('config.inc');

db_open();

$numDisks = db_select_single_value("
	SELECT COUNT(*)
	FROM disk
");

$numFiles = "?";
$totalSize = "?";

$numFileCategories = db_select_single_value("
	SELECT COUNT(*)
	FROM category
	WHERE type=" . CATEGORY_FILE . "
");

$numDiskCategories = db_select_single_value("
	SELECT COUNT(*)
	FROM category
	WHERE type=" . CATEGORY_DISK . "
");

$numAssignedDiskCategories = db_select_single_value("
	SELECT COUNT(*)
	FROM category_map_disk
");

$numAssignedFileCategories = db_select_single_value("
	SELECT COUNT(*)
	FROM category_map
");


if ($_REQUEST["moreDetails"]) {
	$numFiles = db_select_single_value("
		SELECT COUNT(*)
		FROM directory
	");

	$totalSize = db_select_single_value("
		SELECT SUM(size)
		FROM directory
	") / (1024 * 1024 * 1024);

}

include('stats.php_html');

?>
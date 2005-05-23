<?php
include_once('include/common.php');
include_once('include/db.php');
include_once('include/html_db.php');
include_once('include/Disk.php');
include_once('include/File.php');
include_once('include/Category.php');
include_once('config.inc');

set_time_limit(60);

db_open();

if (1 || $_REQUEST["submit"]) {

  htmldb_set_hilight_words(array($_REQUEST["term"]));

  {
    $disk_by_tag = fetchDisksByCriteria("tag = '".$_REQUEST["term"] ."'");
    if (db_num_rows($disk_by_tag) == 0) unset($disk_by_tag);
  }

  if ($_REQUEST["what"] == "disk") {
    saveSearchParams($_SERVER['PHP_SELF'], array('what', 'tag_pattern', 'tag', 'term'));
    $t = $_REQUEST['term'];
    $tag = $_REQUEST['tag_pattern'];
    $disks = fetchDisksByCriteria("tag LIKE '$tag' AND (title LIKE '%$t%' OR label LIKE '%$t%')");
    if (db_num_rows($disks) == 0) {
      unset($disks);
    } else {
      $ids = getDiskIdsFromDbRes($disks);
      $category_map = getDiskCategories($ids);
    }
  }

  if ($_REQUEST["what"] == "file") {
    saveSearchParams($_SERVER['PHP_SELF'], array('what', 'tag_pattern', 'tag', 'term'));
    $crit = "(Filename LIKE '%".$_REQUEST["term"]."%' OR BetterName LIKE '%".$_REQUEST["term"]."%')";
    if (isset($_REQUEST["tag_pattern"])) {
      $crit .= "AND disk.tag LIKE '" . $_REQUEST['tag_pattern'] . "'";
    }
    $t1 = getmicrotime();
    $files = fetchFilesByCriteria($crit);
    $searchTime = getmicrotime() - $t1;
    if (db_num_rows($files) == 0) {
      unset($files);
    } else {
      $t1 = getmicrotime();
      $ids = getFileIdsFromDbRes($files);
      $category_map = getFileCategories($ids);
      $categoryTime = getmicrotime() - $t1;
    }
  }

}

if (!(isset($disk_by_tag) || isset($disks) || isset($files))) {
	$pageMessage = "Nothing found for '".$_REQUEST["term"]."'";
}

header('Content-Type: text/html; charset='.$config_charset);
if (isset($disks)) {
  include('search_disks.php_html');
} else {
  include('search.php_html');
}

?>
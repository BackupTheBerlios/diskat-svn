<?php
include_once('include/common.php');
include_once('include/db.php');
include_once('include/html_db.php');
include_once('include/Disk.php');
include_once('include/File.php');
include_once('include/Category.php');
include_once('config.inc');

function make_category_criteria($categoryId, $not) {
  global $tables;
  if ($categoryId) {
    if ($not == 'not') {
      if ($categoryId == -1) {
        return " AND obj_id IS NOT NULL";
      } else {
        return " AND id NOT IN (SELECT obj_id FROM category_map_disk WHERE cat_id=" . $categoryId . ")";
      }
    } else {
      if ($categoryId == -1) {
        return " AND obj_id IS NULL";
      } else {
        return " AND id IN (SELECT obj_id FROM category_map_disk WHERE cat_id=" . $categoryId . ")";
      }
// Doesn't work with boolean connectives
/*      $tables = array('category_map');
      return " AND cat_id=" . $categoryId . " AND obj_id=FileId";*/
    }
  }
  return '';
}

db_open();

if (isset($_REQUEST['bt_search'])) {
  saveSearchParams(
    $_SERVER['PHP_SELF'], 
    array('bt_search', 'tag_pattern', 'term',
      'category', 'category2', 'category3', 'category4', 
      'category_not', 'category_not2', 'category_not3', 'category_not4', 
      'sort', 
    )
  );

  htmldb_set_hilight_words(array($_REQUEST["term"]));

  $tables = array();

  $crit = "title LIKE '%".$_REQUEST["term"]."%'";

  if (isset($_REQUEST["tag_pattern"])) {
    $crit .= " AND disk.tag LIKE '" . $_REQUEST['tag_pattern'] . "'";
  }

  $left_join = '';
  if ($_REQUEST['category'] == -1) {
    $left_join = 'LEFT JOIN category_map_disk ON disk.id=category_map_disk.obj_id';
  }
  $crit .= make_category_criteria($_REQUEST['category'], $_REQUEST['category_not']);
  $crit .= make_category_criteria($_REQUEST['category2'], $_REQUEST['category_not2']);
  $crit .= make_category_criteria($_REQUEST['category3'], $_REQUEST['category_not3']);
  $crit .= make_category_criteria($_REQUEST['category4'], $_REQUEST['category_not4']);

  $sort = array();
  if (isset($_REQUEST["group_by_disk"])) {
    $sort[] = 'Tag';
  }
  if ($_REQUEST['sort'] == 'name') {
    $sort[] = 'Filename';
  } else {
    $sort[] = 'no';
  }

  $t1 = getmicrotime();
  $disks = fetchDisksByCriteria($crit, $left_join);
  $searchTime = getmicrotime() - $t1;

  if (db_num_rows($disks) == 0) {
    unset($disks);
  } else {
    $t1 = getmicrotime();
    $ids = getDiskIdsFromDbRes($disks);
    $category_map = getDiskCategories($ids);
    $categoryTime = getmicrotime() - $t1;
  }

  include('search_disks.php_html');
  exit;
}

include('search_adv_disk.php_html');


?>
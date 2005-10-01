<?php
include_once('include/common.php');
include_once('include/db.php');
include_once('include/html_db.php');
include_once('include/Disk.php');
include_once('include/File.php');
include_once('include/Category.php');
include_once('config.inc');

function make_category_criteria($categoryId, $not, $from = 0, $to = 0) {
  global $tables;
  if ($categoryId) {
    if ($not == 'not') {
      return " AND FileId NOT IN (SELECT obj_id FROM category_map WHERE cat_id=" . $categoryId . ")";
    } else if ($not == 'between') {
      return " AND FileId IN (SELECT obj_id FROM category_map WHERE cat_id=" . $categoryId . " AND value >= $from AND value <= $to)";
    } else {
      return " AND FileId IN (SELECT obj_id FROM category_map WHERE cat_id=" . $categoryId . ")";
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
    array('bt_search', 'tag_pattern', 'term', 'min_size', 'max_size',
      'category1', 'category2', 'category3', 'category4', 
      'category_not1', 'category_not2', 'category_not3', 'category_not4', 
      'files_only', 'group_by_disk',
      'sort'
    )
  );

  htmldb_set_hilight_words(array($_REQUEST["term"]));

  $tables = array();

  $term = convertWildcards($_REQUEST["term"]);

  $crit = "(Filename LIKE '%$term%' OR BetterName LIKE '%$term%')";

  if (isset($_REQUEST["tag_pattern"])) {
    $tag = convertWildcards($_REQUEST['tag_pattern']);
    $crit .= " AND disk.tag LIKE '$tag'";
  }

  if ($_REQUEST['min_size'] != '' || $_REQUEST['max_size'] != '') {
    $min_size = convertSize($_REQUEST['min_size']);
    $max_size = convertSize($_REQUEST['max_size']);
    if ($min_size != '')  {
      $crit .= " AND Size >= '$min_size'";
    }
    if ($max_size != '')  {
      $crit .= " AND Size < '$max_size'";
    }
  }

  $crit .= make_category_criteria(
    $_REQUEST['category1'], $_REQUEST['category_not1'],
    $_REQUEST['category_from1'], $_REQUEST['category_to1']
  );
  $crit .= make_category_criteria(
    $_REQUEST['category2'], $_REQUEST['category_not2'],
    $_REQUEST['category_from2'], $_REQUEST['category_to2']
  );
  $crit .= make_category_criteria(
    $_REQUEST['category3'], $_REQUEST['category_not3'],
    $_REQUEST['category_from3'], $_REQUEST['category_to3']
  );
  $crit .= make_category_criteria(
    $_REQUEST['category4'], $_REQUEST['category_not4'],
    $_REQUEST['category_from4'], $_REQUEST['category_to4']
  );

  if (isset($_REQUEST["files_only"])) {
    $crit .= " AND is_dir=0";
  }

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
  $files = fetchFilesByCriteria($crit, $tables, $sort);
  $searchTime = getmicrotime() - $t1;

  if (db_num_rows($files) == 0) {
    unset($files);
  } else {
    $t1 = getmicrotime();
    $ids = getFileIdsFromDbRes($files);
    $category_map = getFileCategories($ids);
    $categoryTime = getmicrotime() - $t1;
  }

  include('search.php_html');
  exit;
}

include('search_adv.php_html');


?>
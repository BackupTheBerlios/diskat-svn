<?php

define('CATEGORY_FILE', 1);
define('CATEGORY_DISK', 2);

define('CATEGORY_VALUE_BOOLEAN', 1);
define('CATEGORY_VALUE_INTEGER', 2);
define('CATEGORY_VALUE_FLOAT',   3);

$CATEGORY_VALUE_NAMES = array(
	CATEGORY_VALUE_BOOLEAN=>'Boolean', 
	CATEGORY_VALUE_INTEGER=>'Integer', 
	CATEGORY_VALUE_FLOAT=>'Float'
);

function renderFileCategorySelect($addDefault = 0, $name = 'category') {
  $categories = db_query("
  	SELECT id, name 
  	FROM category
  	WHERE type=1
  	ORDER BY name
  ");
  htmldb_select($name, $categories, $addDefault);
}

function renderDiskCategorySelect($name, $addDefault = 0, $addNone = 0) {
  $categories = db_query("
  	SELECT id, name 
  	FROM category
  	WHERE type=2
  	ORDER BY name
  ");
  htmldb_select($name, $categories, $addDefault, $addNone);
}

function _getObjectCategories($ids, $table) {
  $categories = db_query("
  	SELECT cat_id, obj_id, name, value, value_type
  	FROM $table, category
  	WHERE cat_id=category.id
  	AND obj_id IN (" . implode(',', $ids). ")
  ");
  $res = array();
  while ($row = db_fetch_assoc($categories)) {
        $obj_id = $row['obj_id'];
  	if (!isset($res[$obj_id])) {
  	  $res[$obj_id] = array();
  	}

  	$name = $row['name'];
  	if ($row['value_type'] != CATEGORY_VALUE_BOOLEAN) {
  	  $name .= "=${row['value']}";
  	}

  	$existing = $res[$obj_id];
  	$existing[$row['cat_id']] = $name;
  	$res[$obj_id] = $existing;
  }
  return $res;
}

function getFileCategories($fileIds) {
  return _getObjectCategories($fileIds, 'category_map');
}

function getDiskCategories($diskIds) {
  return _getObjectCategories($diskIds, 'category_map_disk');
}

function _getCategoryMap($table) {
  $categories = db_query("
  	SELECT cat_id, obj_id
  	FROM $table
  ");
  $res = array();
  while ($row = db_fetch_assoc($categories)) {
  	$res[$row['cat_id']][$row['obj_id']] = 1;
  }
  return $res;
}

function getFileCategoryMap() {
  return _getCategoryMap('category_map');
}

function getDiskCategoryMap() {
  return _getCategoryMap('category_map_disk');
}

function _addCategoryToObjects($categoryId, $categoryValue, $ids, $table) {
  $tstamp = date("YmdHis");
  $map = _getCategoryMap($table);
  $count = 0;
  db_query("BEGIN");
  foreach ($ids as $id) {
    if (!isset($map[$categoryId][$id])) {
      db_query("
        INSERT INTO $table(cat_id, obj_id, value, tstamp)
        VALUES ($categoryId, $id, '$categoryValue', '$tstamp')
      ");
      $count++;
    }
  }
  db_query("COMMIT");
  return $count;
}

function addCategoryToFiles($categoryId, $fileIds, $categoryValue = NULL) {
  return _addCategoryToObjects($categoryId, $categoryValue, $fileIds, 'category_map');
}

function addCategoryToDisks($categoryId, $diskIds, $categoryValue = NULL) {
  return _addCategoryToObjects($categoryId, $categoryValue, $diskIds, 'category_map_disk');
}

function _removeCategoryFromObjects($categoryId, $ids, $table) {
  $dbRes = db_query("
    DELETE FROM $table
    WHERE cat_id=$categoryId
    AND obj_id IN (" . implode(', ', $ids) . ")
  ");
  // Doesn't work for some reason
  //return db_affected_rows($dbRes);
  return 0;
}

function removeCategoryFromFiles($categoryId, $fileIds) {
  return _removeCategoryFromObjects($categoryId, $fileIds, 'category_map');
}

function removeCategoryFromDisks($categoryId, $diskIds) {
  return _removeCategoryFromObjects($categoryId, $diskIds, 'category_map_disk');
}

?>
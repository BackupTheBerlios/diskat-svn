<?php

define('ARC_NONE', 0);
define('ARC_IS_ARCHIVE', 1);
define('ARC_IN_ARCHIVE', 2);

/*
 * @return DB result set
 */
function fetchFilesByCriteria($criteria, $more_tables = '', $sort = '')
{
  if ($more_tables && sizeof($more_tables) > 0) {
    $more_tables = ", " . implode(', ', $more_tables);
  } else {
    $more_tables = '';
  }

  if (!$sort) {
    $sort = "Tag, parent, Filename";
  } else {
    $sort = implode(', ', $sort);
  }

  return db_query("
  	SELECT  directory.id as FileId,
  		disk.id as DiskId,
  		tag as Tag, 
  		parent as Path, 
  		name as Filename, 
  		better_name as BetterName, 
  		size as Size, 
  		is_dir,
  		arc_status,
  		directory.description as Description, 
  		directory.notes AS Notes, 
  		label AS Label,
  		mdate AS MDate
  	FROM disk, directory $more_tables
  	WHERE $criteria
  	AND directory.snapshot=disk.id
  	ORDER BY $sort
  ");
}

function fetchFilesByCategoryCriteria($criteria)
{
  return db_query("
  	SELECT  directory.id as FileId,
  		tag as Tag, 
  		parent as Path, 
  		name as Filename, 
  		size as Size, 
  		is_dir,
  		arc_status,
  		directory.description as Description, 
  		directory.notes AS Notes, 
  		label AS Label
  	FROM disk, directory LEFT JOIN category_map ON obj_id=FileId
  	WHERE $criteria
  	AND directory.snapshot=disk.id
  	ORDER BY Tag, no
  ");
}

/*
 * @return DB result set
 */
function fetchFileById($id)
{
  $res = db_query("
  	SELECT  directory.id as FileId,
  		tag as Tag, 
  		parent as Path, 
  		name as Filename, 
  		better_name, 
  		size as Size, 
  		is_dir,
  		arc_status,
  		directory.description AS Description, 
  		directory.notes AS Notes, 
  		label AS Label
  	FROM directory, disk
  	WHERE directory.id=$id
  	AND directory.snapshot=disk.id
  	ORDER BY Tag, no
  ");
  return db_fetch_assoc($res);
}

/*
 * @return DB result set
 */
function fetchFilesByParentId($id)
{
  return db_query("
  	SELECT  directory.id as FileId,
  		name as Filename,
  		is_dir
  	FROM directory
  	WHERE directory.parent='$id'
  	ORDER BY Filename
  ");
}

/*
 * @return fileId of root directory
 */
function getRootOfDisk($diskId) {
  return db_select_single_value("
  	SELECT  directory.id as FileId
  	FROM disk, directory
  	WHERE 
  	disk.id='$diskId'
  	AND directory.parent=0
  	AND directory.snapshot=disk.id
  ");
}

function getFileIdsFromDbRes($dbRes)
{
  $ids = array();
  while ($row = db_fetch_assoc($dbRes)) {
    $ids[] = $row['FileId'];
  }
  db_rewind($dbRes);
  return $ids;
}

function updateFile($id, $data) {
  $sql = db_generate_update('directory', $id, $data);
  db_query($sql);
}

class DirectoryResolver{

  var $cache;

  function DirectoryResolver()
  {
    $this->cache = array();
  }

  function getFullPath($id) {
    $result = '';
    while ($id != 0) {
      $pathElement = $this->getPathElementById($id);
      $parent_id = $pathElement['parent'];
      $parent    = $pathElement['name'];
      $result = $parent . "/" . $result;
      $id = $parent_id;
    }
    // Strip extra '/''s 
    $result = substr($result, 1, strlen($result) - 2);
    return $result;
  }

  function getDirectoryPath($id) {
    $result = '';
    while ($id != 0) {
      $pathElement = $this->getPathElementById($id);
      $parent_id = $pathElement['parent'];
      if ($pathElement['arc_status'] != ARC_IN_ARCHIVE && $pathElement['is_dir']) {
        $parent    = $pathElement['name'];
        $result = $parent . "/" . $result;
      }
      $id = $parent_id;
    }
    // Strip extra '/''s 
    $result = substr($result, 1, strlen($result) - 2);
    return $result;
  }

  function getFilePath($id) {
    $result = '';
    while ($id != 0) {
      $pathElement = $this->getPathElementById($id);
      $parent_id = $pathElement['parent'];
      if ($pathElement['arc_status'] != ARC_IN_ARCHIVE) {
        $parent    = $pathElement['name'];
        $result = $parent . "/" . $result;
      }
      $id = $parent_id;
    }
    // Strip extra '/''s 
    $result = substr($result, 1, strlen($result) - 2);
    return $result;
  }

  /*
   * @return Tuple (parent_id, name)
   */
  function getPathElementById($id)
  {
    if (!isset($this->cache[$id])) {
      $dbRes = db_query("SELECT * FROM directory WHERE id=$id");
      $pathElement = db_fetch_assoc($dbRes);
      $this->cache[$id] = $pathElement;
      return $pathElement;
    } else {
      return $this->cache[$id];
    }
  }
}

?>
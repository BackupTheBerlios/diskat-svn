<?php

function fetchDisksByCriteria($criteria, $left_join = '')
{
  return db_query("
  	SELECT DISTINCT disk.id AS id, disk.tag AS tag, disk.label AS label, disk.title AS title, disk.last_update AS last_update
  	FROM disk $left_join
  	WHERE $criteria
  	ORDER BY tag
  ");
}

function fetchDiskById($id)
{
  $res = db_query("
  	SELECT * 
  	FROM disk 
  	WHERE id='$id'
  ");
  return db_fetch_assoc($res);
}

function updateDisk($id, $data) {
  $sql = db_generate_update('disk', $id, $data);
  db_query($sql);
}

function getDiskIdsFromDbRes($dbRes)
{
  $ids = array();
  while ($row = db_fetch_assoc($dbRes)) {
    $ids[] = $row['id'];
  }
  db_rewind($dbRes);
  return $ids;
}

?>
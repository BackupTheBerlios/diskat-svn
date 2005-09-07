<?php
require_once("config.inc");

$db_conn = 0;

function db_open()
{
  global $config_db_path;
  global $db_conn;
  $db_conn = sqlite_open($config_db_path);
}

function db_query($query) {
  global $db_conn;
//echo $db_conn, $query, "<br/>\n";
  return sqlite_query($db_conn, $query);
}

function db_rewind($res) {
  sqlite_rewind($res);
}

function db_fetch_assoc($res)
{
  return sqlite_fetch_array($res, SQLITE_BOTH); 
}

function db_num_rows($res) {
  return sqlite_num_rows($res);
}

function db_affected_rows($res) {
  return sqlite_changes($res);
}

function db_quote($str) {
  return sqlite_escape_string($str);
}

function db_select_single_value($sql) {
  $res = db_query($sql);
  $row = sqlite_fetch_array($res);
  return $row[0];
}

function db_generate_update($table, $id, $data) {
  $sql = "UPDATE $table SET";
  $first = 1;
  foreach ($data as $k=>$v) {
    if (!$first) $sql .= ', ';
    $sql .= " $k='". db_quote($v) . "'";
    $first = 0;
  }
  if (is_array($id)) {
    $sql .= " WHERE id IN ('" . implode("','", $id) . "')";
  } else {
    $sql .= " WHERE id=$id";
  }
  return $sql;
}

?>

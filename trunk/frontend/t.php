<?php
include_once('include/common.php');
include_once('include/db.php');
include_once('include/File.php');
header('Content-Type: text/xml');

db_open();
$res = fetchFilesByParentId($_REQUEST['id']);
echo '<?xml version="1.0" encoding="windows-1251"?>
';
echo "<directory>\n";
while ($row = db_fetch_assoc($res)) {
  echo '<file id="'.$row['FileId'].'" name="'.htmlspecialchars($row['Filename']).'" '
  	.'dir="'.$row['is_dir'].'" size="' . $row['size'] . '"/>' . "\n";
}
echo "</directory>\n";

?>

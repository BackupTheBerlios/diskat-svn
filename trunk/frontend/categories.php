<?php
include_once('include/db.php');
include_once('include/html_db.php');
include_once('include/Disk.php');
include_once('include/File.php');
include_once('include/Messages.php');
include_once('config.inc');

db_open();

if (isset($_REQUEST["bt_update"])) {
  if ($_REQUEST["add_name"] != "") {
    db_query("
      INSERT INTO category(type, name)
      VALUES ('".$_REQUEST["add_type"]."', '".$_REQUEST["add_name"]."')
    ");
    add_request_message("Category added");
  }
  if (isset($_REQUEST["ids"])) {
    db_query("
      DELETE FROM category
      WHERE id IN (" . implode(',', $_REQUEST["ids"]). ")
    ");
    add_request_message(sizeof($_REQUEST["ids"]) . " categori(es) deleted");
  }

  if (isset($_REQUEST["new_names"])) {
    $count = 0;
    foreach ($_REQUEST["new_names"] as $cat_id=>$new_name) {
      $new_name = trim($new_name);
      if ($new_name != '') {
        db_query("
          UPDATE category
          SET name='$new_name'
          WHERE id='$cat_id'
          AND type='".$_REQUEST["add_type"]."'
        ");
        $count++;
      }
    }
    if ($count > 0) {
      add_request_message("$count categori(es) renamed");
    }
  }
}

if (isset($_REQUEST['type'])) {
  $type = $_REQUEST['type'];
} else {
  $type = 1;
}

$categories = db_query("
	SELECT * 
	FROM category
	WHERE type=$type
	ORDER BY type, name
");

include('categories.php_html');

?>
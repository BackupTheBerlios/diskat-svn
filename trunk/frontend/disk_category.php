<?php
include_once('include/Category.php');
include_once('include/Messages.php');

if ($_REQUEST['cat_op'] == 'add') {
  $count = addCategoryToDisks($_REQUEST['category'], $ids);
  add_request_message("Applied category to $count disks");
} else if ($_REQUEST['cat_op'] == 'del') {
  $count = removeCategoryFromDisks($_REQUEST['category'], $ids);
  add_request_message("Removed category from disks");
}

echo render_messages();

echo returnButton(array('what', 'term', 'tag_pattern'));

?>
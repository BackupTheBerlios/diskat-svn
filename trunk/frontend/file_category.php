<?php
include_once('include/Category.php');
include_once('include/Messages.php');

if ($_REQUEST['cat_op'] == 'add') {
  $count = addCategoryToFiles($_REQUEST['category'], $ids);
  add_request_message("Applied category to $count files");
} else if ($_REQUEST['cat_op'] == 'del') {
  $count = removeCategoryFromFiles($_REQUEST['category'], $ids);
  add_request_message("Removed category from files");
}

echo render_messages();

?>
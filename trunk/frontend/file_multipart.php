<?php
include_once('include/common.php');
include_once('include/File.php');
include_once('include/Messages.php');
include_once('include/html.php');

db_open();

$ids = $_REQUEST['ids'];
$ids = array_diff($ids, array($_REQUEST['main_file']));

updateFile($ids, array('main_file' => $_REQUEST['main_file']));
add_request_message("Created multi-file entry");

echo render_messages();
echo returnToSearchResultsButton();

?>
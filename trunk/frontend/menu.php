<?php
include_once('include/common.php');

if (isset($_REQUEST['cd_drive'])) {
  $_SESSION['cd_drive'] = $_REQUEST['cd_drive'];
}

include('menu.php_html');
?>

<?php
include_once('config.inc');
header('Content-Type: text/html; charset='.$config_charset);

session_start();

if (!isset($_SESSION['cd_drive'])) {
  $_SESSION['cd_drive'] = 'd:';
}

function getmicrotime() { 
  list($usec, $sec) = explode(" ",microtime()); 
  return ((float)$usec + (float)$sec); 
} 

function convertSize($sz) {
  $sz = trim($sz);
  $l = strlen($sz);
  if (strtoupper($sz[$l - 1]) == 'M') {
     return substr($sz, 0, $l - 1) * 1024 * 1024;
  } else if (strtoupper($sz[$l - 1]) == 'K') {
     return substr($sz, 0, $l - 1) * 1024;
  }
  return $sz;
}

?>
<?php

$request_messages = array();

function add_request_message($msg) {
  global $request_messages;
  $request_messages[] = $msg;
}

function render_messages() {
  global $request_messages;
  $res = '';
  foreach($request_messages as $msg) {
    $res .= '<font color="red">'.$msg.'</font><br/>';
  }
  return $res;
}

?>
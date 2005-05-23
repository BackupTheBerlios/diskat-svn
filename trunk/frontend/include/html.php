<?php

/* Start rendering table of type $type:
   <empty>   - usual table
   "border0" - borderless
   "black"   - solid black-bordered, printing-friendly 
 */

function date_format($date) {
  return substr($date, 0, 4) . "-" . substr($date, 4, 2) . "-" . substr($date, 6, 2);
}

function _render_attrs($attrs) {
  if (!$attrs) {
    return '';
  }
  $res = '';
  foreach ($attrs as $a=>$v) {
    $res .= ' ' . $a . '="' . $v . '"';
  }
  return $res;
}

function html_start_row($attrs = 0) {
  $a = _render_attrs($attrs);
  print "<tr$a>";
}
function html_end_row() {
  print "</tr>\n";
}

function html_td($content, $attrs = '') {
  if (!$content) {
    $content = "&nbsp";
  } 
  $a = _render_attrs($attrs);
  print "<td$a>" . $content . "</td>";
}

function html_start_table($type = "")
{
  if (!$type)
  {
    echo '<table border="1" cellspacing="0" cellpadding="1">'."\n";
  }
  elseif ($type=="border0")
  {
    echo "<table border=0 cellspacing=0>\n";
  }
  else
  {
    echo("<table bgcolor=black border=0><tr><td>\n");
    echo("<table bgcolor=white cellpadding=2 cellspacing=1 border=0>\n");
  }
}

function html_end_table()
{
	echo '</table>'."\n";
}

function _html_render_row($headers, $celltag) 
{
        echo "<tr>\n";
	foreach ($headers as $h) {
		if ($h == '') {
			$h = '&nbsp;';
		}
		echo "  <$celltag>$h</$celltag>\n";
	}
        echo "</tr>\n";
}

function html_render_th_row($headers) 
{
        _html_render_row($headers, "th");
}

function html_render_table_row($headers) 
{
        _html_render_row($headers, "td");
}

function html_highlight_words($word_array, $text) {
	if (!$text) {
		return '&nbsp;';
	}
	if (!$word_array || sizeof($word_array) == 0) {
		return $text;
	}

	$re = implode($word_array,'|');
	if (!$re) {
		return $text;
	}
	return eregi_replace("($re)",'<span class="matchHilite">\1</span>',$text);
}

function html_select($name, $assoc) 
{
        $res = '<select name="' . $name . '">';
        foreach ($assoc as $k=>$v) {
        	$res .= '<option value="'.$k.'">' . $v . '</option>';
        }
        $res .= "</select>\n";
        print $res;
}

function saveOnRequest($params) {
        $res = '';
	foreach ($params as $p) {
		$res .= '<input type="hidden" name="' . $p . '" value="' . $_REQUEST[$p]. '">';
	}
	return $res;
}

function returnButton($params) {
	$res = '<form method="POST" action="' . $_REQUEST['returnTo'] . '">';
	$res .= saveOnRequest($params);
	$res .= '<input type="submit" value="Return">';
	$res .= '</form>';
	return $res;
}

function saveSearchParams($returnTo, $params) {
        $arr = array('returnTo' => $_SERVER['PHP_SELF']);
	foreach ($params as $p) {
		$arr[$p] = $_REQUEST[$p];
	}
	$_SESSION['savedSearch'] = $arr;
}

function returnToSearchResultsButton() {
	$res = '';
	$res = '<form method="POST" action="' . $_SESSION['savedSearch']['returnTo'] . '">';
	foreach ($_SESSION['savedSearch'] as $k=>$v) {
		$res .= '<input type="hidden" name="' . $k . '" value="' . $v. '">' . "\n";
	}
	$res .= '<input type="submit" value="Return to search results">';
	$res .= '</form>';
	return $res;
}

?>

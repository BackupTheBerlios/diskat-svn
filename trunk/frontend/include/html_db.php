<?php

require_once("include/db.php");
require_once("include/html.php");
require_once("include/misc.php");

function htmldb_set_hilight_words($word_array)
{
  global $_hilight_words;
  $_hilight_words = $word_array;
}

function _option_process($field_val, $row, $template)
{
  if ($template == 'hilight') {
    global $_hilight_words;
    return html_highlight_words($_hilight_words, $field_val);
  }

  $ret = str_replace("%id", $row['id'], $template);
  $ret = str_replace("%s", $field_val, $ret);
  return $ret;
}

function htmldb_render_table($result, $options = 0)
{
	$row = db_fetch_assoc($result);
	if (!$row) {
		echo "Table empty";
		return;
	}

	if (!$options) $options = array();
	if (isset($options['SHOW_COLS'])) {
		$show_cols = $options['SHOW_COLS'];
	} else if (isset($options['SKIP_COLS'])) {
		$skip_cols = $options['SKIP_COLS'];
	}

	html_start_table();
	$headers = array_keys($row);
	if (isset($options['ROW_NUM'])) {
		$headers = array_merge(array('#'), $headers);
	}
	html_render_th_row($headers);

	$row_no = 1;
	do {
	        $cells = array();

	        /* If so was requested, number the row */
		if (isset($options['ROW_NUM'])) {
			$cells[] = $row_no;
		}

	        foreach($row as $fld=>$val) {
		        if (isset($show_cols) && !isset($show_cols[$fld])) {
		        	continue;
		        } else if (isset($skip_cols) && isset($skip_cols[$fld])) {
		        	continue;
		        }
	        	if (isset($options[$fld])) $val = _option_process($val, $row, $options[$fld]);
	        	$cells[] = $val;
	        }

		html_render_table_row($cells);

		$row_no++;
	} while ($row = db_fetch_assoc($result));

	html_end_table();
}

function htmldb_select($name, $db_res, $addDefault = 0, $addNone = 0) {
        $res = '<select name="' . $name . '">';
        if ($addDefault) {
          $res .= '<option value="0">' . $addDefault . '</option>';
        }
        if ($addNone) {
          $res .= '<option value="-1">' . $addNone . '</option>';
        }
        while ($row = db_fetch_assoc($db_res)) {
        	$res .= '<option value="'.$row[0].'">' . $row[1] . '</option>';
        }
        $res .= "</select>\n";
        print $res;
}


?>
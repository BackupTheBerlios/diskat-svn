<? 
include_once('include/db.php');
include_once('include/File.php');
db_open();
$rootId = getRootOfDisk($_REQUEST['id']); 
?>
<html>
<head>
<script type="text/javascript" language="JavaScript" src="js/nanotree.js"></script>
<script type="text/javascript" language="JavaScript" src="js/xmlload.js"></script>
<script type="text/javascript" language="JavaScript">
showRootNode = false;
sortNodes = false;
dragable = false;

var closedGif = 'images/folder_closed.gif';
var openGif = 'images/folder_open.gif';
var pageIcon = 'images/page16x16.gif';
var userIcon = 'images/user_16x16.gif';
var helpIcon = 'images/help_16x16.gif';

/**
* Needed to initialize the tree.
* And to call showTree(imagePath); to actually show the tree.
* Alternatively this can be done in a script block at the bottom of the page.
* Though this method is somewhat cleaner.
*/
function init() {
	container = document.getElementById('examplediv');
	showTree('');
}
/**
* Called when a user clicks on a node.
* @param treeNode the TreeNode object which have been clicked.
*/
function standardClick(treeNode) {
	var mytext = document.getElementById('mytext');
	var param = treeNode.getParam();
	
	mytext.innerHTML = (param == '') ? treeNode.getName() : param;
}
function nodeEdited(treeNode) {

}
function nodeOpened(treeNodeId) {
	var treeNode = getTreeNode(treeNodeId);
	if (treeNode.loaded == 1) {
		return;
	}

//	alert("openhook:" + treeNodeId + " " + treeNode);
//	alert('http://localhost/diskat/t.php?id=' + treeNodeId);
        var xmlObj = loadXML('http://localhost/diskat/t.php?id=' + treeNodeId); 
        for (var i = 0; i < xmlObj.childNodes.length; i++) {
          var node = xmlObj.childNodes(i);
          icon = pageIcon;
          if (node.getAttribute("dir") == "1") {
            icon = new Array(closedGif,openGif);
          }
          var child = new TreeNode(node.getAttribute("id"), node.getAttribute("name"), icon);
          if (node.getAttribute("dir") == "1") {
            child.setHasChilds(true);
          }
          treeNode.addChild(child);
        }
        treeNode.setHasChilds(false);
        treeNode.loaded = 1;
        refreshNode(treeNode);
}
openHook = 'nodeOpened';


rootNode = new TreeNode(1,'/');
var node1 = new TreeNode(<?= $rootId ?>, '/',new Array(closedGif,openGif));
node1.setHasChilds(true);
rootNode.addChild(node1)


</script>
<style type="text/css">
#exampletable {
	width: 100%;
	height: 100%;
}
#examplediv {
	width: 100%;
	height: 100%;
	overflow: auto;
}
.explanation {
	font-weight: bold;
	font-style: italic;
}
</style>
</head>
<body OnLoad="init();">
<table id="exampletable">
	<tr>
		<td valign="top" style="width: 40%;">
			<div id="examplediv"></div>
		</td>
		<td valign="top">
			<a href="da_index.html">Danish version</a> - <a href="index.html">English version</a>
			<div style="background-color:#EEE;border-style:dashed;border-color:#000000;border-width:1px;padding:5px;">
				<div style="font-weight: bold;">NanoTree.</div>
				<div id="mytext">
				<p>NanoTree is a JavaScript tree, published under the <a href="http://www.gnu.org/copyleft/lesser.html">LGPL License</a>, which is developed to work in (at least) Internet Explorer and Mozilla<br>
				If other browsers will be added later, this will only be a plus.<br>
				The code is flexible, and it's easy to add to- and alter it. Also the code was made so it's easy to auto-generate with serversidescripts like PHP/JSP/ASP.</P>
				<p>Most things in the script can be used with events, without altering the original code.<br>
				(eg. You can tell the editor which function(s) should be called when someone expands a node, renames a node, etc.)</P>
				<p>If you choose to use NanoTree, The original author would be veryhappy to hear about it (Send an E-Mail to: <a href="mailto:martin@nano.dk">martin@nano.dk</a>)</p>
				<p style="font-weight:bold">Get it!</p>
					<ul>
						<li><a href="http://sourceforge.net/projects/nanotree/">Sourceforge project page</a></li>
					</ul>
				</p>
				<p style="font-weight:bold">Word explanation</p>
				<p>
					<span class="explanation">NanoTree: </span>Doesn't really mean anything. It's a combination of the words nano and tree.<br>
					<span class="explanation">Node: </span>A node is simply an item in the tree.<br>
					<span class="explanation">Event: </span>Whenever something happens, eg. a mouseclick on a Node<br>
				</p>
				<p>I hope the tree will be of use, it's been fun to develop, and I hope it evolves.</p>
				<p style="font-style:italic;">Martin Mouritzen</p>
				</div>
			</div>
			<br>
		</td>
	</tr>
</table>
</body></html>
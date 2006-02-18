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
          var child = new TreeNode(node.getAttribute("id"), node.getAttribute("name"), icon, node.getAttribute("size"));
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

var xmlDoc = new ActiveXObject("Microsoft.XMLDOM");
function loadXML(xmlFile)
{
   xmlDoc.async="false";
   xmlDoc.onreadystatechange = verify;
   xmlDoc.load(xmlFile);
   return xmlDoc.documentElement;
}

function verify() {
        // 0 Object is not initialized
        // 1 Loading object is loading data
        // 2 Loaded object has loaded data
        // 3 Data from object can be worked with
        // 4 Object completely initialized
        if (xmlDoc.readyState != 4)
        {
            return false;
        }
}

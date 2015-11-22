/**
 * Created by tanmoy on 16/10/15.
 */
function textToHtml(text) {

	var textlines = text.replace("&","&amp;").replace("\t","&nbsp;&nbsp;&nbsp;&nbsp;").replace("<","&lt;").replace(">","&gt;").split("\n");
	var i;
	var htmlfriend = "";
	for (i=0; i<textlines.length; ++i) {
		htmlfriend += ("<p>" + textlines[i] + "</p>").toString();
	}
 	return htmlfriend ;
}

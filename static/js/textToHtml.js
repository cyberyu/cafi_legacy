/**
 * Created by tanmoy on 16/10/15.
 */
function textToHtml(text) {
	var textlines = text.split("\n");
	var i;
	var htmlfriend = "";
	for (i=0; i<textlines.length; ++i) {
		htmlfriend += ("<p>" + textlines[i] + "</p>").toString();
	}
 	return htmlfriend ;
}

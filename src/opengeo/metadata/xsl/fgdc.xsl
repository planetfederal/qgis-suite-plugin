<?xml version="1.0"?>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" encoding="UTF-8" />

<!-- 

FGDC default stylesheet
Based on FGDC Plus.xsl (version 2.3, public domain) by Howie Sternberg
http://arcscripts.esri.com/details.asp?dbid=14674

/***************************************************************************
 Metadata browser/editor
                             
        begin                : 2011-02-21
        copyright            : (C) 2011 by BV
        email                : enickulin@bv.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 -->

<!--
FGDC Plus.xsl (version 2.3)

FGDC Plus.xsl is an XSL template that can be use with ArcGIS software
to display metadata. It shows metadata elements defined in the Content 
Standard for Digital Geospatial Metadata (CSDGM), aka FGDC Standard;
the ESRI Profile of the Content Standard for Digital Geospatial Metadata
(ESRI Profile); the Biological Data Profile of the Content Standard for 
Digital Geospatial Metadata (Biological Data Profile); and the Shoreline
Data Profile of the Content Standard for Digital Geospatial Metadata
(Shoreline Data Profile). The FGDC Plus Stylesheet includes the Dublin
Core Metadata Element Set. This stylsheet is in the public domain and
may be freely used, modified, and redistributed. It is provided "AS-IS"
without warranty or technical support.
-->
<xsl:template match="/">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
<xsl:call-template name="head_title"/>
<xsl:call-template name="head_dublin_core"/>
<style>
body								{font-family: Verdana,sans-serif; font-size: 9pt; color: #000000; background-color: #FBFBFB; cursor: default;}

#md-clickdef						{font-family: Arial,sans-serif; font-size: 9pt; color: #0000FF; cursor: pointer; text-align: center; padding: 0px; margin-left: 0px; margin-left: 0px; margin-top: 5px; margin-bottom: 10px;}
.md-link							{text-decoration: none;}
.md-over							{text-decoration: underline;}

#md-menu							{font-family: Arial,sans-serif; font-size: 9pt; text-align: center; text-align: center; padding: 0px; margin-left: 0px; margin-left: 0px; margin-top: 5px; margin-bottom: 0px;}
.md-menuitem						{color: #0000FF; padding-left: 6px; padding-right: 6px; padding-top: 2px; text-decoration: none; border-right: solid 1px #FBFBFB; border-top: solid 2px #FBFBFB; cursor: pointer; }
.md-menuitemover					{color: #0000FF; padding-left: 6px; padding-right: 6px; padding-top: 2px; text-decoration: underline; border-right: solid 1px #FBFBFB; border-top: solid 2px #FBFBFB; cursor: pointer; }
.md-menuitemactive					{background-color: #6495ED; color: #FFFFFF; padding-left: 6px; padding-right: 6px; padding-top: 2px; text-decoration: none; border-right: solid 1px #FBFBFB; border-top: solid 2px #DCDCDC; cursor: pointer; }

#md-description						{display: block;}
#md-graphic							{display: block;}
#md-spatial							{display: block;}
#md-structure						{display: block;}
#md-quality							{display: block;}
#md-source							{display: block;}
#md-distribution					{display: block;}
#md-metadata						{display: block;}
#md-thumbnail						{height: 144px; border: solid 1px #B0C4DE; float: left; margin-top: 5px; margin-left: 3px; margin-right: 10px;}

.md-title							{font-family: Arial,sans-serif; font-weight: bold; font-size: 15pt; color: #0000FF; text-align: center; padding: 0px; margin: 3px; cursor: pointer; text-decoration: none;}
.md-titleover						{font-family: Arial,sans-serif; font-weight: bold; font-size: 15pt; color: #0000FF; text-align: center; padding: 0px; margin: 3px; cursor: pointer; text-decoration: underline;}

.md-subtitle						{font-family: Arial,sans-serif; font-size: 10pt; text-align: center; padding: 0px; margin: 3px;}

.md-mastertitle 					{font-weight: bold; color: #FFFFFF; font-size: 11pt; text-align: center; padding: 0px; cursor: pointer; text-decoration: none;}
.md-mastertitleover 				{font-weight: bold; color: #FFFFFF; font-size: 11pt; text-align: center; padding: 0px; cursor: pointer; text-decoration: underline;}

.md-masterhide						{padding: 0px; margin: 0px; display:block;}

.md-detailtitle  					{font-weight: bold; color: #0000FF; padding: 0px; cursor: pointer; text-decoration: none;}
.md-detailtitleover 				{font-weight: bold; color: #0000FF; padding: 0px; cursor: pointer; text-decoration: underline;}

.md-detailhide						{background-color: #FFFFFF; padding: 10px; display:none;}
.md-detailshow						{background-color: #FFFFFF; padding: 10px; display:block;}
.md-detailhelp						{background-color: #FFFFFF; padding: 10px; display:none;}

.md-item  							{color: #0000FF; font-style: italic; font-weight: bold; padding: 1px; margin-left: 0px; margin-top: 5px; cursor: pointer; text-decoration: none;}
.md-itemover 						{color: #0000FF; font-style: italic; font-weight: bold; padding: 1px; margin-left: 0px; margin-top: 5px; cursor: pointer; text-decoration: underline;}

.md-itemlist  						{color: #0000FF; font-style: italic; font-weight: bold; padding: 1px; margin-left: 0px; margin-top: 5px; cursor: pointer; text-decoration: none;}
.md-itemlistover 					{color: #0000FF; font-style: italic; font-weight: bold; padding: 1px; margin-left: 0px; margin-top: 5px; cursor: pointer; text-decoration: underline;}

.md-itemhide						{padding: 5px; margin-left: 20px; display:none;}
.md-itemshow						{padding: 5px; margin-left: 20px; display:block;}

.md-color 							    {border: solid 2px #6495ED; padding: 0px; margin-left: 0px; margin-right: 0px; margin-top: 0px; margin-bottom: 10px;}
.md-color .md-master 				    {background-color: #6495ED; padding: 1px;}
.md-color .md-masterhide .md-separator	{background-color: #6495ED; padding: 4px;}
.md-color .md-masterhide .md-detail	    {background-color: #FFFFCC; border-top: solid 1px #6495ED; padding-left: 6px; padding-right: 4px; padding-top: 4px; padding-bottom: 4px;}

.md-def								{color: #DC143C; font-style: italic; padding-left: 2px; padding-right: 0px; padding-top: 0px; padding-bottom: 5px; display: none;}

.md-grid							{border-collapse: collapse; padding: 2px; margin: 1px;}

.md-grid th							{font-size: 9pt; border: solid 1px #6495ED; padding: 2px; vertical-align: top; font-style: italic; background-color: #F0F8FF;} 

.md-grid td							{font-size: 9pt; border: solid 1px #6495ED; padding: 2px; vertical-align: top;}

.md-grid td.md-italic				{font-family: Arial,sans-serif; font-size: 8pt; font-style: italic; border: solid 1px #6495ED; padding: 2px; vertical-align: top;}

.md-bgraphicimg						{background-color: #DCDCDC;}

.md-bgraphic						{color: #0000FF; cursor: pointer; text-decoration: none;}
.md-bgraphicover   					{color: #0000FF; cursor: pointer; text-decoration: underline;}

div b  								{font-weight:bold; font-style: italic;}

.md									{padding: 2px;}

.md-indent							{padding: 1px; margin-left: 20px;}

.md-block							{padding-left: 0px; padding-right: 0px; padding-top: 3px; padding-bottom: 3px;}
.md-indentblock						{padding-left: 0px; padding-right: 0px; padding-top: 3px; padding-bottom: 3px; margin-left: 20px;}
.md-indentblockstep					{padding-left: 0px; padding-right: 0px; padding-top: 0px; padding-bottom: 3px; margin-left: 20px;}

.md-footer							{font-family: Arial,sans-serif; font-size: 10pt; text-align: center;}

a:link								{color: #0000FF; text-decoration: none;}
a:active							{color: #0000FF; text-decoration: none;}
a:visited							{color: #0000FF; text-decoration: none;}
a:hover								{color: #0000FF; text-decoration: underline;}
</style>
<script type="text/javascript" language="JavaScript1.3"><![CDATA[
// Onload function assigns event handler functions to DIV elements according to className
window.onload = function() {
	var elem = document.getElementById("md-body");
	// Remove white space text nodes in Netscape 7 and Mozilla Firefox in order to 
	// use same set of javascript functions that work in IE to navigate through HTML.
	removewhitespace(elem);
	// Assign event handler functions to children of md-title element
	elem = document.getElementById("md-title");
	setuptitle(elem);
	// Assign event handler functions to md-clickdef element
	elem = document.getElementById("md-clickdef");
	setupclickdef(elem);
	// Assign event handler functions to children of md-menu element
	elem = document.getElementById("md-menu");
	setupmenu(elem);
	// Assign event handler functions md-mastertitle, md-detailtitle, md-item, md-itemlist, and md-bgraphic elements
	elem = document.getElementById("md-description");
	setupmaster(elem);
	elem = document.getElementById("md-graphic");
	setupmaster(elem);
	elem = document.getElementById("md-spatial");
	setupmaster(elem);
	elem = document.getElementById("md-structure");
	setupmaster(elem);
	elem = document.getElementById("md-quality");
	setupmaster(elem);
	elem = document.getElementById("md-source");
	setupmaster(elem);			
	elem = document.getElementById("md-distribution");
	setupmaster(elem);
	elem = document.getElementById("md-metadata");
	setupmaster(elem);
	elem = document.getElementById("tax");
	setuptaxonomy(elem);
	/* Parse Text - Find each <pre> element with an Id="fixvalue" and
	call fixvalue() function to parse text to respect line breaks,
	replace <pre> element with <div> elememt, and convert URL address
	strings in text to <a href> element. */
	elem = document.getElementById("fixvalue");
	while (Boolean(elem != null)) {
		fixvalue(elem);
		elem = document.getElementById("fixvalue");
	}
	window.focus()
}

// Remove white space text nodes in Netscape 7 and Mozilla Firefox in order to 
// use same set of javascript functions that work in IE to navigate through HTML. 
// Although not necessary, this function is called by onload function even for IE.
function removewhitespace(elem) {
	for (var i = 0; i < elem.childNodes.length; i++) {
		var c = elem.childNodes[i]
		if (c.nodeType == 1) {
			removewhitespace(c);
		}
		// Use regular expression to test for white space text nodes and remove
		if (((/^\s+$/.test(c.nodeValue))) && (c.nodeType == 3)) {
			elem.removeChild(elem.childNodes[i--]);
		}
	}
}

// Assign event handler functions to md-title element
function setuptitle(elem) {
	if (Boolean(elem != null)) {
		if (elem.className == "md-title") {
			elem.onclick = clicktitle;
			elem.onmouseover = overtitle;
			elem.onmouseout = overtitle;
		}
	}
}

// Assign event handler functions to md-clickdef element
function setupclickdef(elem) {
	if (Boolean(elem != null)) {
		if (elem.className == "md-link") {
			elem.onclick = clickdef;
			elem.onmouseover = overlink;
			elem.onmouseout = overlink;
		}
	}
}

// Assign event handler functions to md-menuitem elements
function setupmenu(elem) {
	if (Boolean(elem != null)) {
		for (var i = 0; i < elem.childNodes.length; i++) {
			c = elem.childNodes[i];			
			if (c.className == "md-menuitem") {
				c.onclick = clickmenuitem;
				c.onmouseover = overmenuitem;
				c.onmouseout = overmenuitem;
			}
			if (c.className == "md-menuitemactive") {
				c.onclick = clickmenuitem;
				c.onmouseover = overmenuitem;
				c.onmouseout = overmenuitem;
			}
		}
	}
}

// Assign event handler functions to md-mastertitle, md-detailtitle, md-item, md-itemlist, and md-bgraphic elements
function setupmaster(elem) {
	if (Boolean(elem != null)) {
			var c // child
			var gc 	// grandchild
			var ggc // great grandchild
			var gggc // great great grandchild
			var ggggc // great great great grandchild
			var gggggc // great great great great grandchild
		for (var i = 0; i < elem.childNodes.length; i++) {
			c = elem.childNodes[i];			
			for (var j = 0; j < c.childNodes.length; j++) {
				gc = c.childNodes[j];
				if (gc.className == "md-mastertitle") {
					gc.onclick = clickmaster;
					gc.onmouseover = overmaster;
					gc.onmouseout = overmaster;
					// begin name with + symbol to indicate clicking it can open/close content
					// gc.innerHTML = "+ " + gc.innerHTML;
				} 
				for (var k = 0; k < gc.childNodes.length; k++) {
					ggc = gc.childNodes[k];
					if (ggc.className == "md-detailtitle") {
						ggc.onclick = clickdetail;
						ggc.onmouseover = overdetail;
						ggc.onmouseout = overdetail;
					}
					if (ggc.className == "md-item") {
						ggc.onclick = clickitem;
						ggc.onmouseover = overitem;
						ggc.onmouseout = overitem;
					}
					if (ggc.className == "md-itemlist") {
						ggc.onclick = clickitemlist;
						ggc.onmouseover = overitemlist;
						ggc.onmouseout = overitemlist;
					}
					for (var l = 0; l < ggc.childNodes.length; l++) {
						gggc = ggc.childNodes[l];
						if (gggc.className == "md") {
							for (var m = 0; m < gggc.childNodes.length; m++) {
								ggggc = gggc.childNodes[m];						
								if (ggggc.className == "md-bgraphic") {
									ggggc.onclick = clickbgraphic;
									ggggc.onmouseover = overbgraphic;
									ggggc.onmouseout = overbgraphic;
								}
							}
						}
						if (gggc.className == "md-item") {
							gggc.onclick = clickitem;
							gggc.onmouseover = overitem;
							gggc.onmouseout = overitem;
						}
						if (gggc.className == "md-itemlist") {
							gggc.onclick = clickitemlist;
							gggc.onmouseover = overitemlist;
							gggc.onmouseout = overitemlist;
						}
						for (var n = 0; n < gggc.childNodes.length; n++) {
							ggggc = gggc.childNodes[n];
							if (ggggc.className == "md-item") {
								ggggc.onclick = clickitem;
								ggggc.onmouseover = overitem;
								ggggc.onmouseout = overitem;
							}
							if (ggggc.className == "md-itemlist") {
								ggggc.onclick = clickitemlist;
								ggggc.onmouseover = overitemlist;
								ggggc.onmouseout = overitemlist;
							}
							for (var o = 0; o < ggggc.childNodes.length; o++) {
								gggggc = ggggc.childNodes[o];
								if (gggggc.className == "md-item") {
									gggggc.onclick = clickitem;
									gggggc.onmouseover = overitem;
									gggggc.onmouseout = overitem;
								}
								if (gggggc.className == "md-itemlist") {
									gggggc.onclick = clickitemlist;
									gggggc.onmouseover = overitemlist;
									gggggc.onmouseout = overitemlist;
								}
							}					
						}
					}
				}
			}
		}
	}
}

// Assign event handler functions to taxonomy classification elements
function setuptaxonomy(elem) {
	while (Boolean(elem != null)) {
		elem.onclick = clickitem;
		elem.onmouseover = overitem;
		elem.onmouseout = overitem;
		elem.id="";
		elem = document.getElementById("tax");
	}
}
	
/* Fix value - Parse text in <pre> element to respect line breaks introduced in ArcCatalog
by the metadata author who intentionally introduced single line breaks to start new lines
or even more than one consecutive line break to further separate text to form paragraphs.
Note, fixvalue() calls the addtext() function, which adds text to DIV elements, which are
sequentially added to a parent DIV element to form separate lines and paragraphs of text. */

function fixvalue(elem) {
	elem.id = "";
	var n
	var val = String("");
	var pos = Number(0);
	// Make a newline character to use for basis for splitting string into 
	// an array of strings that are processed and turned into separate div
	// elements with either new line or paragraphic-like style.
	var newline = String.fromCharCode(10);
	var par = elem.parentNode;
	if (elem.innerText) {
		// Position of first newline character in IE
		n = elem;
		val = n.innerText;
		pos = val.indexOf(newline);
	} else {
		// Position of first newline character in NS, Firefox
		n = elem.childNodes[0];
		val = n.nodeValue;
		pos = val.indexOf(newline);
	}
	if (pos > 0) {
		// Text string contains at least one white space character
		var sValue = new String ("");
		// Split entire text string value on newline character
		// in order to create an array of string values to process	
		var aValues = val.split(newline);
		var padBottom = Number(0);
		var add = Boolean("false");
		// Loop thru each potential new line or paragraph and append <DIV>
		// element and set its className accordingly.				
		for (var i = 0; i <= aValues.length - 1; i++) {
			var div = document.createElement("DIV");
			sValue = aValues[i];
			add = false;
			for (var j = 0; j < sValue.length; j++) {
				if (sValue.charCodeAt(j) > 32) {
					add = true;
					// window.alert("CHARACTER AT " + sValue.charAt(j) + " CHARCODE " + sValue.charCodeAt(j))
					break;
				}
			}
			if (add) {
				if (i == 0) {
					// Must clone and append label property (e.g. <b>Abstract</b>) to first <DIV>
					// element, and then remove it from parent if at first element in aValues array.
					prev = elem.previousSibling;
					if (Boolean(prev != null)) {
						var label = prev.cloneNode(true)
						div.appendChild(label);
						par.removeChild(prev);
					}
				}
				// Now test to see whether to set style.paddingBottom to 0 or 4 for newline or 
				// paragraph, respectively.  Look ahead and if all characters in the next element 
				// in the aValues array (the next DIV element to make) are not white space then set
				// style.paddingBottom = 0. Otherwise, set style.paddingBottom = 4 to separate the 
				// the current <DIV> from the next <DIV> element. 			
				padBottom = Number(0);
				if (i < aValues.length - 1) {
					// Assume paragraph-like separation between DIV elements
					padBottom = Number(4);
					// Look for non-white space characters in content for next DIV
					var nextValue = aValues[i+1];
					for (var k = 0; k < nextValue.length; k++) {
						if (nextValue.charCodeAt(k) > 32) {
							// Found a non-white space character
							padBottom = Number(0);
							// window.alert("CHARACTER AT " + nextval.charAt(k) + " CHARCODE " + nextval.charCodeAt(k))
							break;
						}
					}
				}
				// Pad element
				div.style.paddingLeft = 0;
				div.style.paddingRight = 0;
				div.style.paddingTop = 0;
				div.style.paddingBottom = padBottom;
				// Scan text for URL strings before adding text to div element
				addtext(div,sValue);
				// Add new div element to parent div element
				par.appendChild(div);
			}
		}
		par.removeChild(elem);
	} else {
		// No white space charaters in text string so can be added directly to parent DIV element.
		par.removeChild(elem);
		// Scan text for URL strings before adding text to div element
		addtext(par,val);
	}		
}

/* Add text - This function adds text to (inside) DIV element, but before doing so 
searches for strings in the text that resemble URLs and converts them to hypertext
elements and adds them to the div element as well. Searches for strings that begin 
with "://" or "www." and converts them to <a href> elements. Add text function is 
called by fixvalue function */ 
 
function addtext(elem,txt) {
	// Scan entire text value and test for presense of URL strings, 
	// convert URL strings to Hypertext Elements, convert text strings
	// between URL strings to Text Nodes and append all Hypertext
	// Elements and Text Nodes to DIV element.
	var start = new Number (0);
	var end = new Number (0);
	var url = new String("");
	var urlpattern = /(\w+):\/\/([\w.]+)((\S)*)|www\.([\w.]+)((\S)*)/g;
	var punctuation = /[\.\,\;\:\?\!\[\]\(\)\{\}\'\"]/;
	var result
	var elemText
	while((result = urlpattern.exec(txt)) != null) {
		var fullurl = result[0];
		var protocol = result[1];
		url = fullurl;
		end = result.index;
		if (start < end){
			// Append Text Node to parent
			elemText = document.createTextNode(txt.substring(start, end));
			elem.appendChild(elemText);
		}
		var lastchar = fullurl.charAt(fullurl.length - 1);
		// Remove last character from url if character is punctuation mark, bracket or parenthesis;
		if (lastchar.match(punctuation) != null) {
			// Remove next-to-last character from url if character is punctuation mark, bracket or parenthesis. For example the ")" in "),"
			var nexttolastchar = fullurl.charAt(fullurl.length - 2);
			if (nexttolastchar.match(punctuation) != null) {
				url = fullurl.substring(0,fullurl.length - 2);		
			} else {		
				url = fullurl.substring(0,fullurl.length - 1);
			}		
		}
		start = (result.index + url.length)
		// Test to concatinate 'http://' to url if not already begininng with 'http://', 'https://' or 'ftp://'"
		if (protocol == "") {
			url = "http://" + url;
		}
		// Append Hypertext (anchor) Element to parent
		elemText = document.createTextNode(url);
		var elemAnchor = document.createElement("A");
		elemAnchor.setAttribute("href", url);
		elemAnchor.setAttribute("target", "viewer");
		elemAnchor.appendChild(elemText);
		elem.appendChild(elemAnchor);				
	}
	end = txt.length;
	if (start < end) {
		// Append Text Node that follows last Hypertext Element
		elemText = document.createTextNode(txt.substring(start, end));
		elem.appendChild(elemText);
	}
}

// "md-title" onmouseover and onmouseout function
function overtitle(evt)  {
	// Get reference to W3C or IE event object
	evt = (evt) ? evt : ((window.event) ? event : null);
	if (evt) {
		// Get reference to element from which event object was created. W3C calls this element target. IE calls it srcElement.
		var elem = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null);
		if (elem.nodeType == 3) {
			// If W3C and element is text node (nodeType = 3), then get reference to container (parent) to equalize with IE event model.
			elem = elem.parentNode;
		}
		if (elem) {
			// Work with element.
			if (elem.className == "md-title") {
				elem.className = "md-titleover";
			} else if (elem.className == "md-titleover") {
				elem.className = "md-title";
			}
		}
		// Prevent event from bubbling past this event handler.
		evt.cancelBubble = true;
	}
}

// "md-link" onmouseover and onmouseout function
function overlink(evt)  {
	// Get reference to W3C or IE event object
	evt = (evt) ? evt : ((window.event) ? event : null);
	if (evt) {
		// Get reference to element from which event object was created. W3C calls this element target. IE calls it srcElement.
		var elem = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null);
		if (elem.nodeType == 3) {
			// If W3C and element is text node (nodeType = 3), then get reference to container (parent) to equalize with IE event model.
			elem = elem.parentNode;
		}
		if (elem) {
			// Work with element.
			if (elem.className == "md-link") {
				elem.className = "md-over";
			} else if (elem.className == "md-over") {
				elem.className = "md-link";
			}
		}
		// Prevent event from bubbling past this event handler.
		evt.cancelBubble = true;
	}
}

// "md-menuitem" onmouseover and onmouseout function
function overmenuitem(evt)  {
	// Get reference to W3C or IE event object
	evt = (evt) ? evt : ((window.event) ? event : null);
	if (evt) {
		// Get reference to element from which event object was created. W3C calls this element target. IE calls it srcElement.
		var elem = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null);
		if (elem.nodeType == 3) {
			// If W3C and element is text node (nodeType = 3), then get reference to container (parent) to equalize with IE event model.
			elem = elem.parentNode;
		}
		if (elem) {
			// Work with element.
			if (elem.className == "md-menuitem") {
				elem.className = "md-menuitemover";
			} else if (elem.className == "md-menuitemover") {
				elem.className = "md-menuitem";
			}
		}
		// Prevent event from bubbling past this event handler.
		evt.cancelBubble = true;
	}
}

// "md-mastertitle" onmouseover and onmouseout function
function overmaster(evt)  {
	// Get reference to W3C or IE event object
	evt = (evt) ? evt : ((window.event) ? event : null);
	if (evt) {
		// Get reference to element from which event object was created. W3C calls this element target. IE calls it srcElement.
		var elem = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null);
		if (elem.nodeType == 3) {
			// If W3C and element is text node (nodeType = 3), then get reference to container (parent) to equalize with IE event model.
			elem = elem.parentNode;
		}
		if (elem) {
			// Work with element.
			if (elem.className == "md-mastertitle") {
				elem.className = "md-mastertitleover";
			} else if (elem.className == "md-mastertitleover") {
				elem.className = "md-mastertitle";
			}
		}
		// Prevent event from bubbling past this event handler.
		evt.cancelBubble = true;
	}
}

// "md-detailtitle" onmouseover and onmouseout function
function overdetail(evt)  {
	// Get reference to W3C or IE event object
	evt = (evt) ? evt : ((window.event) ? event : null);
	if (evt) {
		// Get reference to element from which event object was created. W3C calls this element target. IE calls it srcElement.
		var elem = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null);
		if (elem.nodeType == 3) {
			// If W3C and element is text node (nodeType = 3), then get reference to container (parent) to equalize with IE event model.
			elem = elem.parentNode;
		}
		if (elem) {
			// Work with element.
			if (elem.className == "md-detailtitle") {
				elem.className = "md-detailtitleover";
			} else if (elem.className == "md-detailtitleover") {
				elem.className = "md-detailtitle";
			}
		}
		// Prevent event from bubbling past this event handler.
		evt.cancelBubble = true;
	}
}

// "md-itemlist" onmouseover and onmouseout function
function overitemlist(evt)  {
	// Get reference to W3C or IE event object
	evt = (evt) ? evt : ((window.event) ? event : null);
	if (evt) {
		// Get reference to element from which event object was created. W3C calls this element target. IE calls it srcElement.
		var elem = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null);
		if (elem.nodeType == 3) {
			// If W3C and element is text node (nodeType = 3), then get reference to container (parent) to equalize with IE event model.
			elem = elem.parentNode;
		}
		if (elem) {
			// Work with element.
			if (elem.className == "md-itemlist") {
				elem.className = "md-itemlistover";
			} else if (elem.className == "md-itemlistover") {
				elem.className = "md-itemlist";
			}
		}
		// Prevent event from bubbling past this event handler.
		evt.cancelBubble = true;
	}
}

// "md-item" onmouseover and onmouseout function
function overitem(evt)  {
	// Get reference to W3C or IE event object
	evt = (evt) ? evt : ((window.event) ? event : null);
	if (evt) {
		// Get reference to element from which event object was created. W3C calls this element target. IE calls it srcElement.
		var elem = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null);
		if (elem.nodeType == 3) {
			// If W3C and element is text node (nodeType = 3), then get reference to container (parent) to equalize with IE event model.
			elem = elem.parentNode;
		}
		if (elem) {
			// Work with element.
			if (elem.className == "md-item") {
				elem.className = "md-itemover";
			} else if (elem.className == "md-itemover") {
				elem.className = "md-item";
			}
		}
		// Prevent event from bubbling past this event handler.
		evt.cancelBubble = true;
	}
}

// "md-bgraphic" onmouseover and onmouseout function
function overbgraphic(evt)  {
	// Get reference to W3C or IE event object
	evt = (evt) ? evt : ((window.event) ? event : null);
	if (evt) {
		// Get reference to element from which event object was created. W3C calls this element target. IE calls it srcElement.
		var elem = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null);
		if (elem.nodeType == 3) {
			// If W3C and element is text node (nodeType = 3), then get reference to container (parent) to equalize with IE event model.
			elem = elem.parentNode;
		}
		if (elem) {
			// Work with element.
			if (elem.className == "md-bgraphic") {
				elem.className = "md-bgraphicover";
			} else if (elem.className == "md-bgraphicover") {
				elem.className = "md-bgraphic";
			}
		}
		// Prevent event from bubbling past this event handler.
		evt.cancelBubble = true;
	}
}

// "md-menuitem" onclick function. Tabs to different metadata sections.
function clickmenuitem(evt)  {
	// Get reference to W3C or IE event object
	evt = (evt) ? evt : ((window.event) ? event : null);
	if (evt) {
		// Get reference to element from which event object was created. W3C calls this element target. IE calls it srcElement.
		var elem = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null);
		if (elem.nodeType == 3) {
			// If W3C and element is text node (nodeType = 3), then get reference to container (parent) to equalize with IE event model.
			elem = elem.parentNode;
		}
		if (elem) {
			// Work with element
			// Show other menu tabs
			var siblingNodes = elem.parentNode.childNodes
			for (var i = 0; i < siblingNodes.length; i++) {
				if (siblingNodes[i] != elem) {
					siblingNodes[i].className = "md-menuitem"
				} 
			}
			// Show active menu tab
			elem.className = "md-menuitemactive"				
			// Show active menu metadata.
			var elemMaster = document.getElementById("md-"+elem.id)
			elemMaster.style.display = "block";
			// Hide all other metadata sections
			var listMasterNodeIds = ["md-description","md-graphic","md-spatial","md-structure","md-quality","md-source","md-distribution","md-metadata"]; 
			for (var i = 0; i < listMasterNodeIds.length; i++) {
				if (listMasterNodeIds[i] != elemMaster.id) {
					otherNode = document.getElementById(listMasterNodeIds[i]);
					if (Boolean(otherNode != null)) {
						otherNode.style.display = "none";
					}
				}
			}
		}
		// Prevent event from bubbling past this event handler.
		evt.cancelBubble = true;
	}
}

// "md-clickdef" onclick function. Opens and closes metadata definitions, which "md-def" class div elements
function clickdef (evt) {
	evt = (evt) ? evt : ((window.event) ? event : null);
	if (evt) {
		// Get reference to element from which event object was created. W3C calls this element target. IE calls it srcElement.
		var elem = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null);
		if (elem.nodeType == 3) {
			// If W3C and element is text node (nodeType = 3), then get reference to container (parent) to equalize with IE event model.
			elem = elem.parentNode;
		}
		if (elem) {
			// Work with element.
			var e
			var aElem
			var text 
			var elemDefinition
			var styleDisplay
			elemDefinition = document.getElementById("md-clickdef");
			text = "Show Definitions";
			styleDisplay = "none";
			if (elemDefinition.innerHTML == "Show Definitions") {
				text = "Hide Definitions";
				styleDisplay = "block";
			}
			// hide or show metadata definition elements
			aElem = document.getElementsByName("md-def")
			for (var i = 0; i < aElem.length; i++) {
				e = aElem[i]				
				e.style.display = styleDisplay;
			}
			elem.innerHTML = text;
		}
	}
}

/* "md-title" onclick function. Always opens md-detailshow and either opens or closes md-detailhide,
and md-itemhide elements, depending on value of title elements toggledisplay value. Toggledisplay
value is either "block" to "none" and toggles everytime this function runs. */
function clicktitle(evt) {
	// Get reference to W3C or IE event object
	evt = (evt) ? evt : ((window.event) ? event : null);
	if (evt) {
		// Get reference to element from which event object was created. W3C calls this element target. IE calls it srcElement.
		var elem = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null);
		if (elem.nodeType == 3) {
			// If W3C and element is text node (nodeType = 3), then get reference to container (parent) to equalize with IE event model.
			elem = elem.parentNode;
		}
		if (elem) {
			// Work with element.
			var p = elem.parentNode; // parent
			var c 	// parent's child
			var gc 	// parent's grandchild
			var ggc // parent's great grandchild
			var gggc // parent's great great grandchild
			var ggggc // parent's great great great grandchild
			var gggggc // parent's great great great great grandchild
			var ggggggc // parent's great great great great great grandchild
			// Create toggledisplay attribute when title element is first clicked and set value to "block"
			// in order to open content.
			if (!elem.getAttributeNode("toggledisplay")) {
			 	elem.setAttribute("toggledisplay","block");
			}
			// Loop through child nodes, find those that open and close (md-detail and md-itemhide) 
			// and set their style.display to that of elem.getAttributeNode("toggledisplay").value
			for (var i = 0; i < p.childNodes.length; i++) {
				// Show (open) all metadata sections
				c = p.childNodes[i];
				c.style.display = "block";
				for (var j = 0; j < c.childNodes.length; j++) {
					gc = c.childNodes[j];
					for (var k = 0; k < gc.childNodes.length; k++) {
						ggc = gc.childNodes[k];						
						if (ggc.className == "md-mastertitle") {
							// add + or - to master title text
							if (elem.getAttributeNode("toggledisplay").value == "block") {
								ggc.innerHTML = "-" + ggc.innerHTML.substring(1,ggc.innerHTML.length);
							} else {
								ggc.innerHTML = "+" + ggc.innerHTML.substring(1,ggc.innerHTML.length);
							}
						}
						if (ggc.className == "md-detailhide") {
							// hide or show md-detailhide element
							ggc.style.display = elem.getAttributeNode("toggledisplay").value;
						} else if (ggc.className == "md-detailshow") {
							// make sure md-detailshow is always shown because user could have previously closed it
							ggc.style.display = "block"
						} else if (ggc.className == "md-detailhelp") {
							// make sure md-detailhelp is always not shown
							ggc.style.display = "none"
						}
						for (var l = 0; l < ggc.childNodes.length; l++) {
							gggc = ggc.childNodes[l];
							if (gggc.className == "md-itemhide") {
								// hide or show md-itemhide element
								gggc.style.display = elem.getAttributeNode("toggledisplay").value;
							} else if (gggc.className == "md-itemshow") {
								// show md-itemshow element
								gggc.style.display = "block"
							}					
							for (var m = 0; m < gggc.childNodes.length; m++) {
								ggggc = gggc.childNodes[m];
								if (ggggc.className == "md-itemhide") {
									// hide or show md-itemhide element
									ggggc.style.display = elem.getAttributeNode("toggledisplay").value;
								} else if (ggggc.className == "md-itemshow") {
									// show md-itemshow element
									ggggc.style.display = "block"
								}								
								for (var n = 0; n < ggggc.childNodes.length; n++) {
									gggggc = ggggc.childNodes[n];
									if (gggggc.className == "md-itemhide") {
										// hide or show md-itemhide element
										gggggc.style.display = elem.getAttributeNode("toggledisplay").value;
									} else if (gggggc.className == "md-itemshow") {
										// show md-itemshow element
										gggggc.style.display = "block"
									}			
									for (var o = 0; o < gggggc.childNodes.length; o++) {
										ggggggc = gggggc.childNodes[o];
										if (ggggggc.className == "md-itemhide") {
											// hide or show md-itemhide element
											ggggggc.style.display = elem.getAttributeNode("toggledisplay").value;
										} else if (ggggggc.className == "md-itemshow") {
											// show md-itemshow element
											ggggggc.style.display = "block"
										}			
									}												
								}													
							}							
						}				
					}
				}
			}
			if (elem.getAttributeNode("toggledisplay").value == "block") {
				elem.setAttribute("toggledisplay","none");
			} else {
				elem.setAttribute("toggledisplay","block");
			}
		}
		// Prevent event from bubbling past this event handler.
		evt.cancelBubble = true;
		// Show all menus tabs active, indicating to user that all metadata sections are open.		
		var elemMenu = document.getElementById("md-menu");
		var elemMenuItem		
		if (Boolean(elemMenu != null)) {
			for (var i = 0; i < elemMenu.childNodes.length; i++) {
				elemMenuItem = elemMenu.childNodes[i];			
				if (elemMenuItem.className == "md-menuitem") {
					elemMenuItem.className = "md-menuitemactive"
				}
			}
		}
	}
}

/* "md-mastertitle" onclick function. Always opens md-detailshow and either opens or closes md-detailhide,
and md-itemhide elements, depending on whether they are currently all opened or closed. */
function clickmaster(evt)  {
	// Get reference to W3C or IE event object
	evt = (evt) ? evt : ((window.event) ? event : null);
	if (evt) {
		// Get reference to element from which event object was created. W3C calls this element target. IE calls it srcElement.
		var elem = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null);
		if (elem.nodeType == 3) {
			// If W3C and element is text node (nodeType = 3), then get reference to container (parent) to equalize with IE event model.
			elem = elem.parentNode;
		}
		if (elem) {
			// Work with element.
			var p = elem.parentNode.nextSibling;
			var c 	// parent's child
			var gc 	// parent's grandchild
			var ggc // parent's great grandchild
			var gggc // parent's great great grandchild
			var ggggc // parent's great great great grandchild
			// Are all md-detail children (md-detailhide and md-detailshow) currently open or closed?
			var allClosed = Boolean("true");
			var allOpened = Boolean("true");
			allOpened = allchildrenopenedexcept(p,"md-detail")
			allClosed = allchildrenclosedexcept(p,"md-detail")
			allOpened = allchildrenopenedexcept(p,"md-detailhelp")
			allClosed = allchildrenclosedexcept(p,"md-detailhelp")
			// Are all grand children (md-itemhide) opened?
			if (allOpened) {
				allOpened = allgrandchildrenopened(p)
			}
			// window.alert(allOpened)
			// window.alert(allClosed)
			// Set new display variable. If one or more element but 
			// not all are open, open all elements. Otherwise, close
			// all elements if all of them are open. Also add + or -
			// to master title text.
			var newdisplay = "block";
			if ((allOpened) & (!allClosed)) {
				newdisplay = "none";
				elem.innerHTML = "+" + elem.innerHTML.substring(1,elem.innerHTML.length);
			} else {
				elem.innerHTML = "-" + elem.innerHTML.substring(1,elem.innerHTML.length);
			}
			// Loop through child nodes, find md-detailhide and md-itemhide elements
			// and set their style.display to value of newdisplay variable. The newdisplay
			// variable has a value of either "block" or "none". This value is based on the
			// current display condition of all md-detailhide and md-detailshow elements. If they
			// are currently all opened, then newdisplay is set to "none" so that they will all close.
			// If they are all closed, then the newdisplay value is "block" so that they all will
			// open. If some are opened and closed, the assumption is the user wants to open
			// all elements so the newdisplay value is "block". Once all opened, if user intended to
			// close them, they will close when the user natually clicks element again.			
			for (var i = 0; i < p.childNodes.length; i++) {
				c = p.childNodes[i];
				if (c.className == "md-detailhide") {
					// hide or show md-detailhide element
					c.style.display = newdisplay;
				} else if (c.className == "md-detailshow") {
					// make sure md-detailshow is always shown because user could have previously closed it
					c.style.display = "block";
				} else if (c.className == "md-detailhelp") {
					// make sure md-detailhelp is always not shown
					c.style.display = "none";
				}
				for (var j = 0; j < c.childNodes.length; j++) {
					gc = c.childNodes[j];
					if (gc.className == "md-itemhide") {
						// hide or show md-itemhide element
						gc.style.display = newdisplay;
					} else if (gc.className == "md-itemshow") {
						// show md-itemshow element
						gc.style.display = "block"	
					}				
					for (var k = 0; k < gc.childNodes.length; k++) {
						ggc = gc.childNodes[k];
			 			if (ggc.className == "md-itemhide") {
							// hide or show md-itemhide element
			 				ggc.style.display = newdisplay;
						} else if (ggc.className == "md-itemshow") {
							// show md-itemshow element
							ggc.style.display = "block"	
						}							
						for (var l = 0; l < ggc.childNodes.length; l++) {
							gggc = ggc.childNodes[l];
							if (gggc.className == "md-itemhide") {
								// hide or show md-itemhide element
								gggc.style.display = newdisplay;
							} else if (gggc.className == "md-itemshow") {
								// show md-itemshow element
								gggc.style.display = "block"	
							}				
							for (var m = 0; m < gggc.childNodes.length; m++) {
								ggggc = gggc.childNodes[m];
								if (ggggc.className == "md-itemhide") {
									// hide or show md-itemhide element
									ggggc.style.display = newdisplay;
								} else if (ggggc.className == "md-itemshow") {
									// show md-itemshow element
									ggggc.style.display = "block"	
								}				
							}												
						}													
					}							
				}				
			}
		}
		// Prevent event from bubbling past this event handler.
		evt.cancelBubble = true;
	}
}
			
// "md-detailtitle" onclick function. Opens and closes md-detailhide and md-detailshow elements.
function clickdetail(evt)  {
	// Get reference to W3C or IE event object
	evt = (evt) ? evt : ((window.event) ? event : null);
	if (evt) {
		// Get reference to element from which event object was created. W3C calls this element target. IE calls it srcElement.
		var elem = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null);
		if (elem.nodeType == 3) {
			// If W3C and element is text node (nodeType = 3), then get reference to container (parent) to equalize with IE event model.
			elem = elem.parentNode;
		}
		if (elem) {
			// Work with element.
			var p = elem.parentNode.nextSibling; // parent's next sibling element
			if (getcomputeddisplay(p) == "none") {
				p.style.display = "block";
			} else {
				p.style.display = "none";
			}
		}
		// Prevent event from bubbling past this event handler.
		evt.cancelBubble = true;
	}
}

// "md-detailitemlist" onclick function. Opens and closes all children and all grand children md-itemhide and md-itemshow elements.
function clickitemlist(evt)  {
	// Get reference to W3C or IE event object
	evt = (evt) ? evt : ((window.event) ? event : null);
	if (evt) {
		// Get reference to element from which event object was created. W3C calls this element target. IE calls it srcElement.
		var elem = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null);
		if (elem.nodeType == 3) {
			// If W3C and element is text node (nodeType = 3), then get reference to container (parent) to equalize with IE event model.
			elem = elem.parentNode;
		}
		if (elem) {
			// Work with element.
			var elemNext = elem.nextSibling; // next sibling element
			// Next sibling is normally md-itemshow class, but if md-itemhide
			// class then hide or show it.
			if (elemNext.className == "md-itemhide") {
				if (getcomputeddisplay(elemNext) == "none") {
					elemNext.style.display = "block";
				} else {
					elemNext.style.display = "none";
				}
			}
			// Are all grand children open or are all children closed?
			var allClosed = Boolean("true");
			var allOpened = Boolean("true");
			allOpened = allchildrenopenedexcept(elemNext,"md-item")
			allClosed = allchildrenclosedexcept(elemNext,"md-item")
			var newdisplay = "block";
			if ((allOpened) & (!allClosed)) {
				newdisplay = "none";
			}
			// if they're all opened, close them. Otherwise, open all of them.
			for (var i = 0; i < elemNext.childNodes.length; i++) {
				c = elemNext.childNodes[i];
				if (c.className == "md-itemhide") {
					// hide or show md-itemhide
					c.style.display = newdisplay;
				} else if (c.className == "md-itemshow") {
					// make sure md-itemshow is always shown
					c.style.display = "block";
				}
			}
		}
		// Prevent event from bubbling past this event handler.
		evt.cancelBubble = true;
	}
}

// "md-detailitem" onclick function. Opens and closes nextsibling md-itemhide or md-itemshow element.
function clickitem(evt)  {
	// Get reference to W3C or IE event object
	evt = (evt) ? evt : ((window.event) ? event : null);
	if (evt) {
		// Get reference to element from which event object was created. W3C calls this element target. IE calls it srcElement.
		var elem = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null);
		if (elem.nodeType == 3) {
			// If W3C and element is text node (nodeType = 3), then get reference to container (parent) to equalize with IE event model.
			elem = elem.parentNode;
		}
		if (elem) {
			// Work with element.
			var elemNext = elem.nextSibling; // next sibling element
			if ((elemNext.className == "md-itemhide") || ( elemNext.className == "md-itemshow")) {
				if (getcomputeddisplay(elemNext) == "none") {
					elemNext.style.display = "block";
				} else {
					elemNext.style.display = "none";
				}
			}
		}
		// Prevent event from bubbling past this event handler.
		evt.cancelBubble = true;
	}
}

// "md-bgraphic" onclick function. Opens and closes browsegraphic images (jpg, jpeg, gif, png, bmp).
function clickbgraphic(evt) {
	// Get reference to W3C or IE event object
	evt = (evt) ? evt : ((window.event) ? event : null);
	if (evt) {
		// Get reference to element from which event object was created. W3C calls this element target. IE calls it srcElement.
		var elem = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null);
		if (elem.nodeType == 3) {
			// If W3C and element is text node (nodeType = 3), then get reference to container (parent) to equalize with IE event model.
			elem = elem.parentNode;
		}
		if (elem) {
			// Work with element.
			var p = elem.parentNode.nextSibling;  // parent's next sibling element
			if (getcomputeddisplay(p) == "none") {
				var elemImage = p.childNodes[0];
				var srcImage = elem.getAttributeNode("browsen").value;
				p.style.display = "block";
				elemImage.setAttribute("src",srcImage);
				elemImage.setAttribute("alt","Image - " + srcImage);
			} else {
				p.style.display = "none";
			}
		}
	}
}

// Returns boolean indicating whether all child elements other than a particular class are opened
function allchildrenopenedexcept(elem,cname) {
	var opened = Boolean("true");
	for (var i = 0; i < elem.childNodes.length; i++) {
		c = elem.childNodes[i];
		if (c.className != cname) {
			if (getcomputeddisplay(c) == "none") {
				opened = false;
				break;
			}
		}
	}
	return opened;
}

// Returns boolean indicating whether all child elements other than a particular class are closed
function allchildrenclosedexcept(elem,cname) {
	var closed = Boolean("true");
	for (var i = 0; i < elem.childNodes.length; i++) {
		c = elem.childNodes[i];
		if (c.className != cname) {
			if (getcomputeddisplay(c) == "block") {
				closed = false;
				break;
			}
		}
	}
	return closed;
}

// Returns boolean indicating whether all grand child 
// and grand child's next sibling child elements are opened
function allgrandchildrenopened(elem) {
	var opened = Boolean("true");
	for (var i = 0; i < elem.childNodes.length; i++) {
		c = elem.childNodes[i];
		for (var j = 0; j < c.childNodes.length; j++) {
			gc = c.childNodes[j];
			if (gc.className == "md-itemhide") {
				if (getcomputeddisplay(gc) == "none") {
					opened = false;
					break;
				}
			} else if (gc.className == "md-itemlist") {
				gcns = gc.nextSibling
				for (var k = 0; k < gcns.childNodes.length; k++) {
					gcnsc = gcns.childNodes[k];
					if (gcnsc.className == "md-itemhide") {
						if (getcomputeddisplay(gcnsc) == "none") {
							opened = false;
							break;
						}
					}
				}
			}
		}
		if (!opened) {
			break;
		}
	}
	return opened;
}

// Returns element style.display property as a text string. Returns "none" or "block".
function getcomputeddisplay(elem) {
	var dis
	if (window.getComputedStyle) {
		// W3C		
		dis = window.getComputedStyle(elem, null).display;
	} else if (elem.currentStyle) {
		// IE
		dis = elem.currentStyle.display;
	}
	return dis;
}

]]></script>
</head>

<!--  CALL PRIMARY TEMPLATES -->

<body id="md-body">
<xsl:call-template name="header"/>
<xsl:call-template name="description"/>
<xsl:call-template name="graphic"/>
<xsl:call-template name="spatial"/>
<xsl:call-template name="structure"/>
<xsl:call-template name="quality"/>
<xsl:call-template name="source"/>
<xsl:call-template name="distribution"/>
<xsl:call-template name="metadata"/>
<xsl:call-template name="footer"/>
</body>
</html>

</xsl:template>

<!-- PRIMARY TEMPLATES -->

<!-- Head title -->
<xsl:template name="head_title">
	<xsl:choose>
		<xsl:when test="/metadata/idinfo/citation/citeinfo/title[normalize-space(.) != '']">
			<title><xsl:value-of select="/metadata/idinfo/citation/citeinfo/title[normalize-space(.)]"/></title>
		</xsl:when>
		<xsl:otherwise>
			<title>Metadata</title>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<!-- Dublin Core Metadata Element Set -->
<xsl:template name="head_dublin_core">
	<link rel="schema.dc" href="http://dublincore.org/documents/dces/"/>
	<!-- Title -->
	<xsl:for-each select="/metadata/idinfo/citation/citeinfo/title[normalize-space(.) != '']">
		<xsl:variable name="dc_title" select="normalize-space(.)"/>
		<meta name="dc.title" content='{$dc_title}'/>
	</xsl:for-each>
	<xsl:for-each select="/metadata/idinfo/citation/citeinfo/lworkcit/citeinfo/title[normalize-space(.) != '']">
		<xsl:variable name="dc_title" select="normalize-space(.)"/>
		<meta name="dc.title" content='{$dc_title}'/>
	</xsl:for-each>
	<!-- Creator -->
	<xsl:for-each select="/metadata/idinfo/citation/citeinfo/origin[normalize-space(.) != '']">
		<xsl:variable name="dc_creator" select="normalize-space(.)"/>
		<meta name="dc.creator" content='{$dc_creator}'/>
	</xsl:for-each>
	<xsl:for-each select="/metadata/idinfo/citation/citeinfo/lworkcit/citeinfo/origin[normalize-space(.) != '']">
		<xsl:variable name="dc_creator" select="normalize-space(.)"/>
		<meta name="dc.creator" content='{$dc_creator}'/>
	</xsl:for-each>
	<!-- Subject and Keywords -->
	<xsl:choose>
		<xsl:when test="/metadata/idinfo/keywords/theme/themekey[normalize-space(.) != '']">
			<xsl:variable name="dc_subject">
				<xsl:for-each select="/metadata/idinfo/keywords/theme/themekey[normalize-space(.) != '']">
					<xsl:choose>
						<xsl:when test="position() = 1">
							<xsl:value-of select="normalize-space(.)"/>
						</xsl:when>
						<xsl:otherwise>
							<xsl:text> </xsl:text><xsl:value-of select="normalize-space(.)"/>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:for-each>
			</xsl:variable>
			<meta name="dc.subject" content='{$dc_subject}'/>
		</xsl:when>
	</xsl:choose>
	<!-- Description -->
	<xsl:for-each select="/metadata/idinfo/descript/abstract[normalize-space(.) != '']">
		<xsl:variable name="dc_description" select="normalize-space(.)"/>
		<meta name="dc.description" content='{$dc_description}'/>
	</xsl:for-each>
	<!-- Publisher -->
	<xsl:for-each select="/metadata/idinfo/citation/citeinfo/pubinfo/publish[normalize-space(.) != '']">
		<xsl:variable name="dc_publisher" select="normalize-space(.)"/>
		<meta name="dc.publisher" content='{$dc_publisher}'/>
	</xsl:for-each>
	<!-- Contributor -->
	<xsl:for-each select="/metadata/idinfo/datacred[normalize-space(.) != '']">
		<xsl:variable name="dc_contributor" select="normalize-space(.)"/>
		<meta name="dc.contributor" content='{$dc_contributor}'/>
	</xsl:for-each>
	<!-- Date -->
	<xsl:for-each select="/metadata/idinfo/citation/citeinfo/pubdate[normalize-space(.) != '']">
		<xsl:variable name="dc_date" select="normalize-space(.)"/>
		<meta name="dc.date" content='{$dc_date}'/>
	</xsl:for-each>
	<!-- Resource Type -->
	<xsl:for-each select="/metadata/idinfo/citation/citeinfo/geoform[normalize-space(.) != '']">
		<xsl:variable name="dc_type" select="normalize-space(.)"/>
		<meta name="dc.type" content='data.{$dc_type}'/>
	</xsl:for-each>
	<!-- Format-->
	<xsl:for-each select="/metadata/idinfo/natvform[normalize-space(.) != '']">
		<xsl:variable name="dc_format" select="normalize-space(.)"/>
		<meta name="dc.format" content='{$dc_format}'/>
	</xsl:for-each>
	<!-- Identifier -->
	<xsl:for-each select="/metadata/idinfo/citation/citeinfo/onlink[normalize-space(.) != '']">
		<xsl:variable name="dc_identifier" select="normalize-space(.)"/>
		<meta name="dc.identifier" content='{$dc_identifier}'/>
	</xsl:for-each>
	<!-- Source -->
	<xsl:for-each select="/metadata/distinfo/resdesc[normalize-space(.) != '']">
		<xsl:variable name="dc_source" select="normalize-space(.)"/>
		<meta name="dc.source" content='{$dc_source}'/>
	</xsl:for-each>
	<!-- Language -->
	<xsl:for-each select="/metadata/idinfo/descript/langdata[normalize-space(.) != '']">
		<xsl:variable name="dc_lang" select="normalize-space(.)"/>
		<meta name="dc.lang" content='{$dc_lang}'/>
	</xsl:for-each>
	<!-- Coverage - geographic coordinates -->
	<xsl:for-each select="/metadata/idinfo/spdom/bounding[normalize-space(.) != '']">
		<xsl:variable name="dc_coverage_x_min" select="westbc[normalize-space(.) != '']"/>
		<meta name="dc.coverage.x.min" scheme="DD" content='{$dc_coverage_x_min}'/>
		<xsl:variable name="dc_coverage_x_max" select="eastbc[normalize-space(.) != '']"/>
		<meta name="dc.coverage.x.max" scheme="DD" content='{$dc_coverage_x_max}'/>
		<xsl:variable name="dc_coverage_y_min" select="southbc[normalize-space(.) != '']"/>
		<meta name="dc.coverage.y.min" scheme="DD" content='{$dc_coverage_y_min}'/>
		<xsl:variable name="dc_coverage_y_max" select="northbc[normalize-space(.) != '']"/>
		<meta name="dc.coverage.y.max" scheme="DD" content='{$dc_coverage_y_max}'/>
	</xsl:for-each>
	<!-- Coverage - place name -->
	<xsl:for-each select="/metadata/idinfo/keywords/place/placekey[normalize-space(.) != '']">
		<xsl:variable name="dc_coverage_placeName" select="normalize-space(.)"/>				
		<meta name="dc.coverage.placeName" content='{$dc_coverage_placeName}'/>
	</xsl:for-each>
	<!-- Coverage - time range -->
	<xsl:choose>
		<xsl:when test="/metadata/idinfo/timeperd/timeinfo/rngdates[normalize-space(.) != '']">
			<xsl:variable name="dc_coverage_t_min" select="/metadata/idinfo/timeperd/timeinfo/rngdates/begdate[normalize-space(.) != '']"/>				
			<meta name="dc.coverage.t.min" content='{$dc_coverage_t_min}'/>
			<xsl:variable name="dc_coverage_t_max" select="/metadata/idinfo/timeperd/timeinfo/rngdates/enddate[normalize-space(.) != '']"/>				
			<meta name="dc.coverage.t.max" content='{$dc_coverage_t_max}'/>
		</xsl:when>
	</xsl:choose>
	<!-- Rights -->
	<xsl:choose>
		<xsl:when test="/metadata/idinfo[accconst[normalize-space(.) != ''] or useconst[normalize-space(.) != '']]">
			<xsl:variable name="dc_rights">
				<xsl:for-each select="/metadata/idinfo/accconst[normalize-space(.) != '']">
					<xsl:text>Access constraints: </xsl:text><xsl:value-of select="normalize-space(.)"/><xsl:text>; </xsl:text>
				</xsl:for-each>
				<xsl:for-each select="/metadata/idinfo/useconst[normalize-space(.) != '']">
					<xsl:text> Use constraints: </xsl:text><xsl:value-of select="normalize-space(.)"/>
				</xsl:for-each>
			</xsl:variable>
			<meta name="dc.rights" content='{$dc_rights}'/>
		</xsl:when>
	</xsl:choose>
</xsl:template>

<!-- Header -->
<xsl:template name="header">
	<!-- Show Title -->
	<div id="md-title" class="md-title" title="Open/close all metadata tabs">
		<xsl:choose>
			<xsl:when test="/metadata/idinfo/citation/citeinfo/title[normalize-space(.) != '']">
				<xsl:value-of select="/metadata/idinfo/citation/citeinfo/title[normalize-space(.)]"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:text>Metadata</xsl:text>	
			</xsl:otherwise>
		</xsl:choose>
	</div>
	<!-- Show format type and file name -->
	<div class="md-subtitle">
	 	<!-- ESRI Profile element -->
		<xsl:for-each select="/metadata/idinfo/natvform[normalize-space(.) != '']">
			<xsl:value-of select="."/>
			<!-- ESRI Profile element -->
			<xsl:if test="/metadata/spdoinfo/rastinfo/rastifor[normalize-space(.) != '']">
				- <xsl:value-of select="/metadata/spdoinfo/rastinfo/rastifor" />
			</xsl:if>
			<!-- ESRI Profile element -->
			<xsl:if test="/metadata/idinfo/citation/citeinfo/ftname[normalize-space(.) != '']">
				- <xsl:value-of select="/metadata/idinfo/citation/citeinfo/ftname" />
			</xsl:if>			
		</xsl:for-each>		
	</div>
	<!-- Build subtitle -->
	<div class="md-subtitle">FGDC<xsl:text></xsl:text>
		<!-- Add ESRI to subtitle -->
		<xsl:if test="/metadata/Esri">
			<xsl:text>, ESRI</xsl:text>
		</xsl:if>
		<!-- Add Biological to subtitle -->	
		<xsl:if test="/metadata/idinfo/spdom/boundalt or /metadata/distinfo/digform/asciistr or /metadata/idinfo/taxonomy or /metadata/idinfo/tool or /metadata/dataqual/lineage/method or /metadata/idinfo/timeperd/timeinfo/sngdate/geolage or /metadata/idinfo/timeperd/timeinfo/rngdates/beggeol/geolage or /metadata/idinfo/timeperd/timeinfo/rngdates/endgeol/geolage">
			<xsl:text>, Biological</xsl:text>
		</xsl:if>	
		<xsl:if test="/metadata/dataqual/tidinfo or /metadata/dataqual/marweat or /metadata/dataqual/event">
			<xsl:text>, Shoreline</xsl:text>
		</xsl:if>			
		<xsl:text> </xsl:text>Metadata</div>
	<!-- Toggle definitions -->
	<div id="md-clickdef" class="md-link">Show Definitions</div>
	<!-- Menu links -->
	<div id="md-menu">
		<xsl:if test="/metadata/idinfo[normalize-space(.) != '']"> 
			<span id="description" class="md-menuitemactive">Description</span>
		</xsl:if>
		<xsl:if test="/metadata/idinfo/browse[normalize-space(.) != '']"> 
			 <span id="graphic" class="md-menuitemactive">Graphic</span>
		</xsl:if>
		<xsl:if test="/metadata/spref[horizsys or vertdef] or /metadata/idinfo/spdom">
			 <span id="spatial" class="md-menuitemactive">Spatial</span>
		</xsl:if>
		<xsl:if test="/metadata/eainfo[normalize-space(.) != ''] or /metadata/spdoinfo[normalize-space(.) != '']">
			 <span id="structure" class="md-menuitemactive">Data Structure</span>
		</xsl:if>
		<xsl:if test="/metadata/dataqual[logic or complete or cloud or attracc or posacc]">
			 <span id="quality" class="md-menuitemactive">Data Quality</span>
		</xsl:if>
		<xsl:if test="/metadata/dataqual/lineage[normalize-space(.) != ''] or /metadata/Esri/DataProperties/lineage/Process[normalize-space(.) != '']">
			 <span id="source" class="md-menuitemactive">Data Source</span>
		</xsl:if>
		<xsl:if test="/metadata/distinfo[normalize-space(.) != '']">
			 <span id="distribution" class="md-menuitemactive">Data Distribution</span>
		</xsl:if>
		<xsl:if test="/metadata/metainfo[normalize-space(.) != '']">
			 <span id="metadata" class="md-menuitemactive">Metadata</span>
		</xsl:if>
	</div>
</xsl:template>

<!-- Footer -->
<xsl:template name="footer">
	<div class="md-footer"><a target="viewer"><xsl:attribute name="href">http://www.fgdc.gov/</xsl:attribute>Federal Geographic Data Committee</a></div>
</xsl:template>

<!-- Thumbnail -->
<xsl:template match="/metadata/Binary/Thumbnail/img[(@src != '')]">
	<div style="text-align:center"><img id="md-thumbnail">
		<xsl:attribute name="SRC"><xsl:value-of select="@src"/></xsl:attribute>
	</img></div>
</xsl:template>

<!-- Description -->
<xsl:template name="description">
	<xsl:if test="/metadata/idinfo[normalize-space(.) != '']">
		<div id="md-description" class="md-color">
			<div class="md-master">
				<div class="md-mastertitle">+ Resource Description</div>
			</div>
			<div class="md-masterhide">
				<xsl:call-template name="identification_citation"/>
				<xsl:call-template name="identification_description"/>
				<xsl:call-template name="identification_point_of_contact"/>
				<xsl:call-template name="identification_data_type"/>
				<xsl:call-template name="identification_time_period"/>
				<xsl:call-template name="identification_status"/>
				<xsl:call-template name="identification_key_words"/>
			</div>
		</div>
	</xsl:if>
</xsl:template>

<!-- Graphic Example -->
<xsl:template name="graphic">
	<xsl:if test="/metadata/idinfo/browse[normalize-space(.) != '']"> 
		<div id="md-graphic" class="md-color">
			<div class="md-master">
				<div class="md-mastertitle">+ Graphic Example</div>
			</div>
			<div class="md-masterhide">
				<xsl:call-template name="browse_graphic"/>
			</div>
		</div>
	</xsl:if>
</xsl:template>

<!-- Spatial Reference Information -->
<xsl:template name="spatial">
	<xsl:if test="/metadata/spref[horizsys or vertdef] or /metadata/idinfo/spdom">
		<div id="md-spatial" class="md-color">
			<div class="md-master">
				<div class="md-mastertitle">+ Spatial Reference Information</div>
			</div>
			<div class="md-masterhide">
				<xsl:call-template name="horizontal_coordinate_system"/>
				<xsl:call-template name="vertical_coordinate_system"/>
				<xsl:call-template name="identification_spatial_domain"/>
			</div>
		</div>
	</xsl:if>
</xsl:template>

<!-- Data Structure and Attribute Information -->
<xsl:template name="structure">
	<xsl:if test="/metadata/eainfo[normalize-space(.) != ''] or /metadata/spdoinfo[normalize-space(.) != '']">
		<div id="md-structure" class="md-color">
			<div class="md-master">
				<div class="md-mastertitle">+ Data Structure and Attribute Information</div>
			</div>
			<div class="md-masterhide">
				<xsl:call-template name="attributes_data_organization_overview"/>
				<xsl:call-template name="attributes_entity"/>
				<xsl:call-template name="attributes_esri_subtype"/>
				<xsl:call-template name="attributes_esri_relationship"/>
				<xsl:call-template name="data_organization_sdts_feature"/>
				<xsl:call-template name="data_organization_vpf_feature"/>
				<xsl:call-template name="data_organization_raster"/>
			</div>
		</div>
	</xsl:if>	
</xsl:template>

<!-- Data Quality and Accuracy Information -->
<xsl:template name="quality">
	<xsl:if test="/metadata/dataqual[logic or complete or cloud or attracc or posacc]">
		<div id="md-quality" class="md-color">
			<div class="md-master">
				<div class="md-mastertitle">+ Data Quality and Accuracy Information</div>
			</div>
			<div class="md-masterhide">
				<xsl:call-template name="data_quality_general"/>
				<xsl:call-template name="data_quality_attribute_accuracy"/>
				<xsl:call-template name="data_quality_positional_accuracy"/>
			</div>
		</div>
	</xsl:if>	
</xsl:template>

<!-- Data Source and Process Information -->
<xsl:template name="source">
	<xsl:if test="/metadata/dataqual/lineage[normalize-space(.) != ''] or /metadata/Esri/DataProperties/lineage/Process[normalize-space(.) != '']">
		<div id="md-source" class="md-color">
			<div class="md-master">
				<div class="md-mastertitle">+ Data Source and Process Information</div>
			</div>
			<div class="md-masterhide">
				<xsl:call-template name="data_quality_data_sources"/>
				<xsl:call-template name="data_quality_process_steps"/>
				<xsl:call-template name="data_quality_esri_geoprocessing"/>
			</div>
		</div>
	</xsl:if>
</xsl:template>

<!-- Data Distribution Information -->
<xsl:template name="distribution">
	<xsl:if test="/metadata/distinfo[normalize-space(.) != '']">
		<div id="md-distribution" class="md-color">
			<div class="md-master">
				<div class="md-mastertitle">+ Data Distribution Information</div>
			</div>
			<div class="md-masterhide">
				<xsl:for-each select="/metadata/distinfo[normalize-space(.) != '']">
					<xsl:choose>
						<xsl:when test="position() > 1">
							<div class="md-separator"></div>
						</xsl:when>
					</xsl:choose>
					<xsl:call-template name="distribution_general"/>
					<xsl:call-template name="distribution_contact"/>
					<xsl:call-template name="distribution_standard_order"/>
					<xsl:call-template name="distribution_custom_order"/>
					<xsl:call-template name="distribution_time_period"/>
				</xsl:for-each>
			</div>
		</div>
	</xsl:if>
</xsl:template>

<!-- Metadata Reference -->
<xsl:template name="metadata">
	<xsl:if test="/metadata/metainfo[normalize-space(.) != '']">
		<div id="md-metadata" class="md-color">
			<div class="md-master">
				<div class="md-mastertitle">+ Metadata Reference</div>
			</div>
			<div class="md-masterhide">
				<xsl:call-template name="metadata_date"/>
				<xsl:call-template name="metadata_contact"/>
				<xsl:call-template name="metadata_access"/>
				<xsl:call-template name="metadata_security"/>
				<xsl:call-template name="metadata_standard"/>
				<xsl:call-template name="metadata_fgdc_plus_stylesheet"/>
			</div>
		</div>
	</xsl:if>
</xsl:template>

<!-- SECONDARY TEMPLATES -->

<!-- IDENTIFICATION Metadata elements -->

<!-- Citation -->
<xsl:template name="identification_citation">
	<xsl:for-each select="/metadata/idinfo/citation/citeinfo[normalize-space(.) != '']">
		<div class="md-detail">
			<div class="md-detailtitle">Citation</div>
		</div>
		<div class="md-detailshow">
			<div id="md-def" name="md-def" class="md-def">Information used to reference the data.</div>
			<!-- Show Thumbnail image created in ArcCatalog -->
			<xsl:apply-templates select="/metadata//img[(@src != '')]" />
			<!-- Citation information -->
			<xsl:call-template name="citation_info"/>
		</div>
	</xsl:for-each>	
</xsl:template>

<!-- Description -->
<xsl:template name="identification_description">
	<xsl:if test="/metadata/idinfo[descript[abstract[normalize-space(.) != ''] or purpose[normalize-space(.) != ''] or supplinf[normalize-space(.) != ''] or langdata[normalize-space(.) != '']]]  or /metadata/idinfo/datacred[normalize-space(.) != '']">
		<xsl:for-each select="/metadata/idinfo[normalize-space(.) != '']">		
		<div class="md-detail">
			<div class="md-detailtitle">Description</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">A characterization of the data, including its intended use and limitations.</div>
			<xsl:for-each select="descript/abstract[normalize-space(.) != '']">
				<div class="md"><b>Abstract: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
			</xsl:for-each>
			<xsl:for-each select="descript/purpose[normalize-space(.) != '']">
				<div class="md"><b>Purpose: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
			</xsl:for-each>
			<xsl:for-each select="descript/supplinf[normalize-space(.) != '']">
				<div class="md"><b>Supplemental information: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
			</xsl:for-each>
			<xsl:for-each select="datacred[normalize-space(.) != '']">
				<div class="md"><b>Dataset credit: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
			</xsl:for-each>				
			<!-- ESRI Profile element -->
			<xsl:for-each select="descript/langdata[normalize-space(.) != '']">
				<div class="md"><b>Language of dataset: </b><xsl:value-of select="."/></div>
			</xsl:for-each>
		</div>
		</xsl:for-each>
	</xsl:if>
</xsl:template>

<!-- Point Of Contact -->
<xsl:template name="identification_point_of_contact">
	<xsl:for-each select="/metadata/idinfo/ptcontac/cntinfo[(cntperp/*[normalize-space(.) != '']) or (cntorgp/*[normalize-space(.) != '']) or (cntaddr/address[normalize-space(.) != '']) or (cntaddr/city[normalize-space(.) != '']) or (cntaddr/state[normalize-space(.) != '']) or (cntaddr/postal[normalize-space(.) != '']) or (cntaddr/country[normalize-space(.) != '']) or (cntvoice[normalize-space(.) != '']) or (cntfax[normalize-space(.) != '']) or (cntemail[normalize-space(.) != '']) or (hours[normalize-space(.) != '']) or (cntinst[normalize-space(.) != ''])]"> 
		<div class="md-detail">
			<div class="md-detailtitle">Point Of Contact</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">Contact information for the individual or organization that is knowledgeable about the data.</div>
			<xsl:call-template name="contact_info"/>
		</div>
	</xsl:for-each>
</xsl:template>	

<!-- Data Type -->
<xsl:template name="identification_data_type">
	<xsl:if test="/metadata/idinfo/citation/citeinfo[ftname[normalize-space(.) != ''] or geoform[normalize-space(.) != '']] or /metadata/idinfo[natvform[normalize-space(.) != ''] or native[normalize-space(.) != '']]">
		<xsl:for-each select="/metadata/idinfo[normalize-space(.) != '']">
			<div class="md-detail">
				<div class="md-detailtitle">Data Type</div>
			</div>
			<div class="md-detailhide">
				<div id="md-def" name="md-def" class="md-def">How the data are represented, formatted and maintained by the data producing organization.</div>
				<xsl:for-each select="citation/citeinfo[normalize-space(.) != '']">
				 	<!-- ESRI Profile element -->
					<xsl:for-each select="ftname[normalize-space(.) != '']">
						<div class="md"><b>File or table name: </b><xsl:value-of select="."/></div>
					</xsl:for-each>
					<xsl:for-each select="geoform[normalize-space(.) != '']">	
						<div class="md"><b>Data type: </b><xsl:value-of select="."/></div>
					</xsl:for-each>
				</xsl:for-each>
				<!-- ESRI Profile element -->
				<xsl:for-each select="natvform[normalize-space(.) != '']">
					<div class="md"><b>Data format: </b><xsl:value-of select="."/></div>
				</xsl:for-each>		
				<xsl:for-each select="native[normalize-space(.) != '']">
					<div class="md"><b>Native dataset environment: </b><xsl:value-of select="."/></div>
				</xsl:for-each>
			</div>
		</xsl:for-each>
	</xsl:if>
</xsl:template>

<!-- Data Constraints and Credit -->
<xsl:template name="identification_access">
	<xsl:for-each select="/metadata/idinfo[accconst[normalize-space(.) != ''] or useconst[normalize-space(.) != '']]">
		<div class="md-detail">
			<div class="md-detailtitle">Data Access Constraints</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">Restrictions and legal prerequisites for accessing or using the data after access is granted.</div>
			<xsl:for-each select="accconst[normalize-space(.) != '']">
				<div class="md"><b>Access constraints: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
			</xsl:for-each>
			<xsl:for-each select="useconst[normalize-space(.) != '']">
				<div class="md"><b>Use constraints: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
			</xsl:for-each>
		</div>
	</xsl:for-each>
</xsl:template>

<!-- Time Period of Data -->
<xsl:template name="identification_time_period">
	<xsl:for-each select="/metadata/idinfo/timeperd[(.//caldate[normalize-space(.) != ''] != '') or (timeinfo/rngdates/*[normalize-space(.) != '']) or (current[normalize-space(.) != ''])]">
		<div class="md-detail">
			<div class="md-detailtitle">Time Period of Data</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">Time period(s) for which the data corresponds to the currentness reference.</div>
			<xsl:call-template name="time_info"/>
		</div>
	</xsl:for-each>
</xsl:template>	

<!-- Status -->
<xsl:template name="identification_status">
	<xsl:for-each select="/metadata/idinfo/status[progress[normalize-space(.) != ''] or update[normalize-space(.) != '']]">
		<div class="md-detail">
			<div class="md-detailtitle">Status</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">The state of and maintenance information for the data.</div>
			<xsl:for-each select="progress[normalize-space(.) != '']">
				<div class="md"><b>Data status: </b><xsl:value-of select="."/></div>
			</xsl:for-each>
			<xsl:for-each select="update[normalize-space(.) != '']">
				<div class="md"><b>Update frequency: </b><xsl:value-of select="."/></div>
			</xsl:for-each>				
		</div>
	</xsl:for-each>
</xsl:template>	

<!-- Key Words -->
<xsl:template name="identification_key_words">
	<xsl:for-each select="/metadata/idinfo/keywords[theme[normalize-space(.) != ''] or place[normalize-space(.) != ''] or stratum[normalize-space(.) != ''] or temporal[normalize-space(.) != '']]">
		<div class="md-detail">
			<div class="md-detailtitle">Key Words</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">Words or phrases that summarize certain aspects of the data.</div>
			<xsl:for-each select="theme[normalize-space(.) != '']">
				<div class="md"><b>Theme:</b></div>
				<div class="md-indent">
					<xsl:if test="themekey[normalize-space(.) != '']">
						<div class="md"><b>Keywords: </b>  
							<xsl:for-each select="themekey[normalize-space(.) != '']">	
								<xsl:value-of select="."/>
								<xsl:if test="position() != last()"><xsl:text>, </xsl:text></xsl:if>
							</xsl:for-each>
						</div>
					</xsl:if>
					<xsl:for-each select="themekt[normalize-space(.) != '']">
						<div class="md"><b>Keyword thesaurus: </b><xsl:value-of select="."/></div>
					</xsl:for-each>			
				</div>			
			</xsl:for-each>
			<xsl:for-each select="place[normalize-space(.) != '']">
				<div class="md"><b>Place:</b></div>
				<div class="md-indent">
					<xsl:if test="placekey[normalize-space(.) != '']">
						<div class="md"><b>Keywords: </b>  
							<xsl:for-each select="placekey[normalize-space(.) != '']">	
								<xsl:value-of select="."/>
								<xsl:if test="position() != last()"><xsl:text>, </xsl:text></xsl:if>
							</xsl:for-each>
						</div>
					</xsl:if>
					<xsl:for-each select="placekt[normalize-space(.) != '']">
						<div class="md"><b>Keyword thesaurus: </b><xsl:value-of select="."/></div>
					</xsl:for-each>			
				</div>			
			</xsl:for-each>
			<xsl:for-each select="stratum[normalize-space(.) != '']">
				<div class="md"><b>Stratum:</b></div>
				<div class="md-indent">
					<xsl:if test="stratkey[normalize-space(.) != '']">
						<div class="md"><b>Keywords: </b>  
							<xsl:for-each select="stratkey[normalize-space(.) != '']">	
								<xsl:value-of select="."/>
								<xsl:if test="position() != last()"><xsl:text>, </xsl:text></xsl:if>
							</xsl:for-each>
						</div>
					</xsl:if>
					<xsl:for-each select="stratkt[normalize-space(.) != '']">
						<div class="md"><b>Keyword thesaurus: </b><xsl:value-of select="."/></div>
					</xsl:for-each>			
				</div>			
			</xsl:for-each>
			<xsl:for-each select="temporal[normalize-space(.) != '']">
				<div class="md"><b>Temporal:</b></div>
				<div class="md-indent">
					<xsl:if test="tempkey[normalize-space(.) != '']">
						<div class="md"><b>Keywords: </b>  
							<xsl:for-each select="tempkey[normalize-space(.) != '']">	
								<xsl:value-of select="."/>
								<xsl:if test="position() != last()"><xsl:text>, </xsl:text></xsl:if>
							</xsl:for-each>
						</div>
					</xsl:if>
					<xsl:for-each select="tempkt[normalize-space(.) != '']">
						<div class="md"><b>Keyword thesaurus: </b><xsl:value-of select="."/></div>
					</xsl:for-each>			
				</div>			
			</xsl:for-each>
		</div>
	</xsl:for-each>
</xsl:template>		

<!-- Spatial Domain -->
<xsl:template name="identification_spatial_domain">
	<xsl:for-each select="/metadata/idinfo/spdom[normalize-space(.) != '']">
		<div class="md-detail">
			<div class="md-detailtitle">Spatial Domain</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">The geographic areal domain of the data that describes the western, eastern, northern, and southern geographic limits of data coverage.</div>
			<div class="md-itemlist">Bounding Coordinates</div>
			<div class="md-itemshow">

				<xsl:for-each select="bounding[normalize-space(.) != '']">	
					<div class="md-item">In Unprojected coordinates (geographic)</div>
					<div class="md-itemhide">
						<!-- ESRI Profile element -->	
						<xsl:for-each select="/metadata/spref/horizsys/cordsysn/geogcsn[normalize-space(.) != '']">
							<div class="md"><xsl:value-of select="translate(.,'_',' ')"/></div>
						</xsl:for-each>				
						<table class="md-grid">
							<tr><th>Boundary</th><th>Coordinate</th></tr>
							<xsl:for-each select="westbc[normalize-space(.) != '']">
								<tr><td>West</td><td><xsl:value-of select="."/> (longitude)</td></tr>
							</xsl:for-each>
							<xsl:for-each select="eastbc[normalize-space(.) != '']">
								<tr><td>East</td><td><xsl:value-of select="."/> (longitude)</td></tr>
							</xsl:for-each>
							<xsl:for-each select="northbc[normalize-space(.) != '']">
								<tr><td>North</td><td><xsl:value-of select="."/> (latitude)</td></tr>
							</xsl:for-each>
							<xsl:for-each select="southbc[normalize-space(.) != '']">
								<tr><td>South</td><td><xsl:value-of select="."/> (latitude)</td></tr>
							</xsl:for-each>							
						</table>
					</div>
				</xsl:for-each>				
			</div>
			<xsl:if test="dsgpoly[normalize-space(.) != '']">
				<div class="md-item">Data set Geographic Polygon</div>
				<div class="md-itemhide">			
					<xsl:for-each select="dsgpoly[dsgpolyo[normalize-space(.) != ''] or dsgpolyx[normalize-space(.) != '']]">
						<div class="md-itemlist">Data set G-Polygon <xsl:value-of select="position()"/>:</div>
						<div class="md-itemshow">
							<xsl:for-each select="dsgpolyo[normalize-space(.) != '']">
								<div class="md-item">Outer G-Ring point coordinates</div>
								<div class="md-itemhide">
									<xsl:call-template name="identification_data_set_g_polygon_point_info"/>
									<xsl:for-each select="gring[normalize-space(.) != '']">
										<div class="md"><b>G-Ring: </b><xsl:value-of select="."/></div>
									</xsl:for-each>
								</div>
							</xsl:for-each>
							<xsl:for-each select="dsgpolyx[normalize-space(.) != '']">
								<div class="md-item">Exclusion G-Ring point coordinates</div>
								<div class="md-itemhide">
									<xsl:call-template name="identification_data_set_g_polygon_point_info"/>
									<xsl:for-each select="gring[normalize-space(.) != '']">
										<div class="md"><b>G-Ring: </b><xsl:value-of select="."/></div>
									</xsl:for-each>
								</div>
							</xsl:for-each>
						</div>
					</xsl:for-each>
				</div>
			</xsl:if>
			<xsl:if test="minalti[normalize-space(.) != ''] or maxalti[normalize-space(.) != ''] or altunits[normalize-space(.) != '']">
				<div class="md-item">Altitude</div>
				<div class="md-itemhide">
					<!-- ESRI Profile element -->
					<xsl:for-each select="minalti[normalize-space(.) != '']">
						<div class="md"><b>Minimun altitude: </b><xsl:value-of select="."/></div>
					</xsl:for-each>
					<!-- ESRI Profile element -->
					<xsl:for-each select="maxalti[normalize-space(.) != '']">
						<div class="md"><b>Maximum altitude: </b><xsl:value-of select="."/></div>
					</xsl:for-each>
					<!-- ESRI Profile element -->		
					<xsl:for-each select="altunits[normalize-space(.) != '']">
						<div class="md"><b>Altitude units: </b>><xsl:value-of select="."/></div>
					</xsl:for-each>
				</div>
			</xsl:if>		
			<!-- ESRI Profile element -->
			<xsl:for-each select="eframes[framect[normalize-space(.) != ''] or framenam[normalize-space(.) != '']]">
				<xsl:for-each select="framect[normalize-space(.) != '']">
					<div class="md"><b>Data frame count: </b><xsl:value-of select="."/></div>
				</xsl:for-each>
				<xsl:for-each select="framenam[normalize-space(.) != '']">
					<div class="md"><b>Data frame name: </b><xsl:value-of select="."/></div>
				</xsl:for-each>
			</xsl:for-each>
		</div>
	</xsl:for-each>
</xsl:template>

<!-- Security Information -->
<xsl:template name="identification_security">
	<xsl:for-each select="/metadata/idinfo/secinfo[secsys[normalize-space(.) != ''] or secclass[normalize-space(.) != ''] or sechandl[normalize-space(.) != '']]">
		<div class="md-detail">
			<div class="md-detailtitle">Data Security Information</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">Handling restrictions imposed on the data because of national security, privacy or other concerns.</div>
			<xsl:for-each select="secsys[normalize-space(.) != '']">
				<div class="md"><b>Security classifiction system: </b><xsl:value-of select="."/></div>
			</xsl:for-each>
			<xsl:for-each select="secclass[normalize-space(.) != '']">
				<div class="md"><b>Security classification: </b><xsl:value-of select="."/></div>
			</xsl:for-each>
			<xsl:for-each select="sechandl[normalize-space(.) != '']">
				<div class="md"><b>Security handling: </b><xsl:value-of select="."/></div>
			</xsl:for-each>						
		</div>
	</xsl:for-each>
</xsl:template>	

<!-- Cross Reference -->
<xsl:template name="identification_cross_reference">
	<xsl:for-each select="/metadata/idinfo/crossref[assndesc[normalize-space(.) != ''] or citeinfo[normalize-space(.) != '']]">
		<div class="md-detail">
			<div class="md-detailtitle">Cross Reference</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">Information about other, related data sets that are likely to be of interest.</div>
			<!-- ESRI Profile element -->
			<xsl:for-each select="assndesc[normalize-space(.) != '']">
				<div class="md"><b>Association description: </b><xsl:value-of select="."/></div>
			</xsl:for-each>
			<xsl:for-each select="citeinfo[normalize-space(.) != '']">
				<xsl:call-template name="citation_info"/>
			</xsl:for-each>
		</div>
	</xsl:for-each>	
</xsl:template>

<!-- BROWSE GRAPHIC Metadata elements -->

<xsl:template name="browse_graphic">
	<div class="md-detail">
		<div class="md-detailtitle">Browse Graphic</div>
	</div>
	<div class="md-detailhide">
		<div id="md-def" name="md-def" class="md-def">Graphic illustration of the data.</div>				
		
	</div>
</xsl:template>

<!-- DATA QUALITY Metadata elements -->

<!-- General Data Quality info -->
<xsl:template name="data_quality_general">
	<xsl:for-each select="/metadata/dataqual[logic[normalize-space(.) != ''] or complete[normalize-space(.) != ''] or cloud[normalize-space(.) != '']]">
		<div class="md-detail">
			<div class="md-detailtitle">General</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">Information about the fidelity of relationships, data quality and accuracy tests, omissions, selection criteria, generalization, and definitions used to derive the data.</div>
			<xsl:for-each select="logic[normalize-space(.) != '']">
				<div class="md"><b>Logical consistency report: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
			</xsl:for-each>
			<xsl:for-each select="complete[normalize-space(.) != '']">
				<div class="md"><b>Completeness report: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
			</xsl:for-each>
			<xsl:for-each select="cloud[normalize-space(.) != '']">
				<div class="md"><b>Cloud cover: </b><xsl:value-of select="."/></div>
			</xsl:for-each>				
		</div>
	</xsl:for-each>
</xsl:template>

<!-- Attribute Accuracy -->
<xsl:template name="data_quality_attribute_accuracy">
	<xsl:for-each select="/metadata/dataqual/attracc[attraccr[normalize-space(.) != ''] or qattracc/attraccv[normalize-space(.) != ''] or qattracc/attracce[normalize-space(.) != '']]">
		<div class="md-detail">
			<div class="md-detailtitle">Attribute Accuracy</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">Accuracy of the identification of data entities, features and assignment of attribute values.</div>
			<xsl:for-each select="attraccr[normalize-space(.) != '']">
				<div class="md"><b>Attribute accuracy report: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
			</xsl:for-each>
			<xsl:if test="qattracc[normalize-space(.) != '']">
				<div class="md"><b>Attribute accuracy assessment:</b></div>
				<div class="md-itemlist">Accuracy values</div>
				<div class="md-itemshow">
					<xsl:for-each select="qattracc[normalize-space(.) != '']">
						<xsl:choose>
							<xsl:when test="attraccv[normalize-space(.) != '']">
								<div class="md-item"><xsl:value-of select="attraccv"/></div>
							</xsl:when>
							<xsl:otherwise>
								<div class="md-item">(value unknown)</div>
							</xsl:otherwise>
						</xsl:choose>
						<div class="md-itemhide">
							<xsl:for-each select="attracce[normalize-space(.) != '']">
								<div class="md-indent"><b>Explanation: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
							</xsl:for-each>
						</div>
					</xsl:for-each>
				</div>
			</xsl:if>
		</div>
	</xsl:for-each>			
</xsl:template>

<!-- Positional Accuracy -->
<xsl:template name="data_quality_positional_accuracy">
	<xsl:for-each select="/metadata/dataqual/posacc[horizpa[horizpar[normalize-space(.) != ''] or qhorizpa[horizpae[normalize-space(.) != '']]] or vertacc[vertaccr[normalize-space(.) != ''] or qvertpa[vertacce[normalize-space(.) != '']]]]">
		<div class="md-detail">
			<div class="md-detailtitle">Positional Accuracy</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">Accuracy of the positional aspects of the data.</div>
			<xsl:for-each select="horizpa[horizpar[normalize-space(.) != ''] or qhorizpa[horizpae[normalize-space(.) != '']]]">
				<xsl:for-each select="horizpar[normalize-space(.) != '']">
					<div class="md"><b>Horizontal accuracy report: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
				</xsl:for-each>
				<xsl:if test="qhorizpa[horizpae[normalize-space(.) != '']]">
					<div class="md"><b>Horizontal positional accuracy assessment:</b></div>
					<div class="md-itemlist">Accuracy values</div>
					<div class="md-itemshow">
						<xsl:for-each select="qhorizpa[horizpae[normalize-space(.) != '']]">
							<xsl:choose>
								<xsl:when test="horizpav[normalize-space(.) != '']">
									<div class="md-item"><xsl:value-of select="horizpav"/></div>
								</xsl:when>
								<xsl:otherwise>
									<div class="md-item">(value unknown)</div>
								</xsl:otherwise>
							</xsl:choose>
							<div class="md-itemhide">
								<xsl:for-each select="horizpae[normalize-space(.) != '']">
									<div class="md-indent"><b>Explanation: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
								</xsl:for-each>
							</div>
						</xsl:for-each>
					</div>
				</xsl:if>
			</xsl:for-each>
			<xsl:for-each select="vertacc[vertaccr[normalize-space(.) != ''] or qvertpa[vertacce[normalize-space(.) != '']]]">
				<xsl:for-each select="vertaccr[normalize-space(.) != '']">
					<div class="md"><b>Vertical accuracy report: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
				</xsl:for-each>
				<xsl:if test="qvertpa[vertacce[normalize-space(.) != '']]">
					<div class="md"><b>Vertical positional accuracy assessment:</b></div>
					<div class="md-itemlist">Accuracy values</div>
					<div class="md-itemshow">
						<xsl:for-each select="qvertpa[vertacce[normalize-space(.) != '']]">
							<xsl:choose>
								<xsl:when test="vertaccv[normalize-space(.) != '']">
									<div class="md-item"><xsl:value-of select="vertaccv"/></div>
								</xsl:when>
								<xsl:otherwise>
									<div class="md-item">(value unknown)</div>
								</xsl:otherwise>
							</xsl:choose>
							<div class="md-itemhide">
								<xsl:for-each select="vertacce[normalize-space(.) != '']">
									<div class="md-indent"><b>Explanation: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
								</xsl:for-each>
							</div>
						</xsl:for-each>
					</div>
				</xsl:if>
			</xsl:for-each>
		</div>
	</xsl:for-each>					
</xsl:template>

<!-- FGDC Data Source -->
<xsl:template name="data_quality_data_sources">
	<xsl:if test="/metadata/dataqual/lineage/srcinfo[normalize-space(.) != '']">
		<div class="md-detail">
			<div class="md-detailtitle">Data Sources</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">Information about the source data used to construct or derive the data.</div>
			<div class="md-itemlist">Data source information</div>
			<div class="md-itemshow">				
				<xsl:for-each select="/metadata/dataqual/lineage/srcinfo[normalize-space(.) != '']">
					<xsl:call-template name="data_source_info"/>
				</xsl:for-each>
			</div>
		</div>
	</xsl:if>
</xsl:template>

<!-- FGDC Process Step -->
<xsl:template name="data_quality_process_steps">
	<xsl:if test="/metadata/dataqual/lineage/procstep[normalize-space(.) != '']">
		<div class="md-detail">
			<div class="md-detailtitle">Process Steps</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">Information about events, parameters, tolerances and techniques applied to construct or derive the data.</div>
			<div class="md-itemlist">Process step information</div>
			<div class="md-itemshow">				
				
			</div>
		</div>
	</xsl:if>
</xsl:template>

<!-- ESRI Geoprocessing History -->
<xsl:template name="data_quality_esri_geoprocessing">
	<!-- ESRI Profile element -->
	<xsl:if test="/metadata/Esri/DataProperties/lineage/Process[normalize-space(.) != '']">
		<div class="md-detail">
			<div class="md-detailtitle">ESRI geoprocessing history</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">Description of ESRI geoprocessing commands, settings, and tolerances applied to the data.</div>
			<div class="md-itemlist">ESRI geoprocessing command information</div>
			<div class="md-itemshow">
				<!-- ESRI Profile element -->	
				
			</div>
		</div>
	</xsl:if>
</xsl:template>

<!-- DATA ORGANIZATION Metadata elements -->

<!-- SDTS Feature Type -->
<xsl:template name="data_organization_sdts_feature">
	<xsl:if test="/metadata/spdoinfo/ptvctinf/sdtsterm[sdtstype[normalize-space(.) != ''] or ptvctcnt[normalize-space(.) != '']]">
		<div class="md-detail">
			<div class="md-detailtitle">SDTS Feature Description</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">Description of point and vector spatial objects in the data using the Spatial Data Transfer Standards (SDTS) terminology.</div>
			<div class="md-itemlist">Spatial data transfer standard (SDTS) terms</div>
			<div class="md-itemshow">
				<xsl:for-each select="/metadata/spdoinfo/ptvctinf/sdtsterm[sdtstype[normalize-space(.) != ''] or ptvctcnt[normalize-space(.) != '']]">
					<xsl:choose>
					 	<!-- ESRI Profile element -->
						<xsl:when test="@Name != ''">
							<div class="md-item"><xsl:value-of select="@Name"/></div>
						</xsl:when>
						<xsl:otherwise>
							<div class="md-item">Feature class</div>
						</xsl:otherwise>
					</xsl:choose>
					<div class="md-itemhide">
						<xsl:for-each select="sdtstype[normalize-space(.) != '']">
							<div class="md"><b>Type: </b><xsl:value-of select="."/></div>
						</xsl:for-each>
						<xsl:for-each select="ptvctcnt[normalize-space(.) != '']">
							<div class="md"><b>Count: </b><xsl:value-of select="."/></div>
						</xsl:for-each>
					</div>
				</xsl:for-each>
			</div>
		</div>
	</xsl:if>	
</xsl:template>

<!-- VPF Feature Type -->
<xsl:template name="data_organization_vpf_feature">
	<xsl:if test="/metadata/spdoinfo/ptvctinf/vpfterm[vpflevel[normalize-space(.) != ''] or vpfinfo[vpftype[normalize-space(.) != ''] or ptvctcnt[normalize-space(.) != '']]]">
		<div class="md-detail">
			<div class="md-detailtitle">VPF Feature Description</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">Description of point and vector spatial objects in the data using the Vector Product Format (VPF) terminology.</div>
			<div class="md-itemlist">Vector Product Format (VPF) terms</div>
			<div class="md-itemshow">
				<xsl:for-each select="/metadata/spdoinfo/ptvctinf/vpfterm[vpflevel[normalize-space(.) != ''] or vpfinfo[vpftype[normalize-space(.) != ''] or ptvctcnt[normalize-space(.) != '']]]">
					<xsl:choose>
					 	<!-- ESRI Profile element -->
						<xsl:when test="@Name != ''">
							<div class="md-item"><xsl:value-of select="@Name"/></div>
						</xsl:when>
						<xsl:otherwise>
							<div class="md-item">Feature class</div>
						</xsl:otherwise>
					</xsl:choose>
					<div class="md-itemhide">
						<xsl:for-each select="vpflevel[normalize-space(.) != '']">
							<div class="md"><b>VPF topology level: </b><xsl:value-of select="."/></div>
						</xsl:for-each>
						<xsl:for-each select="vpfinfo[vpftype[normalize-space(.) != ''] or ptvctcnt[normalize-space(.) != '']]">
							<div class="md-indent">
								<xsl:for-each select="vpftype[normalize-space(.) != '']">
									<div class="md"><b>Type: </b><xsl:value-of select="."/></div>
								</xsl:for-each>
								<xsl:for-each select="ptvctcnt[normalize-space(.) != '']">
									<div class="md"><b>Count: </b><xsl:value-of select="."/></div>
								</xsl:for-each>
							</div>
						</xsl:for-each>
					</div>
				</xsl:for-each>
			</div>
		</div>
	</xsl:if>
</xsl:template>

	
						
<!-- Raster Information -->
<xsl:template name="data_organization_raster">
	<xsl:if test="/metadata/spdoinfo/rastinfo[normalize-space(.) != '']">
		<div class="md-detail">
			<div class="md-detailtitle">Raster Information</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">Type and number of raster spatial objects in the data.</div>
			<xsl:for-each select="/metadata/spdoinfo/rastinfo[normalize-space(.) != '']">
				<!-- ESRI Profile element -->
				<xsl:for-each select="rastifor[normalize-space(.) != '']">
					<div class="md"><b>Raster format: </b><xsl:value-of select="."/></div>
				</xsl:for-each>
				<!-- ESRI Profile element -->
				<xsl:for-each select="rastityp[normalize-space(.) != '']">
					<div class="md"><b>Raster type: </b><xsl:value-of select="."/></div>
				</xsl:for-each>
				<xsl:for-each select="rasttype[normalize-space(.) != '']">
					<div class="md"><b>Raster object type: </b><xsl:value-of select="."/></div>
				</xsl:for-each>
				<!-- ESRI Profile element -->
				<xsl:for-each select="rastband[normalize-space(.) != '']">
					<div class="md"><b>Number of raster bands: </b><xsl:value-of select="."/></div>
				</xsl:for-each>
				<xsl:if test=" rastorig[normalize-space(.) != ''] or rastplyr[normalize-space(.) != ''] or rastcmap[normalize-space(.) != ''] or rastcomp[normalize-space(.) != ''] or rastdtyp[normalize-space(.) != '']">
					<div class="md-item">Raster properties</div>
					<div class="md-itemhide">
					 	<!-- ESRI Profile element -->
						<xsl:for-each select="rastorig[normalize-space(.) != '']">
							<div class="md"><b>Raster origin: </b><xsl:value-of select="."/></div>
						</xsl:for-each>
						<!-- ESRI Profile element -->
						<xsl:for-each select="rastplyr[normalize-space(.) != '']">
							<div class="md"><b>Has pyramid layers: </b><xsl:value-of select="."/></div>
						</xsl:for-each>
						<!-- ESRI Profile element -->
						<xsl:for-each select="rastcmap[normalize-space(.) != '']">
							<div class="md"><b>Has image colormap: </b><xsl:value-of select="."/></div>
						</xsl:for-each>
						<!-- ESRI Profile element -->
						<xsl:for-each select="rastcomp[normalize-space(.) != '']">
							<div class="md"><b>Compression type: </b><xsl:value-of select="."/></div>
						</xsl:for-each>
						<!-- ESRI Profile element -->
						<xsl:for-each select="rastdtyp[normalize-space(.) != '']">
							<div class="md"><b>Raster display type: </b><xsl:value-of select="."/></div>
						</xsl:for-each>
					</div>		
				</xsl:if>
				<xsl:if test="rastxsz[normalize-space(.) != ''] or rastysz[normalize-space(.) != ''] or rastbpp[normalize-space(.) != ''] or vrtcount[normalize-space(.) != ''] or rowcount[normalize-space(.) != ''] or colcount[normalize-space(.) != '']">
					<div class="md-item">Cell information</div>
					<div class="md-itemhide">
						<xsl:for-each select="colcount[normalize-space(.) != '']">
							<div class="md"><b>Number of cells on x-axis: </b><xsl:value-of select="."/></div>
						</xsl:for-each>
						<xsl:for-each select="rowcount[normalize-space(.) != '']">
							<div class="md"><b>Number of cells on y-axis: </b><xsl:value-of select="."/></div>
						</xsl:for-each>
						<xsl:for-each select="vrtcount[normalize-space(.) != '']">
							<div class="md"><b>Number of cells on z-axis: </b><xsl:value-of select="."/></div>
						</xsl:for-each>
						<!-- ESRI Profile element -->
						<xsl:for-each select="rastbpp[normalize-space(.) != '']">
							<div class="md"><b>Bits per cell: </b><xsl:value-of select="."/></div>
						</xsl:for-each>
						<!-- ESRI Profile element -->
						<xsl:for-each select="rastnodt[normalize-space(.) != '']">
								<div class="md"><b>Background nodata value: </b><xsl:value-of select="."/></div>
						</xsl:for-each>
						<xsl:if test="rastxsz[normalize-space(.) != ''] or rastxu[normalize-space(.) != ''] or rastysz[normalize-space(.) != ''] or rastyu[normalize-space(.) != '']">
							<div class="md"><b>Cell Size:</b></div>
							<div class="md-indent">
								<!-- ESRI Profile element -->	
								<xsl:for-each select="rastxsz[normalize-space(.) != '']">
									<div class="md"><b>X direction: </b><xsl:value-of select="."/></div>
								</xsl:for-each>
								<!-- ESRI Profile element -->	
								<xsl:for-each select="rastxu[normalize-space(.) != '']">
									<div class="md"><b>X units: </b><xsl:value-of select="."/></div>
								</xsl:for-each>
								<!-- ESRI Profile element -->										
								<xsl:for-each select="rastysz[normalize-space(.) != '']">
									<div class="md"><b>Y direction: </b><xsl:value-of select="."/></div>
								</xsl:for-each>
								<!-- ESRI Profile element -->	
								<xsl:for-each select="rastyu[normalize-space(.) != '']">
									<div class="md"><b>Y units: </b><xsl:value-of select="."/></div>
								</xsl:for-each>									
							</div>
						</xsl:if>
					</div>
				</xsl:if>
			</xsl:for-each>
		</div>
	</xsl:if>
</xsl:template>

<!-- ESRI Terrain Information -->
<xsl:template name="data_organization_esri_terrain">
	<xsl:if test="/metadata/Esri/DataProperties/Terrain[normalize-space(.) != '']">
		<div class="md-detail">
			<div class="md-detailtitle">Terrain Information</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">Description of ESRI terrain class.</div>
			<xsl:for-each select="/metadata/Esri/DataProperties/Terrain[normalize-space(.) != '']">
				<!-- ESRI Profile element -->
				<xsl:for-each select="totalPts[normalize-space(.) != '']">
					<div class="md"><b>Total number of points: </b><xsl:value-of select="."/></div>
				</xsl:for-each>
			</xsl:for-each>
		</div>
	</xsl:if>
</xsl:template>

<!-- ESRI Address Locator Information -->
<xsl:template name="data_organization_esri_locator">
	<xsl:if test="/metadata/Esri/Locator[normalize-space(.) != '']">
		<div class="md-detail">
			<div class="md-detailtitle">Address Locator Information</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">Geocoding information for ESRI address locators</div>
			<xsl:for-each select="/metadata/Esri/Locator[normalize-space(.) != '']">
				<!-- ESRI Profile element -->
				<xsl:for-each select="Style[normalize-space(.) != '']">
					<div class="md"><b>Address locator style: </b><xsl:value-of select="."/></div>
				</xsl:for-each>
				<xsl:if test="Properties/FieldAliases[normalize-space(.) != '']">
					<div class="md"><b>Input Fields</b></div>
					<div class="md-indent">
					<!-- ESRI Profile element -->
						<xsl:for-each select="Properties/FieldAliases[normalize-space(.) != '']">
							<div>- <xsl:value-of select="."/></div>
						</xsl:for-each>
					</div>
				</xsl:if>	
				<xsl:if test="Properties/FileMAT[normalize-space(.) != ''] or Properties/FileSTN[normalize-space(.) != ''] or Properties/IntFileMAT[normalize-space(.) != ''] or Properties/IntFileSTN[normalize-space(.) != '']">
					<div class="md"><b>Geocoding Rule Bases</b></div>
					<div class="md-indent">
						<!-- ESRI Profile element -->
						<xsl:for-each select="Properties/FileMAT[normalize-space(.) != '']">
							<div class="md"><b>Match rules: </b><xsl:value-of select="."/></div>
						</xsl:for-each>
						<!-- ESRI Profile element -->
						<xsl:for-each select="Properties/FileSTN[normalize-space(.) != '']">
							<div class="md"><b>Standardization rules: </b><xsl:value-of select="."/></div>
						</xsl:for-each>
						<!-- ESRI Profile element -->
						<xsl:for-each select="Properties/IntFileMAT[normalize-space(.) != '']">
							<div class="md"><b>Intersection match rules: </b><xsl:value-of select="."/></div>
						</xsl:for-each>
						<!-- ESRI Profile element -->
						<xsl:for-each select="Properties/IntFileSTN[normalize-space(.) != '']">
							<div class="md"><b>Intersection standardization rules: </b><xsl:value-of select="."/></div>
						</xsl:for-each>
					</div>
				</xsl:if>
				<!-- ESRI Profile element -->
				<xsl:for-each select="Properties/Fallback[normalize-space(.) != '']">
					<div class="md"><b>Fallback matching: </b><xsl:value-of select="."/></div>
				</xsl:for-each>
			</xsl:for-each>
		</div>
	</xsl:if>
</xsl:template>

<!-- ATTRIBUTE and ENTITY INFORMATION Metadata elements -->

<!-- Overview -->
<xsl:template name="attributes_data_organization_overview">
	<xsl:if test="/metadata/eainfo/overview[normalize-space(.) != ''] or /metadata/spdoinfo[direct[normalize-space(.) != ''] or indspref[normalize-space(.) != '']]">
		<div class="md-detail">
			<div class="md-detailtitle">Overview</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">Summary of the information content of the data, including other references to complete descriptions of entity types, attributes, and attribute values for the data.</div>
			<xsl:for-each select="/metadata/eainfo/overview[dsoverv[normalize-space(.) != ''] or eaover[normalize-space(.) != ''] or eadetcit[normalize-space(.) != '']]">
				<xsl:for-each select="dsoverv[normalize-space(.) != '']">
					<div class="md"><b>Dataset overview: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
				</xsl:for-each>
				<xsl:for-each select="eaover[normalize-space(.) != '']">
					<div class="md"><b>Entity and attribute overview: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
				</xsl:for-each>
				<xsl:for-each select="eadetcit[normalize-space(.) != '']">
					<div class="md-indent">
						<div class="md"><b>Entity and attribute detailed citation: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
					</div>
				</xsl:for-each>
			</xsl:for-each>
			<xsl:for-each select="/metadata/spdoinfo[direct[normalize-space(.) != ''] or indspref[normalize-space(.) != '']]">
				<xsl:for-each select="direct[normalize-space(.) != '']">
					<div class="md"><b>Direct spatial reference method: </b> <xsl:value-of select="."/></div>
				</xsl:for-each>
				<xsl:for-each select="indspref[normalize-space(.) != '']">
					<div class="md"><b>Indirect spatial reference method: </b><xsl:value-of select="."/></div>
				</xsl:for-each>
			</xsl:for-each>
		</div>
	</xsl:if>
</xsl:template>

<!-- Entity attribute (Attributes of) -->
<xsl:template name="attributes_entity">
	<xsl:for-each select="/metadata/eainfo/detailed[normalize-space(.) != '']">
		<!-- Skip ESRI Profile elements that are relationship classes -->
		<xsl:choose>
			<xsl:when test="enttyp/enttypt[normalize-space(.) != '']">
				<xsl:if test="enttyp/enttypt[. != 'Relationship']">
					<div class="md-detail">
						<div class="md-detailtitle">
							<xsl:for-each select="enttyp/enttypl[normalize-space(.) != '']">			
								Attributes of <xsl:value-of select="."/>
							</xsl:for-each>
						</div>
					</div>
					<div class="md-detailhide">
						<div id="md-def" name="md-def" class="md-def">Detailed descriptions of entity type, attributes, and attribute values for the data.</div>
						<xsl:call-template name="attributes_entity_defintion"/>
					</div>
				</xsl:if>
			</xsl:when>
			<xsl:otherwise>
				<div class="md-detail">
					<div class="md-detailtitle">
						<xsl:for-each select="enttyp/enttypl[normalize-space(.) != '']">			
							Attributes of <xsl:value-of select="."/>
						</xsl:for-each>
					</div>
				</div>
				<div class="md-detailhide">
					<div id="md-def" name="md-def" class="md-def">Detailed descriptions of entity type, attributes, and attribute values for the data.</div>
					<xsl:call-template name="attributes_entity_defintion"/>
				</div>		
			</xsl:otherwise>
		</xsl:choose>	
	</xsl:for-each>	
</xsl:template>

<!-- Entity attribute definition -->
<xsl:template name="attributes_entity_defintion">
	<xsl:variable name="SrcName">
		<!-- ESRI Profile element -->
		<xsl:value-of select="@Name"/>
	</xsl:variable>
	<!-- ESRI Profile element -->
	<xsl:choose>
		<xsl:when test="@Name[normalize-space(.) != '']">
			<div class="md"><b>Name: </b><xsl:value-of select="@Name"/></div>
		</xsl:when>
	</xsl:choose>
	<!-- ESRI Profile element -->
	<xsl:for-each select="enttyp/enttypt[normalize-space(.) != '']">
		<div class="md"><b>Type of object: </b><xsl:value-of select="."/></div>
	</xsl:for-each>
	<!-- ESRI Profile element -->
	<xsl:for-each select="/metadata/spdoinfo/ptvctinf/esriterm[normalize-space(.) != '']">
		<xsl:choose>
			<xsl:when test="@Name = $SrcName">
				<xsl:for-each select="efeageom[normalize-space(.) != '']">
					<div class="md"><b>Geometry type: </b><xsl:value-of select="."/></div>
				</xsl:for-each>	
			</xsl:when>
		</xsl:choose>
	</xsl:for-each>
	<!-- ESRI Profile element -->
	<xsl:for-each select="enttyp/enttypc[normalize-space(.) != '']">
		<div class="md"><b>Number of records: </b><xsl:value-of select="."/></div>
	</xsl:for-each>
	<xsl:for-each select="enttyp/enttypd[normalize-space(.) != '']">
		<div class="md"><b>Description: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
	</xsl:for-each>
	<xsl:for-each select="enttyp/enttypds[normalize-space(.) != '']">
		<div class="md"><b>Source: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
	</xsl:for-each>
	<xsl:if test="attr//*">
		<div class="md-itemlist">Attributes</div>
		<div class="md-itemshow">				
			<xsl:for-each select="attr">
				<xsl:if test="attrlabl[normalize-space(.) != '']">	
					<xsl:for-each select="attrlabl[normalize-space(.) != '']">
						<div class="md-item"><xsl:value-of select="."/></div>
					</xsl:for-each>
					<div class="md-itemhide">
						<xsl:for-each select="attrdef[normalize-space(.) != '']">
							<div class="md"><b>Definition: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
						</xsl:for-each>
						<div class="md">
							<!-- ESRI Profile element -->
							<xsl:for-each select="attalias[normalize-space(.) != '']">
								<b>Alias: </b><xsl:value-of select="."/><xsl:text> </xsl:text>
							</xsl:for-each>
							<!-- ESRI Profile element -->
							<xsl:for-each select="attrtype[normalize-space(.) != '']">
								<b>Type: </b><xsl:value-of select="."/><xsl:text> </xsl:text>
							</xsl:for-each>
							<!-- ESRI Profile element -->
							<xsl:for-each select="attwidth[normalize-space(.) != '']">
								<b>Width: </b><xsl:value-of select="."/><xsl:text> </xsl:text>
							</xsl:for-each>
							<!-- ESRI Profile element -->
							<xsl:for-each select="atnumdec[normalize-space(.) != '']">
								<b>Number of decimals: </b><xsl:value-of select="."/><xsl:text> </xsl:text>
							</xsl:for-each>
							<!-- ESRI Profile element -->
							<xsl:for-each select="atprecis[normalize-space(.) != '']">
								<b>Precision: </b><xsl:value-of select="."/><xsl:text> </xsl:text>
							</xsl:for-each>
							<!-- ESRI Profile element -->
							<xsl:for-each select="attscale[normalize-space(.) != '']">
								<b>Scale: </b><xsl:value-of select="."/>
							</xsl:for-each>
							<!-- ESRI Profile element -->
							<xsl:for-each select="atoutwid[normalize-space(.) != '']">
								<b>Output width: </b><xsl:value-of select="."/>
							</xsl:for-each>
							<!-- ESRI Profile element -->
							<xsl:for-each select="atindex[normalize-space(.) != '']">
								<b>Attribute indexed: </b><xsl:value-of select="."/>
							</xsl:for-each>
						</div>
						<xsl:for-each select="attrvai">
							<xsl:for-each select="attrva[normalize-space(.) != '']">
								<div class="md"><b>Attribute value accuracy: </b><xsl:value-of select="."/></div>
							</xsl:for-each>
							<xsl:for-each select="attrvae[normalize-space(.) != '']">
								<div class="md"><b>Attribute value accuracy explanation: </b><xsl:value-of select="."/></div>
							</xsl:for-each>
						</xsl:for-each>
						<xsl:for-each select="attrmfrq[normalize-space(.) != '']">
							<div class="md"><b>Attribute measurement frequency: </b><xsl:value-of select="."/></div>
						</xsl:for-each>
						<xsl:for-each select="begdatea[normalize-space(.) != '']">
							<div class="md"><b>Beginning date of attribute values: </b><xsl:value-of select="."/></div>	
						</xsl:for-each>
						<xsl:for-each select="enddatea[normalize-space(.) != '']">
							<div class="md"><b>Ending date of attribute values: </b><xsl:value-of select="."/></div>	
						</xsl:for-each>
						<xsl:for-each select="attrdomv[normalize-space(.) != '']">
							<xsl:for-each select="udom[normalize-space(.) != '']">
								<div class="md"><b>Attribute values: </b><xsl:value-of select="."/></div>
							</xsl:for-each>
							<xsl:if test="edom[normalize-space(.) != '']">
								<div class="md-item">Attribute domain values</div>
								<div class="md-itemshow">
								<table class="md-grid">
									<tr><th>Value</th><th>Definition</th></tr>
									<xsl:for-each select="edom[normalize-space(.) != '']">
										<xsl:choose>
											<xsl:when test="edomvds[normalize-space(.) != '']">
												<tr>
													<xsl:choose>
														<xsl:when test="edomv[normalize-space(.) != '']">
															<td rowspan="2"><xsl:value-of select="edomv"/></td>
														</xsl:when>
														<xsl:otherwise>
															<td rowspan="2">(not provided)</td>
														</xsl:otherwise>
													</xsl:choose>
													<xsl:choose>
														<xsl:when test="edomvd[normalize-space(.) != '']">
															<td><pre id="fixvalue"><xsl:value-of select="edomvd"/></pre></td>
														</xsl:when>
														<xsl:otherwise>
															<td>(definition not provided)</td>
														</xsl:otherwise>
													</xsl:choose>
												</tr><tr>
													<xsl:choose>
														<xsl:when test="edomvds[normalize-space(.) != '']">
															<td class="md-italic"><xsl:text>Definition Source: </xsl:text><pre id="fixvalue"><xsl:value-of select="edomvds"/></pre></td>
														</xsl:when>
													</xsl:choose>
												</tr>
											</xsl:when>
											<xsl:otherwise>
												<tr>
													<xsl:choose>
														<xsl:when test="edomv[normalize-space(.) != '']">
															<td><xsl:value-of select="edomv"/></td>
														</xsl:when>
														<xsl:otherwise>
															<td>(not provided)</td>
														</xsl:otherwise>
													</xsl:choose>
													<xsl:choose>
														<xsl:when test="edomvd[normalize-space(.) != '']">
															<td><pre id="fixvalue"><xsl:value-of select="edomvd"/></pre></td>
														</xsl:when>
														<xsl:otherwise>
															<td>(definition not provided)</td>
														</xsl:otherwise>
													</xsl:choose>
												</tr>					
											</xsl:otherwise>
										</xsl:choose>
									</xsl:for-each>
								</table>
								</div>
							</xsl:if>
							<xsl:for-each select="rdom[normalize-space(.) != '']">
								<div class="md-item">Attribute domain range</div>
								<div class="md-itemshow">
									<table class="md-grid">
										<tr><th>Range</th><th>Value</th></tr>
										<xsl:for-each select="rdommin[normalize-space(.) != '']">
											<tr><td>Minimum</td><td><xsl:value-of select="."/></td></tr>	
										</xsl:for-each>
										<xsl:for-each select="rdommax[normalize-space(.) != '']">
											<tr><td>Maximum</td><td><xsl:value-of select="."/></td></tr>	
										</xsl:for-each>
										<!-- ESRI Profile element -->
										<xsl:for-each select="rdommean[normalize-space(.) != '']">
											<tr><td>Mean</td><td><xsl:value-of select="."/></td></tr>	
										</xsl:for-each>
										<!-- ESRI Profile element -->
										<xsl:for-each select="rdomstdv[normalize-space(.) != '']">
											<tr><td>Standard deviation</td><td><xsl:value-of select="."/></td></tr>	
										</xsl:for-each>					
										<xsl:for-each select="attrunit[normalize-space(.) != '']">
											<tr><td>Attribute units of measurement</td><td><xsl:value-of select="."/></td></tr>	
										</xsl:for-each>
										<xsl:for-each select="attrmres[normalize-space(.) != '']">
											<tr><td>Attribute measurement resolution</td><td><xsl:value-of select="."/></td></tr>	
										</xsl:for-each>
									</table>
								</div>							
							</xsl:for-each>
							<xsl:for-each select="codesetd[normalize-space(.) != '']">
								<div class="md-item">Attribute value codeset domain</div>
								<div class="md-itemshow">
									<table class="md-grid">
										<tr><th>Codeset</th><th>Description</th></tr>
										<xsl:for-each select="codesetn[normalize-space(.) != '']">
											<tr><td>Name</td><td><xsl:value-of select="."/></td></tr>	
										</xsl:for-each>
										<xsl:for-each select="codesets[normalize-space(.) != '']">
											<tr><td>Source</td><td><pre id="fixvalue"><xsl:value-of select="."/></pre></td></tr>	
										</xsl:for-each>
									</table>
								</div>
							</xsl:for-each>
						</xsl:for-each>
						<xsl:for-each select="attrdefs[normalize-space(.) != '']">
							<div class="md"><b>Attribute definition source: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
						</xsl:for-each>
					</div>
				</xsl:if>		
			</xsl:for-each>
		</div>
	</xsl:if>
</xsl:template>	

<!-- ESRI Subtype -->
<xsl:template name="attributes_esri_subtype">
	<xsl:for-each select="/metadata/eainfo/detailed[normalize-space(.) != '']">
	 	<!-- ESRI Profile element -->
		<xsl:if test="subtype[normalize-space(.) != '']">
			<div class="md-detail">
				<div class="md-detailtitle">
					<xsl:for-each select="enttyp/enttypl[normalize-space(.) != '']">		
						ESRI Subtypes of <xsl:value-of select="."/>
					</xsl:for-each>
				</div>
			</div>
			<div class="md-detailhide">
				<div id="md-def" name="md-def" class="md-def">Describes the subtypes that have been defined for a feature class in a geodatabase</div>
				<xsl:call-template name="attributes_esri_subtype_defintion"/>
			</div>
		</xsl:if>	
	</xsl:for-each>	
</xsl:template>

<!-- ESRI Subtype definition -->
<xsl:template name="attributes_esri_subtype_defintion">
	<xsl:choose>
		<xsl:when test="subtype/stfield">
			<div class="md">In the following list the subtype code is followed by the subtype name. Attributes (subtype fields) for each subtype are described in terms of their default value, valid domain values, value after merging or splitting features, etc.</div>
			<div class="md-itemlist">Subtypes</div>
			<div class="md-itemshow">
			 	<!-- ESRI Profile element -->
				<xsl:for-each select="subtype[normalize-space(.) != '']">
					<div class="md-item">
						<xsl:for-each select="stcode[normalize-space(.) != '']">
							<xsl:value-of select="."/> 
						</xsl:for-each>
						<xsl:for-each select="stname[normalize-space(.) != '']">
					 		- <xsl:value-of select="."/>
						</xsl:for-each>
					</div>
					<xsl:if test="stfield[normalize-space(.) != '']">
						<div class="md-itemhide">
							<div class="md-itemlist">Attributes</div>
							<div class="md-itemshow">
								<xsl:for-each select="stfield[normalize-space(.) != '']">
									<xsl:choose>
										 <xsl:when test="stfldnm[normalize-space(.) != '']">
											<div class="md-itemlist"><xsl:value-of select="stfldnm"/></div>
										</xsl:when>
										<xsl:otherwise>
											<div class="md-itemlist">Subtype field</div>
										</xsl:otherwise>
									</xsl:choose>
									<div class="md-itemhide">
										<xsl:for-each select="stflddv[normalize-space(.) != '']">
											<div class="md"><b>Default value: </b><xsl:value-of select="."/></div>
										</xsl:for-each>
										<xsl:for-each select="stflddd[normalize-space(.) != '']">
											<div class="md"><b>Attribute defined domain:</b></div>
											<div class="md-indent">
												<xsl:for-each select="domname[normalize-space(.) != '']">
													<div class="md"><b>Domain name: </b><xsl:value-of select="."/></div>
												</xsl:for-each>
												<xsl:for-each select="domdesc[normalize-space(.) != '']">
													<div class="md"><b>Domain description: </b><xsl:value-of select="."/></div>
												</xsl:for-each>
												<xsl:for-each select="domowner[normalize-space(.) != '']">
													<div class="md"><b>Domain owner: </b><xsl:value-of select="."/></div>
												</xsl:for-each>
												<xsl:for-each select="domfldtp[normalize-space(.) != '']">
													<div class="md"><b>Field type: </b><xsl:value-of select="."/></div>
												</xsl:for-each>
												<xsl:for-each select="domtype[normalize-space(.) != '']">
													<div class="md"><b>Domain type: </b><xsl:value-of select="."/></div>
												</xsl:for-each>
												<xsl:for-each select="mrgtype[normalize-space(.) != '']">
													<div class="md"><b>Merge rule: </b><xsl:value-of select="."/></div>
												</xsl:for-each>
												<xsl:for-each select="splttype[normalize-space(.) != '']">
													<div class="md"><b>Split rule: </b><xsl:value-of select="."/></div>
												</xsl:for-each>
											</div>
										</xsl:for-each>
									</div>
								</xsl:for-each>
							</div>		
						</div>
					</xsl:if>
				</xsl:for-each>		
			</div>
		</xsl:when>
		<xsl:otherwise>
			<div class="md">In the following list the subtype code is followed by the subtype name</div>
			<div class="md"><b>Subtypes</b></div>
			<div class="md-indent">
			 	<!-- ESRI Profile element -->
				<xsl:for-each select="subtype[normalize-space(.) != '']">
					<div class="md">
						<xsl:for-each select="stcode[normalize-space(.) != '']">
							<xsl:value-of select="."/> 
						</xsl:for-each>
						<xsl:for-each select="stname[normalize-space(.) != '']">
					 		- <xsl:value-of select="."/>
						</xsl:for-each>
					</div>
				</xsl:for-each>
			</div>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>

<!-- ESRI Relationship -->
<xsl:template name="attributes_esri_relationship">
	<!-- ESRI Profile element -->
	<xsl:for-each select="/metadata/eainfo/detailed/relinfo[normalize-space(.) != '']">
		<div class="md-detail">
			<div class="md-detailtitle">
				<xsl:for-each select="../enttyp/enttypl[normalize-space(.) != '']">		
					<xsl:value-of select="."/> ESRI Relationship Class 
				</xsl:for-each>
			</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">Describes the relationships defined for feature classes and data tables in a geodatabase</div>
			<xsl:call-template name="attributes_esri_relationship_definition"/>
		</div>
	</xsl:for-each>	
</xsl:template>

<!-- ESRI Relationship definition -->
<xsl:template name="attributes_esri_relationship_definition">
	<div class="md"><b>Relationship information:</b></div>
	<div class="md-indent">
		<xsl:for-each select="relcard[normalize-space(.) != '']">
			<div class="md"><b>Relationship cardinality: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
		<xsl:for-each select="relattr[normalize-space(.) != '']">
			<div class="md"><b>Attributed relationship: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
		<xsl:for-each select="relcomp[normalize-space(.) != '']">
			<xsl:choose>
				<xsl:when test=". = 'TRUE'">
					<div class="md"><b>Type of relationship: </b>Composite</div>
				</xsl:when>
				<xsl:otherwise>
					<div class="md"><b>Type of relationship: </b>Simple</div>
				</xsl:otherwise>
			</xsl:choose>	
		</xsl:for-each>
		<xsl:for-each select="relnodir[normalize-space(.) != '']">
			<div class="md"><b>Notification direction: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
		<xsl:for-each select="relflab[normalize-space(.) != '']">
			<div class="md"><b>Forward label: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
		<xsl:for-each select="relblab[normalize-space(.) != '']">
			<div class="md"><b>Backward label: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
	</div>
	<div class="md"><b>Origin table information:</b></div>
	<div class="md-indent">
		<xsl:for-each select="otfcname[normalize-space(.) != '']">
			<div class="md"><b>Origin name: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
		<xsl:for-each select="otfcpkey[normalize-space(.) != '']">
			<div class="md"><b>Primary key: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
		<xsl:for-each select="otfcfkey[normalize-space(.) != '']">
			<div class="md"><b>Foreign key: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
	</div>
	<div class="md"><b>Destination table information:</b></div>
	<div class="md-indent">
		<xsl:for-each select="dtfcname[normalize-space(.) != '']">
			<div class="md"><b>Origin name: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
		<xsl:for-each select="dtfcpkey[normalize-space(.) != '']">
			<div class="md"><b>Primary key: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
		<xsl:for-each select="dtfcfkey[normalize-space(.) != '']">
			<div class="md"><b>Foreign key: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
	</div>
</xsl:template>

<!-- DISTRIBUTION Metadata elements -->

<!-- General -->
<xsl:template name="distribution_general">
	<xsl:if test="resdesc[normalize-space(.) != ''] or distliab[normalize-space(.) != ''] or techpreq[normalize-space(.) != '']">
		<div class="md-detail">
			<div class="md-detailtitle">General</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">Description of the data known by the party from whom the data may be obtained, liability of party distributing data, and technical capabilities required to use the data. </div>
			<xsl:for-each select="resdesc[normalize-space(.) != '']">
				<div class="md"><b>Resource description: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
			</xsl:for-each>
			<xsl:for-each select="distliab[normalize-space(.) != '']">
				<div class="md"><b>Distribution liability: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
			</xsl:for-each>
			<xsl:for-each select="techpreq[normalize-space(.) != '']">
				<div class="md"><b>Technical prerequisites: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
			</xsl:for-each>
		</div>
	</xsl:if>
</xsl:template>

<!-- Distribution Point of Contact -->
<xsl:template name="distribution_contact">
	<xsl:for-each select="distrib/cntinfo[(cntperp/*[normalize-space(.) != '']) or (cntorgp/*[normalize-space(.) != '']) or (cntaddr/address[normalize-space(.) != '']) or (cntaddr/city[normalize-space(.) != '']) or (cntaddr/state[normalize-space(.) != '']) or (cntaddr/postal[normalize-space(.) != '']) or (cntaddr/country[normalize-space(.) != '']) or (cntvoice[normalize-space(.) != '']) or (cntfax[normalize-space(.) != '']) or (cntemail[normalize-space(.) != '']) or (hours[normalize-space(.) != '']) or (cntinst[normalize-space(.) != ''])]"> 
		<div class="md-detail">
			<div class="md-detailtitle">Distribution Point of Contact</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">Contact information for the individual or organization distributing the data.</div>
			<xsl:call-template name="contact_info"/>
		</div>
	</xsl:for-each>
</xsl:template>

<!-- Standard Order Process -->
<xsl:template name="distribution_standard_order">
	<xsl:for-each select="stdorder[normalize-space(.) != '']">	
		<div class="md-detail">
			<div class="md-detailtitle">Standard Order Process</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">Common ways in which data may be obtained.</div>
			<xsl:for-each select="nondig[normalize-space(.) != '']">
				<div class="md"><b>Non-digital form: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
			</xsl:for-each>
			<xsl:for-each select="digform[//*[normalize-space(.) != '']]">	
				<div class="md"><b>Digital form:</b></div>
					<div class="md-indent">			
					<xsl:for-each select="digtinfo[//*[normalize-space(.) != '']]">	
						<xsl:for-each select="formname[normalize-space(.) != '']">
							<div class="md"><b>Format name: </b><xsl:value-of select="."/></div>
						</xsl:for-each>
						<xsl:for-each select="formvern[normalize-space(.) != '']">
							<div class="md"><b>Format version number: </b><xsl:value-of select="."/></div>
						</xsl:for-each>
						<xsl:for-each select="formverd[normalize-space(.) != '']">
							<div class="md"><b>Format version date: </b><xsl:value-of select="."/></div>
						</xsl:for-each>
						<xsl:for-each select="formspec[normalize-space(.) != '']">
							<div class="md"><b>Format specification: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
						</xsl:for-each>
						<xsl:for-each select="formcont[normalize-space(.) != '']">
							<div class="md"><b>Format information content: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
						</xsl:for-each>
						<!-- ESRI Profile element -->
						<xsl:for-each select="dssize[normalize-space(.) != '']">
							<div class="md"><b>Size of the data: </b><xsl:value-of select="."/></div>
						</xsl:for-each>
						<xsl:for-each select="transize[normalize-space(.) != '']">
							<div class="md"><b>Transfer size: </b><xsl:value-of select="."/></div>
						</xsl:for-each>
						<xsl:for-each select="filedec[normalize-space(.) != '']">
							<div class="md"><b>File decompression technique: </b><xsl:value-of select="."/></div>
						</xsl:for-each>
					</xsl:for-each>
					<xsl:for-each select="digtopt[//*[normalize-space(.) != '']]">	
						<div class="md"><b>Digital transfer option:</b></div>
						<div class="md-indent">
							<xsl:for-each select="onlinopt[normalize-space(.) != '']">
								<div class="md"><b>Online option:</b></div>
								<div class="md-indent">
									<xsl:for-each select="computer[normalize-space(.) != '']">
										<div class="md"><b>Computer information:</b></div>
										<div class="md-indent">
											<xsl:for-each select="networka[normalize-space(.) != '']">
												<div class="md"><b>Network address:</b></div>
												<div class="md-indent">
													<xsl:for-each select="networkr[normalize-space(.) != '']">
														<div class="md"><b>Network resource name: </b><A TARGET="viewer"><xsl:attribute name="HREF"><xsl:value-of select="."/></xsl:attribute><xsl:value-of select="."/></A></div>
													</xsl:for-each>
												</div>
											</xsl:for-each>
											<!-- ESRI Profile element -->
											<xsl:for-each select="sdeconn[//*[normalize-space(.) != '']]">	
												<div class="md"><b>Spatial Database connection:</b></div>
												<div class="md-indent">
													<xsl:for-each select="server[normalize-space(.) != '']">
														<div class="md"><b>Server: </b><xsl:value-of select="."/></div>
													</xsl:for-each>
													<xsl:for-each select="instance[normalize-space(.) != '']">
														<div class="md"><b>Instance: </b><xsl:value-of select="."/></div>
													</xsl:for-each>
													<xsl:for-each select="database[normalize-space(.) != '']">
														<div class="md"><b>Database: </b><xsl:value-of select="."/></div>
													</xsl:for-each>
													<xsl:for-each select="user[normalize-space(.) != '']">
														<div class="md"><b>User: </b><xsl:value-of select="."/></div>
													</xsl:for-each>
													<xsl:for-each select="version[normalize-space(.) != '']">
														<div class="md"><b>Version: </b><xsl:value-of select="."/></div>
													</xsl:for-each>
												</div>
											</xsl:for-each>
											<xsl:for-each select="dialinst[//*[normalize-space(.) != '']]">	
												<div class="md"><b>Dialup instructions:</b></div>
												<div class="md-indent">
													<xsl:for-each select="lowbps[normalize-space(.) != '']">
														<div class="md"><b>Lowest BPS: </b><xsl:value-of select="."/></div>
													</xsl:for-each>
													<xsl:for-each select="highbps[normalize-space(.) != '']">
														<div class="md"><b>Highest BPS: </b><xsl:value-of select="."/></div>
													</xsl:for-each>
													<xsl:for-each select="numdata[normalize-space(.) != '']">
														<div class="md"><b>Number DataBits: </b><xsl:value-of select="."/></div>
													</xsl:for-each>
													<xsl:for-each select="numstop[normalize-space(.) != '']">
														<div class="md"><b>Number StopBits: </b><xsl:value-of select="."/></div>
													</xsl:for-each>
													<xsl:for-each select="parity[normalize-space(.) != '']">
														<div class="md"><b>Parity: </b><xsl:value-of select="."/></div>
													</xsl:for-each>
													<xsl:for-each select="compress[normalize-space(.) != '']">
														<div class="md"><b>Compression support: </b><xsl:value-of select="."/></div>
													</xsl:for-each>
													<xsl:for-each select="dialtel[normalize-space(.) != '']">
														<div class="md"><b>Dialup telephone: </b><xsl:value-of select="."/></div>
													</xsl:for-each>
													<xsl:for-each select="dialfile[normalize-space(.) != '']">
														<div class="md"><b>Dialup file name: </b><xsl:value-of select="."/></div>
													</xsl:for-each>
												</div>
											</xsl:for-each>
										</div>
									</xsl:for-each>
									<xsl:for-each select="accinstr[normalize-space(.) != '']">
										<div class="md"><b>Access instructions: </b><xsl:value-of select="."/></div>
									</xsl:for-each>
									<xsl:for-each select="oncomp[normalize-space(.) != '']">
										<div class="md"><b>Online computer and operating system: </b><xsl:value-of select="."/></div>
									</xsl:for-each>
								</div>
							</xsl:for-each>
							<xsl:for-each select="offoptn[//*[normalize-space(.) != '']]">	
								<div class="md"><b>Offline option:</b></div>
								<div class="md-indent">
									<xsl:for-each select="offmedia[normalize-space(.) != '']">
										<div class="md"><b>Offline media: </b><xsl:value-of select="."/></div>
									</xsl:for-each>
									<xsl:for-each select="reccap[//*[normalize-space(.) != '']]">	
										<div class="md"><b>Recording capacity:</b></div>
											<div class="md-indent">
											<xsl:for-each select="recden[normalize-space(.) != '']">
												<div class="md"><b>Recording density: </b><xsl:value-of select="."/></div>
											</xsl:for-each>
											<xsl:for-each select="recdenu[normalize-space(.) != '']">
												<div class="md"><b>Recording density units: </b><xsl:value-of select="."/></div>
											</xsl:for-each>
										</div>
									</xsl:for-each>
									<xsl:for-each select="recfmt[normalize-space(.) != '']">
										<div class="md"><b>Recording format: </b><xsl:value-of select="."/></div>
									</xsl:for-each>
									<xsl:for-each select="compat[normalize-space(.) != '']">
										<div class="md"><b>Compatibility information: </b><xsl:value-of select="."/></div>
									</xsl:for-each>
								</div>
							</xsl:for-each>
						</div>
					</xsl:for-each>
				</div>
			</xsl:for-each>
			<xsl:for-each select="fees[normalize-space(.) != '']">
				<div class="md"><b>Fees: </b><xsl:value-of select="."/></div>
			</xsl:for-each>
			<xsl:for-each select="ordering[normalize-space(.) != '']">
				<div class="md"><b>Ordering instructions: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
			</xsl:for-each>
			<xsl:for-each select="turnarnd[normalize-space(.) != '']">
				<div class="md"><b>Turnaround: </b><xsl:value-of select="."/></div>
			</xsl:for-each>
		</div>
	</xsl:for-each>
</xsl:template>

<!-- Custom Order Process -->
<xsl:template name="distribution_custom_order">
	<xsl:for-each select="custom[normalize-space(.) != '']">
		<div class="md-detail">
			<div class="md-detailtitle">Custom Order Process</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">Description of custom distribution services available.</div>
			<div class="md"><b>Custom order process: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
		</div>
	</xsl:for-each>					
</xsl:template>	

<!--  Available Time Period -->
<xsl:template name="distribution_time_period">
	<xsl:for-each select="availabl[(timeinfo/*[normalize-space(.) != '']) or (current[normalize-space(.) != ''])]">
		<div class="md-detail">
			<div class="md-detailtitle">Available Time Period</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">Time when data is available from the distributer.</div>
			<xsl:call-template name="time_info"/>
		</div>
	</xsl:for-each>
</xsl:template>	

<!-- METADATA elements -->

<!-- Metadata Point of Contact -->
<xsl:template name="metadata_contact">
	<xsl:for-each select="/metadata/metainfo/metc/cntinfo[(cntperp/*[normalize-space(.) != '']) or (cntorgp/*[normalize-space(.) != '']) or (cntaddr/address[normalize-space(.) != '']) or (cntaddr/city[normalize-space(.) != '']) or (cntaddr/state[normalize-space(.) != '']) or (cntaddr/postal[normalize-space(.) != '']) or (cntaddr/country[normalize-space(.) != '']) or (cntvoice[normalize-space(.) != '']) or (cntfax[normalize-space(.) != '']) or (cntemail[normalize-space(.) != '']) or (hours[normalize-space(.) != '']) or (cntinst[normalize-space(.) != ''])]"> 
		<div class="md-detail">
			<div class="md-detailtitle">Metadata Point of Contact</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">Contact information for the individual or organization responsible for the metadata information.</div>
			<xsl:call-template name="contact_info"/>
		</div>
	</xsl:for-each>
</xsl:template>	

<!-- Metadata Date -->
<xsl:template name="metadata_date">
	<xsl:for-each select="/metadata/metainfo[metd[normalize-space(.) != ''] or metrd[normalize-space(.) != ''] or metfrd[normalize-space(.) != ''] or langmeta[normalize-space(.) != '']]">
		<div class="md-detail">
			<div class="md-detailtitle">Metadata Date</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">Dates associated with creating, updating and reviewing the metadata.</div>
			<xsl:for-each select="metd[normalize-space(.) != '']">
				<div class="md"><b>Last updated: </b><xsl:value-of select="."/></div>
			</xsl:for-each>
			<xsl:for-each select="metrd[normalize-space(.) != '']">
				<div class="md"><b>Last metadata review date: </b><xsl:value-of select="."/></div>
			</xsl:for-each>
			<xsl:for-each select="metfrd[normalize-space(.) != '']">
				<div class="md"><b>Future metadata review date: </b><xsl:value-of select="."/></div>
			</xsl:for-each>
			<!-- ESRI Profile element -->
			<xsl:for-each select="langmeta[normalize-space(.) != '']">
				<div class="md"><b>Language of metadata: </b><xsl:value-of select="."/></div>
			</xsl:for-each>
		</div>
	</xsl:for-each>
</xsl:template>

<!-- Metadata Access -->
<xsl:template name="metadata_access">
	<xsl:for-each select="/metadata/metainfo[metac[normalize-space(.) != ''] or metuc[normalize-space(.) != '']]">
		<div class="md-detail">
			<div class="md-detailtitle">Metadata Access Constraints</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">Restrictions and legal prerequisites for accessing or using the data after access is granted.</div>
			<xsl:for-each select="metac[normalize-space(.) != '']">
				<div class="md"><b>Access constraints: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
			</xsl:for-each>
			<xsl:for-each select="metuc[normalize-space(.) != '']">
				<div class="md"><b>Use constraints: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
			</xsl:for-each>
		</div>
	</xsl:for-each>
</xsl:template>

<!-- Metadata Security Information -->
<xsl:template name="metadata_security">
	<xsl:for-each select="/metadata/metainfo/metsi[metscs[normalize-space(.) != ''] or metsc[normalize-space(.) != ''] or metshd[normalize-space(.) != '']]">
		<div class="md-detail">
			<div class="md-detailtitle">Metadata Security Information</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">Handling restrictions imposed on the metadata because of national security, privacy or other concerns.</div>
			<xsl:for-each select="metscs[normalize-space(.) != '']">
				<div class="md"><b>Security classifiction system: </b><xsl:value-of select="."/></div>
			</xsl:for-each>
			<xsl:for-each select="metsc[normalize-space(.) != '']">
				<div class="md"><b>Security classification: </b><xsl:value-of select="."/></div>
			</xsl:for-each>
			<xsl:for-each select="metshd[normalize-space(.) != '']">
				<div class="md"><b>Security handling: </b><xsl:value-of select="."/></div>
			</xsl:for-each>						
		</div>
	</xsl:for-each>
</xsl:template>	

<!-- Metadata Standards -->
<xsl:template name="metadata_standard">
	<xsl:for-each select="/metadata/metainfo[metstdn[normalize-space(.) != ''] or metstdv[normalize-space(.) != ''] or mettc[normalize-space(.) != ''] or metextns[*[normalize-space(.) != '']]]">
			<div class="md-detail">
				<div class="md-detailtitle">Metadata Standards</div>
			</div>
			<div class="md-detailhide">
				<div id="md-def" name="md-def" class="md-def">Description of the metadata standard used to document the data and reference to any additional extended profiles to the standard used by the metadata producer.</div>
				<xsl:for-each select="metstdn[normalize-space(.) != '']">
					<div class="md"><b>Standard name: </b><xsl:value-of select="."/></div>
				</xsl:for-each>
				<xsl:for-each select="metstdv[normalize-space(.) != '']">
					<div class="md"><b>Standard version: </b><xsl:value-of select="."/></div>
				</xsl:for-each>
				<xsl:for-each select="mettc[normalize-space(.) != '']">
					<div class="md"><b>Time convention: </b><xsl:value-of select="."/></div>
				</xsl:for-each>
				<xsl:if test="metextns[normalize-space(.) != '']">
					<div class="md"><b>Metadata profiles defining additonal information:</b></div>
					<xsl:for-each select="metextns[normalize-space(.) != '']">
						<div class="md-indent">
							<xsl:for-each select="metprof[normalize-space(.) != '']">
								<div class="md"><b>Profile: </b><xsl:value-of select="."/></div>
							</xsl:for-each>
							<div class="md-indent">
								<b>Online linkage: </b>
								<xsl:for-each select="onlink[normalize-space(.) != '']">						
									<a target="viewer"><xsl:attribute name="href"><xsl:value-of select="."/></xsl:attribute><xsl:value-of select="."/></a>
									<xsl:if test="position() != last()"><xsl:text>, </xsl:text></xsl:if>
								</xsl:for-each>
							</div>
						</div>
					</xsl:for-each>
				</xsl:if>
			</div>
	</xsl:for-each>
</xsl:template>

<!-- FGDC Plus Metadata Stylesheet info -->
<xsl:template name="metadata_fgdc_plus_stylesheet">
	<div class="md-detail">
		<div class="md-detailtitle">FGDC Plus Metadata Stylesheet</div>
	</div>
	<div class="md-detailhelp">
		<div class="md"><b>Stylesheet: </b>FGDC Plus Stylesheet</div>
		<div class="md"><b>File name: </b>FGDC Plus.xsl</div>
		<div class="md"><b>Version: </b>2.3 </div>
		<div class="md"><b>Description: </b>This metadata is displayed using the FGDC Plus Stylesheet, which is an XSL template that can be used with ArcGIS software to display metadata. It displays metadata elements defined in the Content Standard for Digital Geospatial Metadata (<a target="viewer" href="http://www.fgdc.gov/standards/projects/FGDC-standards-projects/metadata/base-metadata/v2_0698.pdf">CSDGM</a>) - aka FGDC Standard, the <a target="viewer" href="http://www.esri.com/metadata/esriprof80.html">ESRI Profile</a> of CSDGM, the <a target="viewer" href="http://www.fgdc.gov/standards/projects/FGDC-standards-projects/metadata/biometadata/biodatap.pdf">Biological Data Profile</a> of CSDGM, and the <a target="viewer" href="http://www.csc.noaa.gov/metadata/sprofile.pdf">Shoreline Data Profile</a> of CSDGM. CSDGM is the US Federal Metadata standard. The <a href=" http://www.fgdc.gov">Federal Geographic Data Committee</a> originally adopted the CSDGM in 1994 and revised it in 1998. According to Executive Order 12096 all Federal agencies are ordered to use this standard to document geospatial data created as of January, 1995. The standard is often referred to as the FGDC Metadata Standard and has been implemented beyond the federal level with State and local governments adopting the metadata standard as well.
The Biological Data Profile broadens the application of the CSDGM so that it is more easily applied to biological data that are not explicitly geographic (laboratory results, field notes, specimen collections, research reports) but can be associated with a geographic location. Includes taxonomical vocabulary. The Shoreline Data Profile addresses variability in the definition and mapping of shorelines by providing a standardized set of terms and data elements required to support metadata for shoreline and coastal data sets. The FGDC Plus Stylesheet includes the <a target="viewer" href="http://dublincore.org/">Dublin Core Metadata Element Set</a>. It supports W3C DOM compatible browsers such as IE7, IE6, Netscape 7, and Mozilla Firefox. It is in the public domain and may be freely used, modified, and redistributed. It is provided "AS-IS" without warranty or technical support.</div>
		<div class="md"><b>Instructions: </b>On the top of the page, click on the title of the dataset to toggle opening and closing of all metadata content sections or click section links listed horizontally below the title to open individual sections. Click on a section name (e.g. Description) to open and close section content. Within a section, click on a item name (Status, Key Words, etc.) to open and close individual content items. By default, the Citation information within the Description section is always open for display.</div>
		<div class="md"><b>Download: </b>FGDC Plus Stylesheet is available from the ArcScripts downloads at <a target="viewer" href="http://www.esri.com">www.esri.com</a>.</div>
	</div>
</xsl:template>
		
<!-- SPATIAL REFERENCE Metadata elements -->

<!-- Horizontal Coordinate System -->
<xsl:template name="horizontal_coordinate_system">
	<xsl:if test="/metadata/spref/horizsys[geograph | planar | local | cordsysn | geodetic]">
		<xsl:for-each select="/metadata/spref/horizsys[normalize-space(.) != '']">
			<div class="md-detail">
				<div class="md-detailtitle">Horizontal Coordinate System</div>
			</div>
			<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">Reference system from which linear or angular quantities are measured and assigned to the position that a point occupies.</div>
				<!-- ESRI Profile element -->
				<xsl:if test="cordsysn/projcsn[normalize-space(.) != '']">
					<div class="md"><b>Projected coordinate system:</b></div>
					<div class="md-indent">
						<!-- ESRI Profile element -->
						<xsl:for-each select="cordsysn/projcsn[normalize-space(.) != '']">
							<div class="md"><b>Name: </b><xsl:value-of select="translate(.,'_',' ')"/></div>
						</xsl:for-each>
						<xsl:for-each select="planar/planci/plandu[normalize-space(.) != '']">
							<div class="md"><b>Map units: </b><xsl:value-of select="."/></div>
						</xsl:for-each>
					</div>
				</xsl:if>
				<!-- ESRI Profile element -->
				<xsl:if test="cordsysn/geogcsn[normalize-space(.) != '']">
					<div class="md"><b>Geographic coordinate system:</b></div>			
					<div class="md-indent">
						<!-- ESRI Profile element -->
						<xsl:for-each select="cordsysn/geogcsn[normalize-space(.) != '']">
							<div class="md"><b>Name: </b><xsl:value-of select="translate(.,'_',' ')"/></div>
						</xsl:for-each>
						<xsl:for-each select="geograph/eogunit[normalize-space(.) != '']">
							<div class="md"><b>Units: </b><xsl:value-of select="."/></div>
						</xsl:for-each>
					</div>
				</xsl:if>
				<xsl:if test="geograph | planar | local | geodetic">
					<div class="md-itemlist">Coordinate System Details</div>
					<div class="md-itemshow">
						<xsl:apply-templates select="geograph"/>
						<xsl:apply-templates select="planar"/>
						<xsl:apply-templates select="local"/>
					</div>
					<xsl:apply-templates select="geodetic"/>
				</xsl:if>
			</div>
		</xsl:for-each>
	</xsl:if>		
</xsl:template>

<!-- Geographic Coordinate System -->
<xsl:template match="/metadata/spref/horizsys/geograph">
	<div class="md-item">Geographic coordinate system</div>
	<div class="md-itemhide">
		<xsl:for-each select="latres[normalize-space(.) != '']">
			<div class="md"><b>Latitude resolution: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
		<xsl:for-each select="longres[normalize-space(.) != '']">
			<div class="md"><b>Longitude resolution: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
		<xsl:for-each select="geogunit[normalize-space(.) != '']">
			<div class="md"><b>Geographic coordinate units: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
	</div>
</xsl:template>

<!-- Planar Coordinate System -->
<xsl:template match="/metadata/spref/horizsys/planar">
	<xsl:for-each select="mapproj">
		<div class="md-item">Map projection</div>
		<div class="md-itemhide">
			<xsl:apply-templates select="*"/>
		</div>
	</xsl:for-each>

	<xsl:for-each select="gridsys">
		<div class="md-item">Grid coordinate system</div>
		<div class="md-itemhide">
			<xsl:for-each select="gridsysn[normalize-space(.) != '']">
				<div class="md"><b>Grid coordinate system name: </b><xsl:value-of select="."/></div>
			</xsl:for-each>

			<xsl:for-each select="utm">
				<div class="md"><b>Universal Transverse Mercator:</b></div>
				<div class="md-indent">
					<xsl:for-each select="utmzone[normalize-space(.) != '']">
						<div class="md"><b>UTM zone number: </b><xsl:value-of select="."/></div>
					</xsl:for-each>
					<xsl:for-each select="transmer">
						<div class="md"><b>Transverse Mercator:</b></div>
					</xsl:for-each>
					<xsl:apply-templates select="transmer"/>
				</div>
			</xsl:for-each>

			<xsl:for-each select="ups">
				<div class="md"><b>Universal Polar Stereographic:</b></div>
				<div class="md-indent">
					<xsl:for-each select="upszone[normalize-space(.) != '']">
						<div class="md"><b>UPS zone identifier: </b><xsl:value-of select="."/></div>
					</xsl:for-each>
					<xsl:for-each select="polarst">
						<div class="md"><b>Polar Stereographic:</b></div>
					</xsl:for-each>
					<xsl:apply-templates select="polarst"/>
				</div>
			</xsl:for-each>

			<xsl:for-each select="spcs">
				<div class="md"><b>State Plane Coordinate System:</b></div>
				<div class="md-indent">
					<xsl:for-each select="spcszone[normalize-space(.) != '']">
						<div class="md"><b>SPCS xone identifier: </b><xsl:value-of select="."/></div>
					</xsl:for-each>
					<xsl:for-each select="lambertc">
						<div class="md"><b>Lambert Conformal Conic:</b></div>
					</xsl:for-each>
					<xsl:apply-templates select="lambertc"/>
					<xsl:for-each select="transmer">
						<div class="md"><b>Transverse Mercator:</b></div>
					</xsl:for-each>
					<xsl:apply-templates select="transmer"/>
					<xsl:for-each select="obqmerc">
						<div class="md"><b>Oblique Mercator:</b></div>
					</xsl:for-each>
					<xsl:apply-templates select="obqmerc"/>
					<xsl:for-each select="polycon">
						<div class="md"><b>Polyconic:</b></div>
					</xsl:for-each>
					<xsl:apply-templates select="polycon"/>
				</div>
			</xsl:for-each>

			<xsl:for-each select="arcsys">
				<div class="md"><b>ARC Coordinate System:</b></div>
				<div class="md-indent">
					<xsl:for-each select="arczone[normalize-space(.) != '']">
						<div class="md"><b>ARC system zone identifier: </b><xsl:value-of select="."/></div>
					</xsl:for-each>
					<xsl:for-each select="equirect">
						<div class="md"><b>Equirectangular:</b></div>
					</xsl:for-each>
					<xsl:apply-templates select="equirect"/>
					<xsl:for-each select="azimequi">
						<div class="md"><b>Azimuthal Equidistant:</b></div>
					</xsl:for-each>
					<xsl:apply-templates select="azimequi"/>
				</div>
			</xsl:for-each>

			<xsl:for-each select="othergrd[normalize-space(.) != '']">
				<div class="md"><b>Other Grid System's Definition: </b><xsl:value-of select="."/></div>
			</xsl:for-each>
		</div>
	</xsl:for-each>

	<xsl:for-each select="localp">
		<div class="md-item">Local Planar</div>
		<div class="md-itemhide">
			<xsl:for-each select="localpd[normalize-space(.) != '']">
				<div class="md"><b>Description: </b><xsl:value-of select="."/></div>
			</xsl:for-each>
			<xsl:for-each select="localpgi[normalize-space(.) != '']">
				<div class="md"><b>Georeference Information: </b><xsl:value-of select="."/></div>
			</xsl:for-each>
		</div>
	</xsl:for-each>

	<xsl:for-each select="planci">
		<div class="md-item">Planar Coordinate Information</div>
		<div class="md-itemhide">
			<xsl:for-each select="plance[normalize-space(.) != '']">
				<div class="md"><b>Planar coordinate encoding method: </b><xsl:value-of select="."/></div>
			</xsl:for-each>
			<xsl:for-each select="coordrep">
				<div class="md"><b>Coordinate representation:</b></div>
				<div class="md-indent">
					<xsl:for-each select="absres[normalize-space(.) != '']">
						<div class="md"><b>Abscissa resolution: </b><xsl:value-of select="."/></div>
					</xsl:for-each>
					<xsl:for-each select="ordres[normalize-space(.) != '']">
						<div class="md"><b>Ordinate resolution: </b><xsl:value-of select="."/></div>
					</xsl:for-each>
				</div>
			</xsl:for-each>
			<xsl:for-each select="distbrep">
				<div class="md"><b>Distance and bearing representation:</b></div>
				<div class="md-indent">
					<xsl:for-each select="distres[normalize-space(.) != '']">
						<div class="md"><b>Distance resolution: </b><xsl:value-of select="."/></div>
					</xsl:for-each>
					<xsl:for-each select="bearres[normalize-space(.) != '']">
						<div class="md"><b>Bearing resolution: </b><xsl:value-of select="."/></div>
					</xsl:for-each>
					<xsl:for-each select="bearunit[normalize-space(.) != '']">
						<div class="md"><b>Bearing units: </b><xsl:value-of select="."/></div>
					</xsl:for-each>
					<xsl:for-each select="bearrefd[normalize-space(.) != '']">
						<div class="md"><b>Bearing reference direction: </b><xsl:value-of select="."/></div>
					</xsl:for-each>
					<xsl:for-each select="bearrefm[normalize-space(.) != '']">
						<div class="md"><b>Bearing reference meridian: </b><xsl:value-of select="."/></div>
					</xsl:for-each>
				</div>
			</xsl:for-each>
			<xsl:for-each select="plandu[normalize-space(.) != '']">
				<div class="md"><b>Planar distance units: </b><xsl:value-of select="."/></div>
			</xsl:for-each>
		</div>
	</xsl:for-each>
</xsl:template>

<!-- Local Coordinate System -->
<xsl:template match="/metadata/spref/horizsys/local">
	<div class="md-item">Local Coordinate System Details</div>
	<div class="md-itemhide">
		<xsl:for-each select="localdes[normalize-space(.) != '']">
			<div class="md"><b>Description: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
		<xsl:for-each select="localgeo[normalize-space(.) != '']">
			<div class="md"><b>Georeference information: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
	</div>
</xsl:template>

<!-- Geodetic Model -->
<xsl:template match="/metadata/spref/horizsys/geodetic">
	<div class="md-item">Geodetic model</div>
	<div class="md-itemhide">
		<xsl:for-each select="horizdn[normalize-space(.) != '']">
			<div class="md"><b>Horizontal datum name: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
		<xsl:for-each select="ellips[normalize-space(.) != '']">
			<div class="md"><b>Ellipsoid name: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
		<xsl:for-each select="semiaxis[normalize-space(.) != '']">
			<div class="md"><b>Semi-major axis: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
		<xsl:for-each select="denflat[normalize-space(.) != '']">
			<div class="md"><b>Denominator of flattening ratio: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
	</div>
</xsl:template>

<!-- Vertical Coordinate Systems -->
<xsl:template name="vertical_coordinate_system">
	<xsl:for-each select="/metadata/spref/vertdef[normalize-space(.) != '']">
		<div class="md-detail">
			<div class="md-detailtitle">Vertical Coordinate System</div>
		</div>
		<div class="md-detailhide">
			<div id="md-def" name="md-def" class="md-def">Reference system from which vertical distances (altitudes or depths) are measured.</div>
			<xsl:for-each select="altsys[normalize-space(.) != '']">
				<div class="md"><b>Altitude system definition:</b></div>
				<div class="md-indent">
					<xsl:for-each select="altdatum[normalize-space(.) != '']">
						<div class="md"><b>Altitude datum name: </b><xsl:value-of select="."/></div>
					</xsl:for-each>
					<xsl:for-each select="altres[normalize-space(.) != '']">
						<div class="md"><b>Altitude resolution: </b><xsl:value-of select="."/></div>
					</xsl:for-each>
					<xsl:for-each select="altunits[normalize-space(.) != '']">
						<div class="md"><b>Altitude distance units: </b><xsl:value-of select="."/></div>
					</xsl:for-each>
					<xsl:for-each select="altenc[normalize-space(.) != '']">
						<div class="md"><b>Altitude encoding method: </b><xsl:value-of select="."/></div>
					</xsl:for-each>
				</div>
			</xsl:for-each>
			<xsl:for-each select="depthsys[normalize-space(.) != '']">
				<div class="md"><b>Depth system definition:</b></div>
				<div class="md-indent">
					<xsl:for-each select="depthdn[normalize-space(.) != '']">
						<div class="md"><b>Depth datum name: </b><xsl:value-of select="."/></div>
					</xsl:for-each>
					<xsl:for-each select="depthres[normalize-space(.) != '']">
						<div class="md"><b>Depth resolution: </b><xsl:value-of select="."/></div>
					</xsl:for-each>
					<xsl:for-each select="depthdu[normalize-space(.) != '']">
						<div class="md"><b>Depth distance units: </b><xsl:value-of select="."/></div>
					</xsl:for-each>
					<xsl:for-each select="depthem[normalize-space(.) != '']">
						<div class="md"><b>Depth encoding method: </b><xsl:value-of select="."/></div>
					</xsl:for-each>
				</div>
			</xsl:for-each>
		</div>
	</xsl:for-each>
</xsl:template>

<!-- Map Projections -->

<!-- Projections explicitly supported in the FGDC standard -->
<xsl:template match="albers | azimequi | equicon | equirect | gnomonic | gvnsp | lamberta | 
    lambertc | mercator | miller | modsak | obqmerc | orthogr | polarst | polycon | robinson | 
    sinusoid | spaceobq | stereo | transmer | vdgrin">
  <xsl:apply-templates select="*"/>
</xsl:template>

<!-- Projections defined in the 8.0 ESRI Profile -->
<xsl:template match="behrmann | bonne | cassini | eckert1 | eckert2 | eckert3 | eckert4 | 
    eckert5 | eckert6 | gallster | loximuth | mollweid | quartic | winkel1 | winkel2">
  <xsl:apply-templates select="*"/>
</xsl:template>

<!-- For projections not explicitly supported, FGDC standard places parameters in mapprojp; used by Catalog at 8.1 -->
<xsl:template match="mapprojp">
  <xsl:apply-templates select="*"/>
</xsl:template>

<!-- Map Projection Parameters -->

<xsl:template match="mapprojn[normalize-space(.) != '']">
	<div class="md"><b>Map projection name: </b><xsl:value-of select="."/></div>
</xsl:template>

<xsl:template match="stdparll[normalize-space(.) != '']">
	<div class="md-indent"><b>Standard parallel: </b><xsl:value-of select="."/></div>
</xsl:template>

<xsl:template match="longcm[normalize-space(.) != '']">
	<div class="md-indent"><b>Longitude of central meridian: </b><xsl:value-of select="."/></div>
</xsl:template>

<xsl:template match="latprjo[normalize-space(.) != '']">
	<div class="md-indent"><b>Latitude of projection origin: </b><xsl:value-of select="."/></div>
</xsl:template>

<xsl:template match="feast[normalize-space(.) != '']">
	<div class="md-indent"><b>False easting: </b><xsl:value-of select="."/></div>
</xsl:template>

<xsl:template match="fnorth[normalize-space(.) != '']">
	<div class="md-indent"><b>False northing: </b><xsl:value-of select="."/></div>
</xsl:template>

<xsl:template match="sfequat[normalize-space(.) != '']">
	<div class="md-indent"><b>Scale factor at equator: </b><xsl:value-of select="."/></div>
</xsl:template>

<xsl:template match="heightpt[normalize-space(.) != '']">
	<div class="md-indent"><b>Height of perspective point above surface: </b><xsl:value-of select="."/></div>
</xsl:template>

<xsl:template match="longpc[normalize-space(.) != '']">
	<div class="md-indent"><b>Longitude of projection center: </b><xsl:value-of select="."/></div>
</xsl:template>

<xsl:template match="latprjc[normalize-space(.) != '']">
	<div class="md-indent"><b>Latitude of projection center: </b><xsl:value-of select="."/></div>
</xsl:template>

<xsl:template match="sfctrlin[normalize-space(.) != '']">
	<div class="md-indent"><b>Scale factor at center line: </b><xsl:value-of select="."/></div>
</xsl:template>

<xsl:template match="obqlazim[normalize-space(.) != '']">
	<div class="md-indent"><b>Oblique line azimuth: </b></div>
	<div class="md-indent">
		<xsl:for-each select="azimangl[normalize-space(.) != '']">
			<div class="md"><b>Azimuthal angle: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
		<xsl:for-each select="azimptl[normalize-space(.) != '']">
			<div class="md"><b>Azimuthal measure point longitude: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
	</div>
</xsl:template>

<xsl:template match="obqlpt[normalize-space(.) != '']">
	<div class="md-indent"><b>Oblique line point: </b></div>
	<div class="md-indent">
		<xsl:for-each select="obqllat[normalize-space(.) != '']">
			<div class="md"><b>Oblique line latitude: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
		<xsl:for-each select="obqllong[normalize-space(.) != '']">
			<div class="md"><b>Oblique line longitude: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
	</div>
</xsl:template>

<xsl:template match="svlong[normalize-space(.) != '']">
	<div class="md-indent"><b>Straight vertical longitude from pole: </b><xsl:value-of select="."/></div>
</xsl:template>

<xsl:template match="sfprjorg[normalize-space(.) != '']">
	<div class="md-indent"><b>Scale factor at projection origin: </b><xsl:value-of select="."/></div>
</xsl:template>

<xsl:template match="landsat[normalize-space(.) != '']">
	<div class="md-indent"><b>Landsat number: </b><xsl:value-of select="."/></div>
</xsl:template>

<xsl:template match="pathnum[normalize-space(.) != '']">
	<div class="md-indent"><b>Path number: </b><xsl:value-of select="."/></div>
</xsl:template>

<xsl:template match="sfctrmer[normalize-space(.) != '']">
	<div class="md-indent"><b>Scale factor at central meridian: </b><xsl:value-of select="."/></div>
</xsl:template>

<xsl:template match="otherprj[normalize-space(.) != '']">
	<div class="md-indent"><b>Other projection's definition: </b><xsl:value-of select="."/></div>
</xsl:template>

<!-- SUPPORTING TEMPLATES -->

<!-- Time Period info -->
<xsl:template name="time_info">
		<xsl:for-each select="timeinfo[sngdate[normalize-space(.) != ''] or mdattim[normalize-space(.) != ''] or rngdates[normalize-space(.) != ''] or current[normalize-space(.) != '']]">
			<!-- Single Date/Time -->
			<xsl:for-each select="sngdate[normalize-space(.) != '']">
				<xsl:if test="caldate[normalize-space(.) != '']">
					<div class="md"><b>Date: </b><xsl:value-of select="caldate"/>
						<xsl:if test="time[normalize-space(.) != '']"> <b> Time: </b><xsl:value-of select="time"/></xsl:if>
					</div>
				</xsl:if>
				<!-- <xsl:for-each select="caldate[normalize-space(.) != '']">
					<div class="md"><b>Date: </b><xsl:value-of select="."/></div>
				</xsl:for-each>
				<xsl:for-each select="time[normalize-space(.) != '']">
					<div class="md"><b>Time: </b><xsl:value-of select="."/></div>
				</xsl:for-each> -->
				<!-- Start Biological Data Profile element -->
    				<xsl:apply-templates select="geolage"/>
				<!-- End Biological Data Profile element -->
			</xsl:for-each>	
			<!-- Multiple Date/Time -->
			<xsl:for-each select="mdattim[normalize-space(.) != '']">		
				<xsl:for-each select="sngdate[normalize-space(.) != '']">
			 	<xsl:if test="caldate[normalize-space(.) != '']">
					<div class="md"><b>Date: </b><xsl:value-of select="caldate"/>
						<xsl:if test="time[normalize-space(.) != '']"> <b> Time: </b><xsl:value-of select="time"/></xsl:if>
					</div>
				</xsl:if>			
				<!-- <div class="md">
						<xsl:for-each select="caldate[normalize-space(.) != '']">
							<b>Date: </b><xsl:value-of select="."/>
						</xsl:for-each>
						<xsl:for-each select="time[normalize-space(.) != '']">
							<b> Time: </b><xsl:value-of select="."/>
						</xsl:for-each>
					</div> -->
				</xsl:for-each>
			</xsl:for-each>
			<!-- Range of Dates/Times -->
			<xsl:for-each select="rngdates[normalize-space(.) != '']">
				<xsl:if test="begdate[normalize-space(.) != '']">
					<div class="md"><b>Beginning date: </b><xsl:value-of select="begdate"/>
						<xsl:if test="begtime[normalize-space(.) != '']"> <b> Beginning time: </b><xsl:value-of select="begtime"/></xsl:if>
					</div>
				</xsl:if>
				<xsl:if test="enddate[normalize-space(.) != '']">
					<div class="md"><b>Ending date: </b><xsl:value-of select="enddate"/>
						<xsl:if test="endtime[normalize-space(.) != '']"> <b> Ending time: </b><xsl:value-of select="endtime"/></xsl:if>
					</div>
				</xsl:if>
				<!-- <xsl:for-each select="begdate[normalize-space(.) != '']">
					<div class="md"><b>Beginning date: </b><xsl:value-of select="."/></div>
				</xsl:for-each>		
				<xsl:for-each select="begtime[normalize-space(.) != '']">
					<div class="md"><b>Beginning time: </b><xsl:value-of select="."/></div>
				</xsl:for-each>
				<xsl:for-each select="enddate[normalize-space(.) != '']">
					<div class="md"><b>Ending date: </b><xsl:value-of select="."/></div>
				</xsl:for-each>	
				<xsl:for-each select="endtime[normalize-space(.) != '']">
					<div class="md"><b>Ending time: </b><xsl:value-of select="."/></div>
				</xsl:for-each> -->
				<!-- Start Biological Data Profile element -->
				<xsl:apply-templates select="beggeol"/>
				<xsl:apply-templates select="endgeol"/>
				<!-- End Biological Data Profile element -->
			</xsl:for-each>
		</xsl:for-each>
		<xsl:for-each select="current[normalize-space(.) != '']">
			<div class="md"><b>Currentness reference: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>		
		</xsl:for-each>
</xsl:template>

<!-- Citation and Larger Work Citation info -->
<xsl:template name="citation_info">
	<xsl:for-each select="title[normalize-space(.) != '']">	
		<div class="md"><b>Title: </b><xsl:value-of select="."/></div>
	</xsl:for-each>
	<xsl:for-each select="origin[normalize-space(.) != '']">
		<xsl:choose>
			<xsl:when test="position() = 1">
				<div class="md"><b>Originators: </b><xsl:value-of select="."/></div>
			</xsl:when>
			<xsl:otherwise>
				<div class="md"><xsl:value-of select="."/></div>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:for-each>
	<xsl:for-each select="serinfo">
		<xsl:for-each select="sername[normalize-space(.) != '']">
			<div class="md"><b>Series name: </b><xsl:value-of select="."/></div>
		</xsl:for-each>	
		<xsl:for-each select="issue[normalize-space(.) != '']">
			<div class="md"><b>Series identification: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
	</xsl:for-each>
	<xsl:for-each select="pubinfo">
		<xsl:for-each select="publish[normalize-space(.) != '']">				
			<div class="md"><b>Publisher: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
		<xsl:for-each select="pubplace[normalize-space(.) != '']">		
			<div class="md"><b>Publication place: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
	</xsl:for-each>
	<xsl:if test="pubdate[normalize-space(.) != '']">
		<div class="md"><b>Publication date: </b><xsl:value-of select="pubdate"/>
			<xsl:if test="pubtime[normalize-space(.) != '']"> <b> Publication time: </b><xsl:value-of select="pubtime"/></xsl:if>
		</div>
	</xsl:if>
	<!-- <xsl:for-each select="pubdate[normalize-space(.) != '']">
		<div class="md"><b>Publication date: </b><xsl:value-of select="."/></div>
	</xsl:for-each>
	<xsl:for-each select="pubtime[normalize-space(.) != '']">
		<div class="md"><b>Publication time: </b><xsl:value-of select="."/></div>
	</xsl:for-each>	-->
	<xsl:for-each select="edition[normalize-space(.) != '']">
		<div class="md"><b>Edition: </b><xsl:value-of select="."/></div>
	</xsl:for-each>
	<xsl:for-each select="geoform[normalize-space(.) != '']">
		<div class="md"><b>Data type: </b><xsl:value-of select="."/></div>
	</xsl:for-each>
	<div class="md">
		<xsl:for-each select="onlink[normalize-space(.) != '']">
			<xsl:choose>
				<xsl:when test="position() = 1">
					<b>Data location: </b><a target="viewer"><xsl:attribute name="HREF"><xsl:value-of select="."/></xsl:attribute><xsl:value-of select="."/></a>
				</xsl:when>
				<xsl:otherwise>
					<xsl:text>, </xsl:text><a target="viewer"><xsl:attribute name="HREF"><xsl:value-of select="."/></xsl:attribute><xsl:value-of select="."/></a>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:for-each>
	</div>
	<xsl:for-each select="othercit[normalize-space(.) != '']">
		<div class="md"><b>Other citation details: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
	</xsl:for-each>
	<!-- Larger Work Citation -->
	<xsl:for-each select="lworkcit/citeinfo[normalize-space(.) != '']">
		<div class="md-item">Larger Work Citation</div>
		<div class="md-itemhide">
			<xsl:call-template name="citation_info"/>
		</div>
	</xsl:for-each>
</xsl:template>

<!-- Contact info-->
<xsl:template name="contact_info">
	<xsl:for-each select="cntorgp">
		<xsl:for-each select="cntorg[normalize-space(.) != '']">
			<div class="md"><b>Organization: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
		<xsl:for-each select="cntper[normalize-space(.) != '']">
			<div class="md"><b>Person: </b><xsl:value-of select="."/></div>
		</xsl:for-each>					
	</xsl:for-each>
	<xsl:for-each select="cntperp">
		<xsl:for-each select="cntper[normalize-space(.) != '']">
			<div class="md"><b>Person: </b><xsl:value-of select="."/></div>
		</xsl:for-each>					
		<xsl:for-each select="cntorg[normalize-space(.) != '']">
			<div class="md"><b>Organization: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
	</xsl:for-each>
	<xsl:for-each select="cntpos[normalize-space(.) != '']">
		<div class="md"><b>Position: </b><xsl:value-of select="."/></div>
	</xsl:for-each>
	<xsl:for-each select="cntvoice[normalize-space(.) != '']">				
		<div class="md"><b>Phone: </b><xsl:value-of select="."/></div>
	</xsl:for-each>
	<xsl:for-each select="cntfax[normalize-space(.) != '']">
		<div class="md"><b>Fax: </b><xsl:value-of select="."/></div>
	</xsl:for-each>
	<xsl:for-each select="cnttdd[normalize-space(.) != '']">
		<div class="md"><b>Telecommunications Device or Teletypewriter (TDD/TTY) phone: </b><xsl:value-of select="."/></div>
	</xsl:for-each>
	<xsl:for-each select="cntemail[normalize-space(.) != '']">
		<div class="md"><b>Email: </b><xsl:value-of select="."/></div>
	</xsl:for-each>
	<xsl:for-each select="hours[normalize-space(.) != '']">
		<div class="md"><b>Hours of service: </b><xsl:value-of select="."/></div>
	</xsl:for-each>
	<xsl:for-each select="cntinst[normalize-space(.) != '']">
		<div class="md"><b>Instructions: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
	</xsl:for-each>
	<xsl:for-each select="cntaddr">	
		<xsl:for-each select="addrtype[normalize-space(.) != '']">
			<div class="md"><b>Address type: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
		<xsl:if test="address[normalize-space(.) != ''] or city[normalize-space(.) != ''] or state[normalize-space(.) != ''] or postal[normalize-space(.) != ''] or country[normalize-space(.) != '']">
			<div class="md-indent">
				<xsl:for-each select="address[normalize-space(.) != '']">
					<div class="md"><b>Address: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
				</xsl:for-each>
				<xsl:for-each select="city[normalize-space(.) != '']">
					<div class="md"><b>City: </b><xsl:value-of select="."/></div>
				</xsl:for-each>
				<xsl:for-each select="state[normalize-space(.) != '']">
					<div class="md"><b>State or Province: </b><xsl:value-of select="."/></div>
				</xsl:for-each>
				<xsl:for-each select="postal[normalize-space(.) != '']">
					<div class="md"><b>Postal code: </b><xsl:value-of select="."/></div>
				</xsl:for-each>
				<xsl:for-each select="country[normalize-space(.) != '']">
					<div class="md"><b>Country: </b><xsl:value-of select="."/></div>
				</xsl:for-each>
			</div>
		</xsl:if>
	</xsl:for-each>
</xsl:template>

<!-- G-Ring Point Coordinates -->
<xsl:template name="identification_data_set_g_polygon_point_info">
	<table class="md-grid">
		<tr><th>Point</th><th>Longitude</th><th>Latitude</th></tr>
			<xsl:for-each select="grngpoin[normalize-space(.) != '']">>
				<tr>
					<td><xsl:value-of select="position()"/></td>							
					<xsl:choose>
						<xsl:when test="gringlat[normalize-space(.) != '']">
							<xsl:for-each select="gringlat[normalize-space(.) != '']">
								<td><xsl:value-of select="."/></td>
							</xsl:for-each>
						</xsl:when>
						<xsl:otherwise>
							<td>(not provided)</td>
						</xsl:otherwise>
					</xsl:choose>
					<xsl:choose>
					<xsl:when test="gringlon[normalize-space(.) != '']">
						<xsl:for-each select="gringlon[normalize-space(.) != '']">
							<td><xsl:value-of select="."/></td>
						</xsl:for-each>
					</xsl:when>
					<xsl:otherwise>
						<td>(not provided)</td>
					</xsl:otherwise>
				</xsl:choose>
			</tr>
		</xsl:for-each>									
	</table>
</xsl:template>

<!-- Data source info -->
<xsl:template name="data_source_info">
	<xsl:choose>
		<xsl:when test="srccitea[normalize-space(.) != '']">
			<div class="md-item"><xsl:value-of select="srccitea"/></div>
		</xsl:when>
		
	</xsl:choose>
	<div class="md-itemhide">
		<xsl:for-each select="srccite/citeinfo[normalize-space(.) != '']">
			<xsl:call-template name="citation_info"/>
		</xsl:for-each>
		<xsl:for-each select="srcscale[normalize-space(.) != '']">
			<div class="md"><b>Map scale denominator: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
		<xsl:for-each select="typesrc[normalize-space(.) != '']">
			<div class="md"><b>Media: </b><xsl:value-of select="."/></div>
		</xsl:for-each>
		<xsl:for-each select="srccontr[normalize-space(.) != '']">
			<div class="md"><b>Source contribution: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>
		</xsl:for-each>
		<xsl:for-each select="srctime[normalize-space(.) != '']">
			<xsl:call-template name="time_info"/>
			<xsl:for-each select="srccurr[normalize-space(.) != '']">
				<div class="md"><b>Currentness reference: </b><pre id="fixvalue"><xsl:value-of select="."/></pre></div>		
			</xsl:for-each>
		</xsl:for-each>
	</div>
</xsl:template>





</xsl:stylesheet>
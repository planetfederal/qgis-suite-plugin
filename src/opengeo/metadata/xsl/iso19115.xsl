<?xml version="1.0" encoding="UTF-8"?>

<!-- 
ISO 19139 default stylesheet
Based on metadata-iso19139.xsl from exCat
http://gdsc.nlr.nl/gdsc/en/tools/excat

/***************************************************************************
 Metadata browser/editor
                             
        begin                : 2011-02-21
        copyright            : (C) 2011 by NextGIS
        email                : info@nextgis.ru
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 <xsl:output method="html" encoding="ISO-8859-1"/>	 
-->

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
         xmlns:gco="http://www.isotc211.org/2005/gco"
         xmlns:gmd="http://www.isotc211.org/2005/gmd"
         >
<xsl:output method="html" encoding="UTF-8"/>

<xsl:template name="tablerow" >
    <xsl:param name="cname"/>
    <xsl:param name="cvalue"/>
    <xsl:choose>
      <xsl:when test="string($cvalue)">
        <tr>
          <td class="meta-param">
            <xsl:value-of select="$cname"/>
            <xsl:text>: </xsl:text>
          </td>
          <td class="meta-value">
            <xsl:value-of select="$cvalue"/>
          </td>
        </tr>
      </xsl:when>
      <xsl:otherwise>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  
<xsl:template match="gmd:MD_Metadata">
   
<!-- Metadata block -->
 
 <html>
   <head>
   	 <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
  	 <style type="text/css">
 	.captioneddiv { margin: 2em 0em 0em 0em;
    				padding: 1em;
				    height:auto;
    				border: solid #2A669D 1px;
					background: #ffffff; }
	.captioneddiv h3 { position: relative;
    				   margin: 0.5em;
					   top: -2.0em;
					   left: -1.0em;
					   padding: 0em 0.5em;
					   display: inline;
					   font-size: 0.9em;
					   /*background: #cae1ff;*/
					   background: #ffffff; }					
	.meta { vertical-align: top; }
	.meta-param { vertical-align: top; color: #004393 }
	.meta-value { vertical-align: top;}
	</style>
   </head>
   <body>
<div class="captioneddiv">
<h3>Metadata</h3>
<table class="meta"><tr></tr>
      <xsl:call-template name="tablerow">
      <xsl:with-param name="cname" select="'File Identifier'"/>
      <xsl:with-param name="cvalue" select="./gmd:fileIdentifier/gco:CharacterString"/>
      </xsl:call-template>
      <xsl:call-template name="tablerow">
      <xsl:with-param name="cname" select="'Language'"/>
      <xsl:with-param name="cvalue" select="./gmd:language/gco:CharacterString"/>
      </xsl:call-template>
      <xsl:call-template name="tablerow">
      <xsl:with-param name="cname" select="'Character set'"/>
      <xsl:with-param name="cvalue" select="./gmd:characterSet/gmd:MD_CharacterSetCode/@codeListValue"/>
      </xsl:call-template>
      <xsl:call-template name="tablerow">
      <xsl:with-param name="cname" select="'Date stamp'"/>
      <xsl:with-param name="cvalue" select="./gmd:dateStamp/gco:Date"/>
      </xsl:call-template>
      <xsl:call-template name="tablerow">
      <xsl:with-param name="cname" select="'Metadata standard name'"/>
      <xsl:with-param name="cvalue" select="./gmd:metadataStandardName/gco:CharacterString"/>
      </xsl:call-template>
      <xsl:call-template name="tablerow">
      <xsl:with-param name="cname" select="'Metadata standard version'"/>
      <xsl:with-param name="cvalue" select="./gmd:metadataStandardVersion/gco:CharacterString"/>
      </xsl:call-template>
</table>
 
<xsl:apply-templates select="./gmd:contact"/>
</div> 

<!-- Identification block -->
<xsl:apply-templates select="./gmd:identificationInfo/gmd:MD_DataIdentification"/>

<!--  Distribution -->
<xsl:apply-templates select="./gmd:distributionInfo/gmd:MD_Distribution"/>

<!-- ContentInfo -->
<xsl:apply-templates select="./gmd:contentInfo"/>

<!--  DataQuality -->
<xsl:apply-templates select="./gmd:dataQualityInfo/gmd:DQ_DataQuality"/>
  		
   </body>
 </html>
</xsl:template>


<!-- 'Metadata->Metadata author' block -->
<xsl:template match="gmd:contact">
<div class="captioneddiv">
<h3>Metadata author</h3>
<table class="meta">
<tr>
<td class="meta" valign="top">
<table class="meta"><tr></tr>
      <xsl:call-template name="tablerow">
      <xsl:with-param name="cname" select="'Individual name'"/>
      <xsl:with-param name="cvalue" select="./gmd:CI_ResponsibleParty/gmd:individualName/gco:CharacterString"/>
      </xsl:call-template>
      <xsl:call-template name="tablerow">
      <xsl:with-param name="cname" select="'Organisation name'"/>
      <xsl:with-param name="cvalue" select="./gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString"/>
      </xsl:call-template>
      <xsl:call-template name="tablerow">
      <xsl:with-param name="cname" select="'Position'"/>
      <xsl:with-param name="cvalue" select="./gmd:CI_ResponsibleParty/gmd:positionName/gco:CharacterString"/>
      </xsl:call-template>
      <xsl:call-template name="tablerow">
      <xsl:with-param name="cname" select="'Role'"/>
      <xsl:with-param name="cvalue" select="./gmd:CI_ResponsibleParty/gmd:role/gmd:CI_RoleCode/@codeListValue"/>
      </xsl:call-template>
</table></td>
<td class="meta" valign="top">
<table class="meta"><tr></tr>
      <xsl:call-template name="tablerow">
      <xsl:with-param name="cname" select="'Voice'"/>
      <xsl:with-param name="cvalue" select="./gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:voice/gco:CharacterString"/>
      </xsl:call-template>
      <xsl:call-template name="tablerow">
      <xsl:with-param name="cname" select="'Facsimile'"/>
      <xsl:with-param name="cvalue" select="./gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:facsimile/gco:CharacterString"/>
      </xsl:call-template>
      <xsl:call-template name="tablerow">
      <xsl:with-param name="cname" select="'Delivery Point'"/>
      <xsl:with-param name="cvalue" select="./gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:deliveryPoint/gco:CharacterString"/>
      </xsl:call-template>
      <xsl:call-template name="tablerow">
      <xsl:with-param name="cname" select="'City'"/>
      <xsl:with-param name="cvalue" select="./gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:city/gco:CharacterString"/>
      </xsl:call-template>
      <xsl:call-template name="tablerow">
      <xsl:with-param name="cname" select="'Postal code'"/>
      <xsl:with-param name="cvalue" select="./gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:postalCode/gco:CharacterString"/>
      </xsl:call-template>
      <xsl:call-template name="tablerow">
      <xsl:with-param name="cname" select="'Country'"/>
      <xsl:with-param name="cvalue" select="./gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:country/gco:CharacterString"/>
      </xsl:call-template>
      <xsl:call-template name="tablerow">
      <xsl:with-param name="cname" select="'Email'"/>
      <xsl:with-param name="cvalue" select="./gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString"/>
      </xsl:call-template>
</table></td>
</tr>
</table>
</div>
</xsl:template>


<!-- 'Identification' block -->
<xsl:template match="gmd:MD_DataIdentification">
<div class="captioneddiv">
<h3>Identification info</h3>
<table class="meta"><tr></tr>
      <xsl:call-template name="tablerow">
      <xsl:with-param name="cname" select="'Title'"/>
      <xsl:with-param name="cvalue" select="./gmd:citation/gmd:CI_Citation/gmd:title/gco:CharacterString"/>
      </xsl:call-template>
      <xsl:call-template name="tablerow">
      <xsl:with-param name="cname" select="'Date'"/>
      <xsl:with-param name="cvalue" select="./gmd:citation/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:data/gco:Date"/>
      </xsl:call-template>
      <!--xsl:call-template name="tablerow">
      <xsl:with-param name="cname" select="'Presentation form'"/>
      <xsl:with-param name="cvalue" select="./idCitation/presForm/PresFormCd/@value"/>
      </xsl:call-template-->
      <xsl:call-template name="tablerow">
      <xsl:with-param name="cname" select="'Individual name'"/>
      <xsl:with-param name="cvalue" select="./gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:individualName/gco:CharacterString"/>
      </xsl:call-template>
      <xsl:call-template name="tablerow">
      <xsl:with-param name="cname" select="'Organisation name'"/>
      <xsl:with-param name="cvalue" select="./gmd:pointOfContact/gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString"/>
      </xsl:call-template>

      <!--abstract is handled seperately because of text formatting-->
      <tr>
      <td class="meta-param">Abstract:</td>
      <td class="meta-value">
      <xsl:apply-templates select="./gmd:abstract"/>
      </td>
      </tr>
      
      <!-- Keywords  -->
      <xsl:choose>
      <xsl:when test="./gmd:descriptiveKeywords/gmd:MD_Keywords/gmd:keyword">
      <tr>
      <td class="meta-param">Keywords:</td>
        <td class="meta-value">
            <xsl:apply-templates select="./gmd:descriptiveKeywords/gmd:MD_Keywords/gmd:keyword"/>
        </td>
      </tr>  
      </xsl:when>
      <xsl:otherwise>
      </xsl:otherwise>
    </xsl:choose>
      
     <!--  Spatial repres --> 
      <xsl:call-template name="tablerow">
      <xsl:with-param name="cname" select="'Spatial representation type'"/>
      <xsl:with-param name="cvalue" select="./gmd:spatialRepresentationType/gmd:MD_SpatialRepresentationTypeCode"/>
      </xsl:call-template>
      
      <!-- Spatial scale -->
      <xsl:choose>
      <xsl:when test="./gmd:spatialResolution/gmd:MD_Resolution/gmd:equivalentScale/gmd:MD_RepresentativeFraction/gmd:denominator/gco:Integer">
      <tr>
      <td class="meta-param">Spatial scale:</td>
        <td class="meta-value">
            1:<xsl:apply-templates select="./gmd:spatialResolution/gmd:MD_Resolution/gmd:equivalentScale/gmd:MD_RepresentativeFraction/gmd:denominator/gco:Integer"/>
        </td>
      </tr>  
      </xsl:when>
          <xsl:otherwise>
        </xsl:otherwise>
      </xsl:choose>
      
      <!-- Spatial accuracy -->
      <xsl:choose>
      <xsl:when test="./gmd:spatialResolution/gmd:MD_Resolution/gmd:distance/gco:Distance">
      <tr>
      <td class="meta-param">Spatial accuracy:</td>
        <td class="meta-value">
            <xsl:apply-templates select="./gmd:spatialResolution/gmd:MD_Resolution/gmd:distance/gco:Distance"/>
            <xsl:apply-templates select="./gmd:spatialResolution/gmd:MD_Resolution/gmd:distance/gco:Distance/@uom"/>
        </td>
      </tr>  
      </xsl:when>
          <xsl:otherwise>
        </xsl:otherwise>
      </xsl:choose>
      
     
      
</table>
            <!-- License info block -->
            <xsl:apply-templates select="./gmd:resourceConstraints/gmd:MD_LegalConstraints"/>
            <xsl:apply-templates select="./gmd:extent"/>
            <xsl:apply-templates select="./gmd:pointOfContact"/>
</div>

</xsl:template>

<!-- 'dataQualityInfo block -->
<xsl:template match="gmd:DQ_DataQuality">
<div class="captioneddiv">
<h3>Data quality info</h3>
<table class="meta"><tr></tr>
        <xsl:call-template name="tablerow">
            <xsl:with-param name="cname" select="'Scope'"/>
            <xsl:with-param name="cvalue" select="./gmd:scope/gmd:DQ_Scope/gmd:level/gmd:MD_ScopeCode"/>
        </xsl:call-template>
        <xsl:call-template name="tablerow">
            <xsl:with-param name="cname" select="'Statement'"/>
            <xsl:with-param name="cvalue" select="./gmd:lineage/gmd:LI_Lineage/gmd:statement/gco:CharacterString"/>
        </xsl:call-template>
        <xsl:call-template name="tablerow">
            <xsl:with-param name="cname" select="'Process info'"/>
            <xsl:with-param name="cvalue" select="./gmd:lineage/gmd:LI_Lineage/gmd:processStep/gmd:LI_ProcessStep/gmd:description/gco:CharacterString"/>
        </xsl:call-template>

</table>
</div>

</xsl:template>
 

<!-- 'dataQualityInfo block -->
<xsl:template match="gmd:contentInfo">
<div class="captioneddiv">
<h3>Content information</h3>
    <!-- Raster info -->
    <xsl:apply-templates select="./gmd:MD_ImageDescription"/>
    <!-- Vector info -->
</div>
</xsl:template>

<xsl:template match="gmd:MD_ImageDescription">
<table class="meta"><tr></tr>
    <xsl:call-template name="tablerow">
      <xsl:with-param name="cname" select="'Content type'"/>
      <xsl:with-param name="cvalue" select="./gmd:contentType/gmd:MD_CoverageContentTypeCode"/>
    </xsl:call-template>
    
    <xsl:choose>
      <xsl:when test="./gmd:dimension/gmd:MD_Band">
      <tr>
      <td class="meta-param">Bands:</td>
        <td class="meta-value">    
            <xsl:apply-templates select="./gmd:dimension/gmd:MD_Band"/>
        </td>   
      </tr>  
      </xsl:when>
          <xsl:otherwise>
        </xsl:otherwise>
      </xsl:choose>

</table>
</xsl:template>


<!-- Band info -->
<xsl:template match="gmd:MD_Band">
<div class="captioneddiv">
<table >
          <xsl:call-template name="tablerow">
          <xsl:with-param name="cname" select="'Min value'"/>
          <xsl:with-param name="cvalue" select="./gmd:minValue/gco:Real"/>
          </xsl:call-template>

          <xsl:call-template name="tablerow">
          <xsl:with-param name="cname" select="'Max value'"/>
          <xsl:with-param name="cvalue" select="./gmd:maxValue/gco:Real"/>
          </xsl:call-template>
          
          <xsl:call-template name="tablerow">
          <xsl:with-param name="cname" select="'Bits per value'"/>
          <xsl:with-param name="cvalue" select="./gmd:bitsPerValue/gco:Integer"/>
          </xsl:call-template>              
</table> 
</div>
</xsl:template>
 

 <!-- 'License info' block -->
  <xsl:template match="gmd:MD_LegalConstraints">
  	<xsl:if test="./gmd:useLimitation/gco:CharacterString">
      <div class="captioneddiv">
        <h3>Constraints</h3>
        <table class="meta"><tr></tr>
        <xsl:call-template name="tablerow">
      		<xsl:with-param name="cname" select="'Constraint type'"/>
      		<xsl:with-param name="cvalue" select="./gmd:useConstraints/gmd:MD_RestrictionCode"/>
      	</xsl:call-template>
      	<xsl:call-template name="tablerow">
      		<xsl:with-param name="cname" select="'Constraint text'"/>
      		<xsl:with-param name="cvalue" select="./gmd:useLimitation/gco:CharacterString"/>
      	</xsl:call-template>
      	</table>
      </div>
    </xsl:if>
  </xsl:template>

<!-- 'Identification->Point of Contact' block -->
<xsl:template match="gmd:pointOfContact">
    <div class="captioneddiv">
      <h3>Point of Contact</h3>
      <table class="meta">
        <tr>
          <td class="meta" valign="top">
            <table class="meta">
              <tr></tr>
              <xsl:call-template name="tablerow">
                <xsl:with-param name="cname" select="'Individual name'"/>
                <xsl:with-param name="cvalue" select="./gmd:CI_ResponsibleParty/gmd:individualName/gco:CharacterString"/>
              </xsl:call-template>
              <xsl:call-template name="tablerow">
                <xsl:with-param name="cname" select="'Organisation name'"/>
                <xsl:with-param name="cvalue" select="./gmd:CI_ResponsibleParty/gmd:organisationName/gco:CharacterString"/>
              </xsl:call-template>
              <xsl:call-template name="tablerow">
                <xsl:with-param name="cname" select="'Position'"/>
                <xsl:with-param name="cvalue" select="./gmd:CI_ResponsibleParty/gmd:positionName/gco:CharacterString"/>
              </xsl:call-template>
              <xsl:call-template name="tablerow">
                <xsl:with-param name="cname" select="'Role'"/>
                <xsl:with-param name="cvalue" select="./gmd:CI_ResponsibleParty/gmd:role/gmd:CI_RoleCode/@codeListValue"/>
              </xsl:call-template>
            </table>
          </td>
          <td class="meta" valign="top">
            <table class="meta">
              <tr></tr>
              <xsl:call-template name="tablerow">
                <xsl:with-param name="cname" select="'Voice'"/>
                <xsl:with-param name="cvalue" select="./gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:voice/gco:CharacterString"/>
              </xsl:call-template>
              <xsl:call-template name="tablerow">
                <xsl:with-param name="cname" select="'Facsimile'"/>
                <xsl:with-param name="cvalue" select="./gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:phone/gmd:CI_Telephone/gmd:facsimile/gco:CharacterString"/>
              </xsl:call-template>
              <xsl:call-template name="tablerow">
                <xsl:with-param name="cname" select="'Delivery Point'"/>
                <xsl:with-param name="cvalue" select="./gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:deliveryPoint/gco:CharacterString"/>
              </xsl:call-template>
              <xsl:call-template name="tablerow">
                <xsl:with-param name="cname" select="'City'"/>
                <xsl:with-param name="cvalue" select="./gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:city/gco:CharacterString"/>
              </xsl:call-template>
              <xsl:call-template name="tablerow">
                <xsl:with-param name="cname" select="'Postal code'"/>
                <xsl:with-param name="cvalue" select="./gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:postalCode/gco:CharacterString"/>
              </xsl:call-template>
              <xsl:call-template name="tablerow">
                <xsl:with-param name="cname" select="'Country'"/>
                <xsl:with-param name="cvalue" select="./gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:country/gco:CharacterString"/>
              </xsl:call-template>
              <xsl:call-template name="tablerow">
                <xsl:with-param name="cname" select="'Email'"/>
                <xsl:with-param name="cvalue" select="./gmd:CI_ResponsibleParty/gmd:contactInfo/gmd:CI_Contact/gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString"/>
              </xsl:call-template>
            </table>
          </td>
        </tr>
      </table>
    </div>
  </xsl:template>


  <!-- 'Identification->Geographic box' block -->
  <xsl:template match="gmd:extent">
    <xsl:if test="./gmd:EX_Extent/gmd:geographicElement">
      <div class="captioneddiv">
        <h3>Geographic box</h3>
        <br/>
        <table class="meta" width="100%" align="center">
          <tr></tr>
          <tr>
            <td></td>
            <td class="meta-param" align="center">
              North bound latitude<br/>
              <font color="#000000">
                <xsl:value-of select="./gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:northBoundLatitude/gco:Decimal"/>
              </font>
            </td>
            <td></td>
          </tr>
          <tr>
            <td class="meta-param" align="center">
              West bound longitude<br/>
              <font color="#000000">
                <xsl:value-of select="./gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:westBoundLongitude/gco:Decimal"/>
              </font>
            </td>
            <td></td>
            <td class="meta-param" align="center">
              East bound longitude<br/>
              <font color="#000000">
                <xsl:value-of select="./gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:eastBoundLongitude/gco:Decimal"/>
              </font>
            </td>
          </tr>
          <tr>
            <td></td>
            <td class="meta-param" align="center">
              South bound latitude<br/>
              <font color="#000000">
                <xsl:value-of select="./gmd:EX_Extent/gmd:geographicElement/gmd:EX_GeographicBoundingBox/gmd:southBoundLatitude/gco:Decimal"/>
              </font>
            </td>
            <td></td>
          </tr>
        </table>
      </div>
    </xsl:if>
  </xsl:template>
  
  <!-- 'Distribution Info' block -->
  <xsl:template match="gmd:MD_Distribution">
    <div class="captioneddiv">
      <h3>Distribution info</h3>
      <table class="meta">
        <tr></tr>
        <xsl:for-each select="gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine/gmd:CI_OnlineResource">
          <xsl:choose>
            <xsl:when test="starts-with(./gmd:protocol/gco:CharacterString,'WWW:DOWNLOAD-') and contains(./gmd:protocol/gco:CharacterString,'http--download') and ./gmd:name/gco:CharacterString">
              <tr>
                <td class="meta-param">Download:</td>
                <td class="meta-value">
                  <a>
                    <xsl:attribute name="href">
                      <xsl:value-of select="gmd:linkage/gmd:URL"/>
                    </xsl:attribute>
                    <xsl:value-of select="gmd:name/gco:CharacterString"/>
                  </a>
                </td>
              </tr>
            </xsl:when>
            <xsl:when test="starts-with(./gmd:protocol/gco:CharacterString,'ESRI:AIMS-') and contains(./gmd:protocol/gco:CharacterString,'-get-image') and ./gmd:name/gco:CharacterString">
              <tr>
                <td class="meta-param">Esri ArcIms:</td>
                <td class="meta-value">
                  <a>
                    <xsl:attribute name="href">
                      <xsl:value-of select="gmd:linkage/gmd:URL"/>
                    </xsl:attribute>
                    <xsl:value-of select="gmd:name/gco:CharacterString"/>
                  </a>
                </td>
              </tr>
            </xsl:when>
            <xsl:when test="starts-with(./gmd:protocol/gco:CharacterString,'OGC:WMS-') and contains(./gmd:protocol/gco:CharacterString,'-get-capabilities') and ./gmd:name/gco:CharacterString">
              <tr>
                <td class="meta-param">OGC-WMS Capabilities:</td>
                <td class="meta-value">
                  <a>
                    <xsl:attribute name="href">
                      <xsl:value-of select="gmd:linkage/gmd:URL"/>
                    </xsl:attribute>
                    <xsl:value-of select="gmd:name/gco:CharacterString"/>
                  </a>
                </td>
              </tr>
            </xsl:when>
          </xsl:choose>
        </xsl:for-each>
      </table>
    </div>
  </xsl:template>

</xsl:stylesheet>

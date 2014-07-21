<?xml version="1.0"?>
<!-- xsl:stylesheet xmlns:xsl="http://www.w3.org/TR/WD-xsl" -->

<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output encoding="ISO-8859-1"/>

<!-- An xsl template for displaying metadata in ArcInfo8 with the
     traditional FGDC look and feel created by mp
	
     Revision History: Created 6/7/99 avienneau
     	04/10/2001 IAAA, http://iaaa.cps.unizar.es
-->

<xsl:template match="/">
  <HTML>
  <BODY>

    <A name="Top"/>
    <H1><xsl:value-of select="metadata/idinfo/citation/citeinfo/title"/></H1>
    <H2>Metadata:</H2>

    <UL>
      <xsl:for-each select="metadata/idinfo">
        <LI><A HREF="#Identification_Information">Identification_Information</A></LI>
      </xsl:for-each>
      <xsl:for-each select="metadata/dataqual">
        <LI><A HREF="#Data_Quality_Information">Data_Quality_Information</A></LI>
      </xsl:for-each>
      <xsl:for-each select="metadata/spdoinfo">
        <LI><A HREF="#Spatial_Data_Organization_Information">Spatial_Data_Organization_Information</A></LI>
      </xsl:for-each>
      <xsl:for-each select="metadata/spref">
        <LI><A HREF="#Spatial_Reference_Information">Spatial_Reference_Information</A></LI>
      </xsl:for-each>
      <xsl:for-each select="metadata/eainfo">
        <LI><A HREF="#Entity_and_Attribute_Information">Entity_and_Attribute_Information</A></LI>
      </xsl:for-each>

<!--

      <xsl:for-each select="metadata/distinfo">

      <xsl:choose>
        <xsl:when test="context()[0]">
          <xsl:choose>
            <xsl:when test="context()[end()]">
              <LI>
                <A>
                  <xsl:attribute name="HREF">#<xsl:eval>uniqueID(this)</xsl:eval></xsl:attribute>
                  Distribution_Information
                </A>
              </LI>
            </xsl:when>

            <xsl:otherwise>
              <LI>Distribution_Information</LI>
              <LI STYLE="margin-left:0.3in">
                <A>
                  <xsl:attribute name="HREF">#<xsl:eval>uniqueID(this)</xsl:eval></xsl:attribute>
                  Distributor <xsl:eval>formatIndex(childNumber(this), "1")</xsl:eval>
                </A>
              </LI>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:when>

        <xsl:otherwise>
          <LI STYLE="margin-left:0.3in">
            <A>
              <xsl:attribute name="HREF">#<xsl:eval>uniqueID(this)</xsl:eval></xsl:attribute>
              Distributor <xsl:eval>formatIndex(childNumber(this), "1")</xsl:eval>
            </A>
          </LI>
        </xsl:otherwise>
      </xsl:choose>

      </xsl:for-each>

-->



      <xsl:for-each select="metadata/distinfo">

      <xsl:choose>
        <xsl:when test="position()=1">
          <xsl:choose>
            <xsl:when test="position()=last()">
              <LI>
<!--                <A>
                  <xsl:attribute name="HREF">#<xsl:eval>uniqueID(this)</xsl:eval></xsl:attribute>
                  Distribution_Information
                </A>
-->
		<A HREF="#{generate-id()}">Distribution_Information</A>

              </LI>
            </xsl:when>

            <xsl:otherwise>
              <LI>Distribution_Information</LI>
              <LI STYLE="margin-left:0.3in">
		<A HREF="#{generate-id()}">Distribution_Information</A>
              </LI>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:when>

        <xsl:otherwise>
          <LI STYLE="margin-left:0.3in">
            <A HREF="#{generate-id()}">Distribution_Information</A>
          </LI>
        </xsl:otherwise>
      </xsl:choose>

      </xsl:for-each>



      <xsl:for-each select="metadata/metainfo">
        <LI><A HREF="#Metadata_Reference_Information">Metadata_Reference_Information</A></LI>
      </xsl:for-each>
    </UL>

    <xsl:apply-templates select="metadata/idinfo"/>
    <xsl:apply-templates select="metadata/dataqual"/>
    <xsl:apply-templates select="metadata/spdoinfo"/>
    <xsl:apply-templates select="metadata/spref"/>
    <xsl:apply-templates select="metadata/eainfo"/>
    <xsl:apply-templates select="metadata/distinfo"/>
    <xsl:apply-templates select="metadata/metainfo"/>

  </BODY>
  </HTML>
</xsl:template>

<!-- Identification -->
<xsl:template match="idinfo">
  <A name="Identification_Information"><HR/></A>
  <DL>
    <DT><I>Identification_Information:</I></DT>
    <DD>
    <DL>
      <xsl:for-each select="citation">
        <DT><I>Citation:</I></DT>
        <DD>
        <DL>
          <xsl:apply-templates select="citeinfo"/>
        </DL>
        </DD>
      </xsl:for-each>

      <xsl:for-each select="descript">
        <DT><I>Description:</I></DT>
        <DD>
        <DL>
          <xsl:for-each select="abstract">
            <DT><I>Abstract:</I></DT>
            <DD><xsl:value-of select="."/></DD>      
          </xsl:for-each>

          <xsl:for-each select="purpose">
            <DT><I>Purpose:</I></DT>
            <DD><xsl:value-of select="."/></DD>
          </xsl:for-each>

          <xsl:for-each select="supplinf">
            <DT><I>Supplemental_Information:</I></DT>
            <DD><xsl:value-of select="."/></DD>
          </xsl:for-each>
        </DL>
        </DD>
      </xsl:for-each>

      <xsl:for-each select="timeperd">
        <DT><I>Time_Period_of_Content:</I></DT>
        <DD>
        <DL>
          <xsl:apply-templates select="timeinfo"/>
          <xsl:for-each select="current">
            <DT><I>Currentness_Reference:</I></DT>
            <DD><xsl:value-of select="."/></DD>
          </xsl:for-each>
        </DL>
        </DD>
      </xsl:for-each>

      <xsl:for-each select="status">
        <DT><I>Status:</I></DT>
        <DD>
        <DL>
          <xsl:for-each select="progress">
            <DT><I>Progress:</I> <xsl:value-of select="."/></DT>
          </xsl:for-each>
          <xsl:for-each select="update">
            <DT><I>Maintenance_and_Update_Frequency:</I> <xsl:value-of select="."/></DT>
          </xsl:for-each>
        </DL>
        </DD>
      </xsl:for-each>

      <xsl:for-each select="spdom">
        <DT><I>Spatial_Domain:</I></DT>
        <DD>
        <DL>
          <xsl:for-each select="bounding">
            <DT><I>Bounding_Coordinates:</I></DT>
            <DD>
            <DL>
              <DT><I>West_Bounding_Coordinate:</I> <xsl:value-of select="westbc"/></DT>
              <DT><I>East_Bounding_Coordinate:</I> <xsl:value-of select="eastbc"/></DT>
              <DT><I>North_Bounding_Coordinate:</I> <xsl:value-of select="northbc"/></DT>
              <DT><I>South_Bounding_Coordinate:</I> <xsl:value-of select="southbc"/></DT>
            </DL>
            </DD>
          </xsl:for-each>
          <xsl:for-each select="dsgpoly">
            <DT><I>Data_Set_G-Polygon:</I></DT>
            <DD>
            <DL>
              <xsl:for-each select="dsgpolyo">
                <DT><I>Data_Set_G-Polygon_Outer_G-Ring:</I></DT>
                <DD>
                <DL>
                  <xsl:apply-templates select="grngpoin"/>
                  <xsl:apply-templates select="gring"/>
                </DL>
                </DD>
              </xsl:for-each>
              <xsl:for-each select="dsgpolyx">
                <DT><I>Data_Set_G-Polygon_Exclusion_G-Ring:</I></DT>
                <DD>
                <DL>
                  <xsl:apply-templates select="grngpoin"/>
                  <xsl:apply-templates select="gring"/>
                </DL>
                </DD>
              </xsl:for-each>
            </DL>
            </DD>
          </xsl:for-each>
        </DL>
        </DD>
      </xsl:for-each>

      <xsl:for-each select="keywords">
        <DT><I>Keywords:</I></DT>
        <DD>
        <DL>
          <xsl:for-each select="theme">
            <DT><I>Theme:</I></DT>
            <DD>
            <DL>
              <xsl:for-each select="themekt">
                <DT><I>Theme_Keyword_Thesaurus:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
              <xsl:for-each select="themekey">
                <DT><I>Theme_Keyword:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
            </DL>
            </DD>
          </xsl:for-each>

          <xsl:for-each select="place">
            <DT><I>Place:</I></DT>
            <DD>
            <DL>
              <xsl:for-each select="placekt">
                <DT><I>Place_Keyword_Thesaurus:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
              <xsl:for-each select="placekey">
                <DT><I>Place_Keyword:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
            </DL>
            </DD>
          </xsl:for-each>

          <xsl:for-each select="stratum">
            <DT><I>Stratum:</I></DT>
            <DD>
            <DL>
              <xsl:for-each select="stratkt">
                <DT><I>Stratum_Keyword_Thesaurus:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
              <xsl:for-each select="stratkey">
                <DT><I>Stratum_Keyword:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
            </DL>
            </DD>
          </xsl:for-each>
 
          <xsl:for-each select="temporal">
            <DT><I>Temporal:</I></DT>
            <DD>
            <DL>
              <xsl:for-each select="tempkt">
                <DT><I>Temporal_Keyword_Thesaurus:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
              <xsl:for-each select="tempkey">
                <DT><I>Temporal_Keyword:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
            </DL>
            </DD>
          </xsl:for-each>
        </DL>
        </DD>
      </xsl:for-each>

      <xsl:for-each select="accconst">
        <DT><I>Access_Constraints:</I> <xsl:value-of select="."/></DT>
      </xsl:for-each>
      <xsl:for-each select="useconst">
        <DT><I>Use_Constraints:</I></DT>
        <DD><xsl:value-of select="."/></DD>
      </xsl:for-each>

      <xsl:for-each select="ptcontac">
        <DT><I>Point_of_Contact:</I></DT>
        <DD>
        <DL>
          <xsl:apply-templates select="cntinfo"/>
        </DL>
        </DD>
      </xsl:for-each>

      <xsl:for-each select="browse">
        <DT><I>Browse_Graphic:</I></DT>
        <DD>
        <DL>
          <xsl:for-each select="browsen">
            <DT><I>Browse_Graphic_File_Name:</I> <A TARGET="viewer">
              <xsl:attribute name="HREF"><xsl:value-of select="."/></xsl:attribute>
              <xsl:value-of select="."/></A>
            </DT>
          </xsl:for-each>
          <xsl:for-each select="browsed">
            <DT><I>Browse_Graphic_File_Description:</I></DT>
            <DD><xsl:value-of select="."/></DD>
          </xsl:for-each>
          <xsl:for-each select="browset">
            <DT><I>Browse_Graphic_File_Type:</I> <xsl:value-of select="."/></DT>
          </xsl:for-each>
        </DL>
        </DD>
      </xsl:for-each>

      <xsl:for-each select="datacred">
        <DT><I>Data_Set_Credit:</I></DT>
        <DD><xsl:value-of select="."/></DD>
      </xsl:for-each>

      <xsl:for-each select="secinfo">
        <DT><I>Security_Information:</I></DT>
        <DD>
        <DL>
          <xsl:for-each select="secsys">
            <DT><I>Security_Classification_System:</I> <xsl:value-of select="."/></DT>
          </xsl:for-each>
          <xsl:for-each select="secclass">
            <DT><I>Security_Classification:</I> <xsl:value-of select="."/></DT>
          </xsl:for-each>
          <xsl:for-each select="sechandl">
            <DT><I>Security_Handling_Description:</I> <xsl:value-of select="."/></DT>
          </xsl:for-each>
        </DL>
        </DD>
      </xsl:for-each>

      <xsl:for-each select="native">
        <DT><I>Native_Data_Set_Environment:</I></DT>
        <DD><xsl:value-of select="."/></DD>
      </xsl:for-each>

      <xsl:for-each select="crossref">
        <DT><I>Cross_Reference:</I></DT>
        <DD>
        <DL>
          <xsl:apply-templates select="citeinfo"/>
        </DL>
        </DD>
      </xsl:for-each>

    </DL>
    </DD>
  </DL>
  <A HREF="#Top">Back to Top</A>
</xsl:template>

<!-- Data Quality -->
<xsl:template match="dataqual">
  <A name="Data_Quality_Information"><HR/></A>
  <DL>
    <DT><I>Data_Quality_Information:</I></DT>
    <DD>
    <DL>
      <xsl:for-each select="attracc">
        <DT><I>Attribute_Accuracy:</I></DT>
        <DD>
        <DL>
          <xsl:for-each select="attraccr">
            <DT><I>Attribute_Accuracy_Report:</I></DT>
            <DD><xsl:value-of select="."/></DD>
          </xsl:for-each>
          <xsl:for-each select="qattracc">
            <DT><I>Quantitative_Attribute_Accuracy_Assessment:</I></DT>
            <DD>
            <DL>
              <xsl:for-each select="attraccv">
                <DT><I>Attribute_Accuracy_Value:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
              <xsl:for-each select="attracce">
                <DT><I>Attribute_Accuracy_Explanation:</I></DT>
                <DD><xsl:value-of select="."/></DD>
              </xsl:for-each>
            </DL>
            </DD>
          </xsl:for-each>
        </DL>
        </DD>
      </xsl:for-each>

      <xsl:for-each select="logic">
        <DT><I>Logical_Consistency_Report:</I></DT>
        <DD><xsl:value-of select="."/></DD>
      </xsl:for-each>
      <xsl:for-each select="complete">
        <DT><I>Completeness_Report:</I></DT>
        <DD><xsl:value-of select="."/></DD>
      </xsl:for-each>

      <xsl:for-each select="posacc">
        <DT><I>Positional_Accuracy:</I></DT>
        <DD>
        <DL>
          <xsl:for-each select="horizpa">
            <DT><I>Horizontal_Positional_Accuracy:</I></DT>
            <DD>
            <DL>
              <xsl:for-each select="horizpar">
                <DT><I>Horizontal_Positional_Accuracy_Report:</I></DT>
                <DD><xsl:value-of select="."/></DD>
              </xsl:for-each>
              <xsl:for-each select="qhorizpa">
                <DT><I>Quantitative_Horizontal_Positional_Accuracy_Assessment:</I></DT>
                <DD>
                <DL>
                  <xsl:for-each select="horizpav">
                    <DT><I>Horizontal_Positional_Accuracy_Value:</I> <xsl:value-of select="."/></DT>
                  </xsl:for-each>
                  <xsl:for-each select="horizpae">
                    <DT><I>Horizontal_Positional_Accuracy_Explanation:</I></DT>
                    <DD><xsl:value-of select="."/></DD>
                  </xsl:for-each>
                </DL>
                </DD>
              </xsl:for-each>
            </DL>
            </DD>
          </xsl:for-each>
          <xsl:for-each select="vertacc">
            <DT><I>Vertical_Positional_Accuracy:</I></DT>
            <DD>
            <DL>
              <xsl:for-each select="vertaccr">
                <DT><I>Vertical_Positional_Accuracy_Report:</I></DT>
                <DD><xsl:value-of select="."/></DD>
              </xsl:for-each>
              <xsl:for-each select="qvertpa">
                <DT><I>Quantitative_Vertical_Positional_Accuracy_Assessment:</I></DT>
                <DD>
                <DL>
                  <xsl:for-each select="vertaccv">
                    <DT><I>Vertical_Positional_Accuracy_Value:</I> <xsl:value-of select="."/></DT>
                  </xsl:for-each>
                  <xsl:for-each select="vertacce">
                    <DT><I>Vertical_Positional_Accuracy_Explanation:</I></DT>
                    <DD><xsl:value-of select="."/></DD>
                  </xsl:for-each>
                </DL>
                </DD>
              </xsl:for-each>
            </DL>
            </DD>
          </xsl:for-each>
        </DL>
        </DD>
      </xsl:for-each>

      <xsl:for-each select="lineage">
        <DT><I>Lineage:</I></DT>
        <DD>
        <DL>
          <xsl:for-each select="srcinfo">
            <DT><I>Source_Information:</I></DT>
            <DD>
            <DL>
              <xsl:for-each select="srccite">
                <DT><I>Source_Citation:</I></DT>
                <DD>
                <DL>
                  <xsl:apply-templates select="citeinfo"/>
                </DL>
                </DD>
              </xsl:for-each>
              <xsl:for-each select="srcscale">
                <DT><I>Source_Scale_Denominator:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
              <xsl:for-each select="typesrc">
                <DT><I>Type_of_Source_Media:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>

              <xsl:for-each select="srctime">
                <DT><I>Source_Time_Period_of_Content:</I></DT>
                <DD>
                <DL>
                  <xsl:apply-templates select="timeinfo"/>
                  <xsl:for-each select="srccurr">
                    <DT><I>Source_Currentness_Reference:</I></DT>
                    <DD><xsl:value-of select="."/></DD>
                  </xsl:for-each>
                </DL>
                </DD>
              </xsl:for-each>

              <xsl:for-each select="srccitea">
                <DT><I>Source_Citation_Abbreviation:</I></DT>
                <DD><xsl:value-of select="."/></DD>
              </xsl:for-each>
              <xsl:for-each select="srccontr">
                <DT><I>Source_Contribution:</I></DT>
                <DD><xsl:value-of select="."/></DD>
              </xsl:for-each>
            </DL>
            </DD>
          </xsl:for-each>

          <xsl:for-each select="procstep">
            <DT><I>Process_Step:</I></DT>
            <DD>
            <DL>
              <xsl:for-each select="procdesc">
                <DT><I>Process_Description:</I></DT>
                <DD><xsl:value-of select="."/></DD>
              </xsl:for-each>
              <xsl:for-each select="srcused">
                <DT><I>Source_Used_Citation_Abbreviation:</I></DT>
                <DD><xsl:value-of select="."/></DD>
              </xsl:for-each>
              <xsl:for-each select="procdate">
                <DT><I>Process_Date:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
              <xsl:for-each select="proctime">
                <DT><I>Process_Time:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
              <xsl:for-each select="srcprod">
                <DT><I>Source_Produced_Citation_Abbreviation:</I></DT>
                <DD><xsl:value-of select="."/></DD>
              </xsl:for-each>
              <xsl:for-each select="proccont">
                <DT><I>Process_Contact:</I></DT>
                <DD>
                <DL>
                  <xsl:apply-templates select="cntinfo"/>
                </DL>
                </DD>
              </xsl:for-each>
            </DL>
            </DD>
          </xsl:for-each>
        </DL>
        </DD>
      </xsl:for-each>
      <xsl:for-each select="cloud">
        <DT><I>Cloud_Cover:</I> <xsl:value-of select="."/></DT>
      </xsl:for-each>
    </DL>
    </DD>
  </DL>
  <A HREF="#Top">Back to Top</A>
</xsl:template>

<!-- Spatial Data Organization -->
<xsl:template match="spdoinfo">
  <A name="Spatial_Data_Organization_Information"><HR/></A>
  <DL>
    <DT><I>Spatial_Data_Organization_Information:</I></DT>
    <DD>
    <DL>
      <xsl:for-each select="indspref">
        <DT><I>Indirect_Spatial_Reference_Method:</I></DT>
        <DD><xsl:value-of select="."/></DD>
      </xsl:for-each>

      <xsl:for-each select="direct">
        <DT><I>Direct_Spatial_Reference_Method:</I> <xsl:value-of select="."/></DT>
      </xsl:for-each>

      <xsl:for-each select="ptvctinf">
        <DT><I>Point_and_Vector_Object_Information:</I></DT>
        <DD>
        <DL>
          <xsl:for-each select="sdtsterm">
            <DT><I>SDTS_Terms_Description:</I></DT>
            <DD>
            <DL>
              <xsl:for-each select="sdtstype">
                <DT><I>SDTS_Point_and_Vector_Object_Type:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
              <xsl:for-each select="ptvctcnt">
                <DT><I>Point_and_Vector_Object_Count:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
            </DL>
            </DD>
          </xsl:for-each>

          <xsl:for-each select="vpfterm">
            <DT><I>VPF_Terms_Description:</I></DT>
            <DD>
            <DL>
              <xsl:for-each select="vpflevel">
                <DT><I>VPF_Topology_Level:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
              <xsl:for-each select="vpfinfo">
                <DT><I>VPF_Point_and_Vector_Object_Information:</I></DT>
                <DD>
                <DL>
                  <xsl:for-each select="vpftype">
                    <DT><I>VPF_Point_and_Vector_Object_Type:</I> <xsl:value-of select="."/></DT>
                  </xsl:for-each>
                  <xsl:for-each select="ptvctcnt">
                    <DT><I>Point_and_Vector_Object_Count:</I> <xsl:value-of select="."/></DT>
                  </xsl:for-each>
                </DL>
                </DD>
              </xsl:for-each>
            </DL>
            </DD>
          </xsl:for-each>
        </DL>
        </DD>
      </xsl:for-each>

      <xsl:for-each select="rastinfo">
        <DT><I>Raster_Object_Information:</I></DT>
        <DD>
        <DL>
          <xsl:for-each select="rasttype">
            <DT><I>Raster_Object_Type:</I> <xsl:value-of select="."/></DT>
          </xsl:for-each>
          <xsl:for-each select="rowcount">
            <DT><I>Row_Count:</I> <xsl:value-of select="."/></DT>
          </xsl:for-each>
          <xsl:for-each select="colcount">
            <DT><I>Column_Count:</I> <xsl:value-of select="."/></DT>
          </xsl:for-each>
          <xsl:for-each select="vrtcount">
            <DT><I>Vertical_Count:</I> <xsl:value-of select="."/></DT>
          </xsl:for-each>
        </DL>
        </DD>
      </xsl:for-each>
    </DL>
    </DD>
  </DL>
  <A HREF="#Top">Back to Top</A>
</xsl:template>

<!-- Spatial Reference -->
<xsl:template match="spref">
  <A name="Spatial_Reference_Information"><HR/></A>
  <DL>
    <DT><I>Spatial_Reference_Information:</I></DT>
    <DD>
    <DL>
      <xsl:for-each select="horizsys">
        <DT><I>Horizontal_Coordinate_System_Definition:</I></DT>
        <DD>
        <DL>
          <xsl:for-each select="geograph">
            <DT><I>Geographic:</I></DT>
            <DD>
            <DL>
              <xsl:for-each select="latres">
                <DT><I>Latitude_Resolution:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
              <xsl:for-each select="longres">
                <DT><I>Longitude_Resolution:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
              <xsl:for-each select="geogunit">
                <DT><I>Geographic_Coordinate_Units:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
            </DL>
            </DD>
          </xsl:for-each>

          <xsl:for-each select="planar">
            <DT><I>Planar:</I></DT>
            <DD>
            <DL>
              <xsl:for-each select="mapproj">
                <DT><I>Map_Projection:</I></DT>
                <DD>
                <DL>
                  <xsl:for-each select="mapprojn">
                    <DT><I>Map_Projection_Name:</I> <xsl:value-of select="."/></DT>
                  </xsl:for-each>

                  <xsl:for-each select="albers">
                    <DT><I>Albers_Conical_Equal_Area:</I></DT>
                  </xsl:for-each>
                  <xsl:for-each select="azimequi">
                    <DT><I>Azimuthal_Equidistant:</I></DT>
                  </xsl:for-each>
                  <xsl:for-each select="equicon">
                    <DT><I>Equidistant_Conic:</I></DT>
                  </xsl:for-each>
                  <xsl:for-each select="equirect">
                    <DT><I>Equirectangular:</I></DT>
                  </xsl:for-each>
                  <xsl:for-each select="gvnsp">
                    <DT><I>General_Vertical_Near-sided_Perspective:</I></DT>
                  </xsl:for-each>
                  <xsl:for-each select="gnomonic">
                    <DT><I>Gnomonic:</I></DT>
                  </xsl:for-each>
                  <xsl:for-each select="lamberta">
                    <DT><I>Lambert_Azimuthal_Equal_Area:</I></DT>
                  </xsl:for-each>
                  <xsl:for-each select="lambertc">
                    <DT><I>Lambert_Conformal_Conic:</I></DT>
                  </xsl:for-each>
                  <xsl:for-each select="mercator">
                    <DT><I>Mercator:</I></DT>
                  </xsl:for-each>
                  <xsl:for-each select="modsak">
                    <DT><I>Modified_Stereographic_for_Alaska:</I></DT>
                    <DD>
                    <DL>
                      <xsl:apply-templates select="feast"/>
                      <xsl:apply-templates select="fnorth"/>
                    </DL>
                    </DD>
                  </xsl:for-each>
                  <xsl:for-each select="miller">
                    <DT><I>Miller_Cylindrical:</I></DT>
                  </xsl:for-each>
                  <xsl:for-each select="obqmerc">
                    <DT><I>Oblique_Mercator:</I></DT>
                  </xsl:for-each>
                  <xsl:for-each select="orthogr">
                    <DT><I>Orthographic:</I></DT>
                  </xsl:for-each>
                  <xsl:for-each select="polarst">
                    <DT><I>Polar_Stereographic:</I></DT>
                  </xsl:for-each>
                  <xsl:for-each select="polycon">
                    <DT><I>Polyconic:</I></DT>
                  </xsl:for-each>
                  <xsl:for-each select="robinson">
                    <DT><I>Robinson:</I></DT>
                    <DD>
                    <DL>
                      <xsl:apply-templates select="longpc"/>
                      <xsl:apply-templates select="feast"/>
                      <xsl:apply-templates select="fnorth"/>
                    </DL>
                    </DD>
                  </xsl:for-each>
                  <xsl:for-each select="sinusoid">
                    <DT><I>Sinusoidal:</I></DT>
                  </xsl:for-each>
                  <xsl:for-each select="spaceobq">
                    <DT><I>Space_Oblique_Mercator_(Landsat):</I></DT>
                    <DD>
                    <DL>
                      <xsl:apply-templates select="landsat"/>
                      <xsl:apply-templates select="pathnum"/>
                      <xsl:apply-templates select="feast"/>
                      <xsl:apply-templates select="fnorth"/>
                    </DL>
                    </DD>
                  </xsl:for-each>
                  <xsl:for-each select="stereo">
                    <DT><I>Stereographic:</I></DT>
                  </xsl:for-each>
                  <xsl:for-each select="transmer">
                    <DT><I>Transverse_Mercator:</I></DT>
                  </xsl:for-each>
                  <xsl:for-each select="vdgrin">
                    <DT><I>van_der_Grinten:</I></DT>
                  </xsl:for-each>

                  <xsl:apply-templates select="*"/>
                </DL>
                </DD>
              </xsl:for-each>

              <xsl:for-each select="gridsys">
                <DT><I>Grid_Coordinate_System:</I></DT>
                <DD>
                <DL>
                  <xsl:for-each select="gridsysn">
                    <DT><I>Grid_Coordinate_System_Name:</I> <xsl:value-of select="."/></DT>
                  </xsl:for-each>

                  <xsl:for-each select="utm">
                    <DT><I>Universal_Transverse_Mercator:</I></DT>
                    <DD>
                    <DL>
                      <xsl:for-each select="utmzone">
                        <DT><I>UTM_Zone_Number:</I> <xsl:value-of select="."/></DT>
                      </xsl:for-each>
                      <xsl:for-each select="transmer">
                        <DT><I>Transverse_Mercator:</I></DT>
                      </xsl:for-each>
                      <xsl:apply-templates select="transmer"/>
                    </DL>
                    </DD>
                  </xsl:for-each>

                  <xsl:for-each select="ups">
                    <DT><I>Universal_Polar_Stereographic:</I></DT>
                    <DD>
                    <DL>
                      <xsl:for-each select="upszone">
                        <DT><I>UPS_Zone_Identifier:</I> <xsl:value-of select="."/></DT>
                      </xsl:for-each>
                      <xsl:for-each select="polarst">
                        <DT><I>Polar_Stereographic:</I></DT>
                      </xsl:for-each>
                      <xsl:apply-templates select="polarst"/>
                    </DL>
                    </DD>
                  </xsl:for-each>

                  <xsl:for-each select="spcs">
                    <DT><I>State_Plane_Coordinate_System:</I></DT>
                    <DD>
                    <DL>
                      <xsl:for-each select="spcszone">
                        <DT><I>SPCS_Zone_Identifier:</I> <xsl:value-of select="."/></DT>
                      </xsl:for-each>
                      <xsl:for-each select="lambertc">
                        <DT><I>Lambert_Conformal_Conic:</I></DT>
                      </xsl:for-each>
                      <xsl:apply-templates select="lambertc"/>
                      <xsl:for-each select="transmer">
                        <DT><I>Transverse_Mercator:</I></DT>
                      </xsl:for-each>
                      <xsl:apply-templates select="transmer"/>
                      <xsl:for-each select="obqmerc">
                        <DT><I>Oblique_Mercator:</I></DT>
                      </xsl:for-each>
                      <xsl:apply-templates select="obqmerc"/>
                      <xsl:for-each select="polycon">
                        <DT><I>Polyconic:</I></DT>
                      </xsl:for-each>
                      <xsl:apply-templates select="polycon"/>
                    </DL>
                    </DD>
                  </xsl:for-each>

                  <xsl:for-each select="arcsys">
                    <DT><I>ARC_Coordinate_System:</I></DT>
                    <DD>
                    <DL>
                      <xsl:for-each select="arczone">
                        <DT><I>ARC_System_Zone_Identifier:</I> <xsl:value-of select="."/></DT>
                      </xsl:for-each>
                      <xsl:for-each select="equirect">
                        <DT><I>Equirectangular:</I></DT>
                      </xsl:for-each>
                      <xsl:apply-templates select="equirect"/>
                      <xsl:for-each select="azimequi">
                        <DT><I>Azimuthal_Equidistant:</I></DT>
                      </xsl:for-each>
                      <xsl:apply-templates select="azimequi"/>
                    </DL>
                    </DD>
                  </xsl:for-each>

                  <xsl:for-each select="othergrd">
                    <DT><I>Other_Grid_System's_Definition:</I></DT>
                    <DD><xsl:value-of select="."/></DD>
                  </xsl:for-each>
                </DL>
                </DD>
              </xsl:for-each>

              <xsl:for-each select="localp">
                <DT><I>Local_Planar:</I></DT>
                <DD>
                <DL>
                  <xsl:for-each select="localpd">
                    <DT><I>Local_Planar_Description:</I></DT>
                    <DD><xsl:value-of select="."/></DD>
                  </xsl:for-each>
                  <xsl:for-each select="localpgi">
                    <DT><I>Local_Planar_Georeference_Information:</I></DT>
                    <DD><xsl:value-of select="."/></DD>
                  </xsl:for-each>
                </DL>
                </DD>
              </xsl:for-each>

              <xsl:for-each select="planci">
                <DT><I>Planar_Coordinate_Information:</I></DT>
                <DD>
                <DL>
                  <xsl:for-each select="plance">
                    <DT><I>Planar_Coordinate_Encoding_Method:</I> <xsl:value-of select="."/></DT>
                  </xsl:for-each>
                  <xsl:for-each select="coordrep">
                    <DT><I>Coordinate_Representation:</I></DT>
                    <DD>
                    <DL>
                      <xsl:for-each select="absres">
                        <DT><I>Abscissa_Resolution:</I> <xsl:value-of select="."/></DT>
                      </xsl:for-each>
                      <xsl:for-each select="ordres">
                        <DT><I>Ordinate_Resolution:</I> <xsl:value-of select="."/></DT>
                      </xsl:for-each>
                    </DL>
                    </DD>
                  </xsl:for-each>
                  <xsl:for-each select="distbrep">
                    <DT><I>Distance_and_Bearing_Representation:</I></DT>
                    <DD>
                    <DL>
                      <xsl:for-each select="distres">
                        <DT><I>Distance_Resolution:</I> <xsl:value-of select="."/></DT>
                      </xsl:for-each>
                      <xsl:for-each select="bearres">
                        <DT><I>Bearing_Resolution:</I> <xsl:value-of select="."/></DT>
                      </xsl:for-each>
                      <xsl:for-each select="bearunit">
                        <DT><I>Bearing_Units:</I> <xsl:value-of select="."/></DT>
                      </xsl:for-each>
                      <xsl:for-each select="bearrefd">
                        <DT><I>Bearing_Reference_Direction:</I> <xsl:value-of select="."/></DT>
                      </xsl:for-each>
                      <xsl:for-each select="bearrefm">
                        <DT><I>Bearing_Reference_Meridian:</I> <xsl:value-of select="."/></DT>
                      </xsl:for-each>
                    </DL>
                    </DD>
                  </xsl:for-each>
                  <xsl:for-each select="plandu">
                    <DT><I>Planar_Distance_Units:</I> <xsl:value-of select="."/></DT>
                  </xsl:for-each>
                </DL>
                </DD>
              </xsl:for-each>
            </DL>
            </DD>
          </xsl:for-each>

          <xsl:for-each select="local">
            <DT><I>Local:</I></DT>
            <DD>
            <DL>
              <xsl:for-each select="localdes">
                <DT><I>Local_Description:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
              <xsl:for-each select="localgeo">
                <DT><I>Local_Georeference_Information:</I></DT>
                <DD><xsl:value-of select="."/></DD>
              </xsl:for-each>
            </DL>
            </DD>
          </xsl:for-each>

          <xsl:for-each select="geodetic">
            <DT><I>Geodetic_Model:</I></DT>
            <DD>
            <DL>
              <xsl:for-each select="horizdn">
                <DT><I>Horizontal_Datum_Name:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
              <xsl:for-each select="ellips">
                <DT><I>Ellipsoid_Name:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
              <xsl:for-each select="semiaxis">
                <DT><I>Semi-major_Axis:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
              <xsl:for-each select="denflat">
                <DT><I>Denominator_of_Flattening_Ratio:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
            </DL>
            </DD>
          </xsl:for-each>
        </DL>
        </DD>
      </xsl:for-each>

      <xsl:for-each select="vertdef">
        <DT><I>Vertical_Coordinate_System_Definition:</I></DT>
        <DD>
        <DL>
          <xsl:for-each select="altsys">
            <DT><I>Altitude_System_Definition:</I></DT>
            <DD>
            <DL>
              <xsl:for-each select="altdatum">
                <DT><I>Altitude_Datum_Name:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
              <xsl:for-each select="altres">
                <DT><I>Altitude_Resolution:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
              <xsl:for-each select="altunits">
                <DT><I>Altitude_Distance_Units:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
              <xsl:for-each select="altenc">
                <DT><I>Altitude_Encoding_Method:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
            </DL>
            </DD>
          </xsl:for-each>

          <xsl:for-each select="depthsys">
            <DT><I>Depth_System_Definition:</I></DT>
            <DD>
            <DL>
              <xsl:for-each select="depthdn">
                <DT><I>Depth_Datum_Name:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
              <xsl:for-each select="depthres">
                <DT><I>Depth_Resolution:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
              <xsl:for-each select="depthdu">
                <DT><I>Depth_Distance_Units:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
              <xsl:for-each select="depthem">
                <DT><I>Depth_Encoding_Method:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
            </DL>
            </DD>
          </xsl:for-each>
        </DL>
        </DD>
      </xsl:for-each>
    </DL>
    </DD>
  </DL>
  <A HREF="#Top">Back to Top</A>
</xsl:template>

<!-- Entity and Attribute -->
<xsl:template match="eainfo">
  <A name="Entity_and_Attribute_Information"><HR/></A>
  <DL>
    <DT><I>Entity_and_Attribute_Information:</I></DT>
    <DD>
    <DL>
      <xsl:for-each select="detailed">
        <DT><I>Detailed_Description:</I></DT>
        <DD>
        <DL>
          <xsl:for-each select="enttyp">
            <DT><I>Entity_Type:</I></DT>
            <DD>
            <DL>
              <xsl:for-each select="enttypl">
                <DT><I>Entity_Type_Label:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
              <xsl:for-each select="enttypd">
                <DT><I>Entity_Type_Definition:</I></DT>
                <DD><xsl:value-of select="."/></DD>
              </xsl:for-each>
              <xsl:for-each select="enttypds">
                <DT><I>Entity_Type_Definition_Source:</I></DT>
                <DD><xsl:value-of select="."/></DD>
              </xsl:for-each>
            </DL>
            </DD>
          </xsl:for-each>

          <xsl:for-each select="attr">
            <DT><I>Attribute:</I></DT>
            <DD>
            <DL>
              <xsl:for-each select="attrlabl">
                <DT><I>Attribute_Label:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
              <xsl:for-each select="attrdef">
                <DT><I>Attribute_Definition:</I></DT>
                <DD><xsl:value-of select="."/></DD>
              </xsl:for-each>
              <xsl:for-each select="attrdefs">
                <DT><I>Attribute_Definition_Source:</I></DT>
                <DD><xsl:value-of select="."/></DD>
              </xsl:for-each>

              <xsl:for-each select="attrdomv">
                <DT><I>Attribute_Domain_Values:</I></DT>
                <DD>
                <DL>
                  <xsl:for-each select="edom">
                    <DT><I>Enumerated_Domain:</I></DT>
                    <DD>
                    <DL>
                      <xsl:for-each select="edomv">
                        <DT><I>Enumerated_Domain_Value:</I> <xsl:value-of select="."/></DT>
                      </xsl:for-each>
                      <xsl:for-each select="edomvd">
                        <DT><I>Enumerated_Domain_Value_Definition:</I></DT>
                        <DD><xsl:value-of select="."/></DD>
                      </xsl:for-each>
                      <xsl:for-each select="edomvds">
                        <DT><I>Enumerated_Domain_Value_Definition_Source:</I></DT>
                        <DD><xsl:value-of select="."/></DD>
                      </xsl:for-each>
                      <xsl:for-each select="attr">
                        <DT><I>Attribute:</I> <xsl:value-of select="."/></DT>
                      </xsl:for-each>
                    </DL>
                    </DD>
                  </xsl:for-each>

                  <xsl:for-each select="rdom">
                    <DT><I>Range_Domain:</I></DT>
                    <DD>
                    <DL>
                      <xsl:for-each select="rdommin">
                        <DT><I>Range_Domain_Minimum:</I> <xsl:value-of select="."/></DT>
                      </xsl:for-each>
                      <xsl:for-each select="rdommax">
                        <DT><I>Range_Domain_Maximum:</I> <xsl:value-of select="."/></DT>
                      </xsl:for-each>
                      <xsl:for-each select="attrunit">
                        <DT><I>Attribute_Units_of_Measure:</I> <xsl:value-of select="."/></DT>
                      </xsl:for-each>
                      <xsl:for-each select="attrmres">
                        <DT><I>Attribute_Measurement_Resolution:</I> <xsl:value-of select="."/></DT>
                      </xsl:for-each>
                      <xsl:for-each select="attr">
                        <DT><I>Attribute:</I> <xsl:value-of select="."/></DT>
                      </xsl:for-each>
                    </DL>
                    </DD>
                  </xsl:for-each>

                  <xsl:for-each select="codesetd">
                    <DT><I>Codeset_Domain:</I></DT>
                    <DD>
                    <DL>
                      <xsl:for-each select="codesetn">
                        <DT><I>Codeset_Name:</I> <xsl:value-of select="."/></DT>
                      </xsl:for-each>
                      <xsl:for-each select="codesets">
                        <DT><I>Codeset_Source:</I> <xsl:value-of select="."/></DT>
                      </xsl:for-each>
                    </DL>
                    </DD>
                  </xsl:for-each>

                  <xsl:for-each select="udom">
                    <DT><I>Unrepresentable_Domain:</I></DT>
                    <DD><xsl:value-of select="."/></DD>
                  </xsl:for-each>
                </DL>
                </DD>
              </xsl:for-each>

              <xsl:for-each select="begdatea">
                <DT><I>Beginning_Date_of_Attribute_Values:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>
              <xsl:for-each select="enddatea">
                <DT><I>Ending_Date_of_Attribute_Values:</I> <xsl:value-of select="."/></DT>
              </xsl:for-each>

              <xsl:for-each select="attrvai">
                <DT><I>Attribute_Value_Accuracy_Information:</I></DT>
                <DD>
                <DL>
                  <xsl:for-each select="attrva">
                    <DT><I>Attribute_Value_Accuracy:</I> <xsl:value-of select="."/></DT>
                  </xsl:for-each>
                   <xsl:for-each select="attrvae">
                    <DT><I>Attribute_Value_Accuracy_Explanation:</I></DT>
                    <DD><xsl:value-of select="."/></DD>
                  </xsl:for-each>
                 </DL>
                </DD>
              </xsl:for-each>
              <xsl:for-each select="attrmfrq">
                <DT><I>Attribute_Measurement_Frequency:</I></DT>
                <DD><xsl:value-of select="."/></DD>
              </xsl:for-each>
            </DL>
            </DD>
          </xsl:for-each>
        </DL>
        </DD>
      </xsl:for-each>

      <xsl:for-each select="overview">
        <DT><I>Overview_Description:</I></DT>
        <DD>
        <DL>
          <xsl:for-each select="eaover">
            <DT><I>Entity_and_Attribute_Overview:</I></DT>
            <DD><xsl:value-of select="."/></DD>
          </xsl:for-each>
          <xsl:for-each select="eadetcit">
            <DT><I>Entity_and_Attribute_Detail_Citation:</I></DT>
            <DD><xsl:value-of select="."/></DD>
          </xsl:for-each>
        </DL>
        </DD>
      </xsl:for-each>
    </DL>
    </DD>
  </DL>
  <A HREF="#Top">Back to Top</A>
</xsl:template>

<!-- Distribution -->
<xsl:template match="distinfo">
<!--  <A>
    <xsl:attribute name="NAME"><xsl:eval>uniqueID(this)</xsl:eval></xsl:attribute>
    <HR/>
  </A>
-->
  <A name="{generate-id()}"><HR/></A> 
  <DL>
    <DT><I>Distribution_Information:</I> </DT>
    <DD>
    <DL>
      <xsl:for-each select="distrib">
        <DT><I>Distributor:</I></DT>
        <DD>
        <DL>
          <xsl:apply-templates select="cntinfo"/>
        </DL>
        </DD>
      </xsl:for-each>

      <xsl:for-each select="resdesc">
        <DT><I>Resource_Description:</I> <xsl:value-of select="."/></DT>
      </xsl:for-each>
      <xsl:for-each select="distliab">
        <DT><I>Distribution_Liability:</I></DT>
        <DD><xsl:value-of select="."/></DD>
      </xsl:for-each>

      <xsl:for-each select="stdorder">
        <DT><I>Standard_Order_Process:</I></DT>
        <DD>
        <DL>
          <xsl:for-each select="nondig">
            <DT><I>Non-digital_Form:</I></DT>
            <DD><xsl:value-of select="."/></DD>
          </xsl:for-each>
          <xsl:for-each select="digform">
            <DT><I>Digital_Form:</I></DT>
            <DD>
            <DL>
              <xsl:for-each select="digtinfo">
                <DT><I>Digital_Transfer_Information:</I></DT>
                <DD>
                <DL>
                  <xsl:for-each select="formname">
                    <DT><I>Format_Name:</I> <xsl:value-of select="."/></DT>
                  </xsl:for-each>
                  <xsl:for-each select="formvern">
                    <DT><I>Format_Version_Number:</I> <xsl:value-of select="."/></DT>
                  </xsl:for-each>
                  <xsl:for-each select="formverd">
                    <DT><I>Format_Version_Date:</I> <xsl:value-of select="."/></DT>
                  </xsl:for-each>
                  <xsl:for-each select="formspec">
                    <DT><I>Format_Specification:</I></DT>
                    <DD><xsl:value-of select="."/></DD>
                  </xsl:for-each>
                  <xsl:for-each select="formcont">
                   <DT><I>Format_Information_Content:</I></DT>
                    <DD><xsl:value-of select="."/></DD>
                  </xsl:for-each>
                  <xsl:for-each select="filedec">
                    <DT><I>File_Decompression_Technique:</I> <xsl:value-of select="."/></DT>
                  </xsl:for-each>
                  <xsl:for-each select="transize">
                    <DT><I>Transfer_Size:</I> <xsl:value-of select="."/></DT>
                  </xsl:for-each>
                </DL>
                </DD>
              </xsl:for-each>

              <xsl:for-each select="digtopt">
                <DT><I>Digital_Transfer_Option:</I></DT>
                <DD>
                <DL>
                  <xsl:for-each select="onlinopt">
                    <DT><I>Online_Option:</I></DT>
                    <DD>
                    <DL>
                      <xsl:for-each select="computer">
                        <DT><I>Computer_Contact_Information:</I></DT>
                        <DD>
                        <DL>
                          <xsl:for-each select="networka">
                            <DT><I>Network_Address:</I></DT>
                            <DD>
                            <DL>
                              <xsl:for-each select="networkr">
                                <DT><I>Network_Resource_Name:</I> <A TARGET="viewer">
                                  <xsl:attribute name="HREF"><xsl:value-of select="."/></xsl:attribute>
                                  <xsl:value-of select="."/></A>
                                </DT>
                              </xsl:for-each>
                            </DL>
                            </DD>
                          </xsl:for-each>

                          <xsl:for-each select="dialinst">
                            <DT><I>Dialup_Instructions:</I></DT>
                            <DD>
                            <DL>
                              <xsl:for-each select="lowbps">
                                <DT><I>Lowest_BPS:</I> <xsl:value-of select="."/></DT>
                              </xsl:for-each>
                              <xsl:for-each select="highbps">
                                <DT><I>Highest_BPS:</I> <xsl:value-of select="."/></DT>
                              </xsl:for-each>
                              <xsl:for-each select="numdata">
                                <DT><I>Number_DataBits:</I> <xsl:value-of select="."/></DT>
                              </xsl:for-each>
                              <xsl:for-each select="numstop">
                                <DT><I>Number_StopBits:</I> <xsl:value-of select="."/></DT>
                              </xsl:for-each>
                              <xsl:for-each select="parity">
                                <DT><I>Parity:</I> <xsl:value-of select="."/></DT>
                              </xsl:for-each>
                              <xsl:for-each select="compress">
                                <DT><I>Compression_Support:</I> <xsl:value-of select="."/></DT>
                              </xsl:for-each>
                              <xsl:for-each select="dialtel">
                                <DT><I>Dialup_Telephone:</I> <xsl:value-of select="."/></DT>
                              </xsl:for-each>
                              <xsl:for-each select="dialfile">
                                <DT><I>Dialup_File_Name:</I> <xsl:value-of select="."/></DT>
                              </xsl:for-each>
                            </DL>
                            </DD>
                          </xsl:for-each>
                        </DL>
                        </DD>
                      </xsl:for-each>
                      <xsl:for-each select="accinstr">
                        <DT><I>Access_Instructions:</I></DT>
                        <DD><xsl:value-of select="."/></DD>
                      </xsl:for-each>
                      <xsl:for-each select="oncomp">
                        <DT><I>Online_Computer_and_Operating_System:</I></DT>
                        <DD><xsl:value-of select="."/></DD>
                      </xsl:for-each>
                    </DL>
                    </DD>
                  </xsl:for-each>

                  <xsl:for-each select="offoptn">
                    <DT><I>Offline_Option:</I></DT>
                    <DD>
                    <DL>
                      <xsl:for-each select="offmedia">
                        <DT><I>Offline_Media:</I> <xsl:value-of select="."/></DT>
                      </xsl:for-each>
                      <xsl:for-each select="reccap">
                        <DT><I>Recording_Capacity:</I></DT>
                        <DD>
                        <DL>
                          <xsl:for-each select="recden">
                            <DT><I>Recording_Density:</I> <xsl:value-of select="."/></DT>
                          </xsl:for-each>
                          <xsl:for-each select="recdenu">
                            <DT><I>Recording_Density_Units:</I> <xsl:value-of select="."/></DT>
                          </xsl:for-each>
                        </DL>
                        </DD>
                      </xsl:for-each>
                      <xsl:for-each select="recfmt">
                        <DT><I>Recording_Format:</I> <xsl:value-of select="."/></DT>
                      </xsl:for-each>
                      <xsl:for-each select="compat">
                        <DT><I>Compatibility_Information:</I></DT>
                        <DD><xsl:value-of select="."/></DD>
                      </xsl:for-each>
                    </DL>
                    </DD>
                  </xsl:for-each>
                </DL>
                </DD>
              </xsl:for-each>
            </DL>
            </DD>
          </xsl:for-each>

          <xsl:for-each select="fees">
            <DT><I>Fees:</I> <xsl:value-of select="."/></DT>
          </xsl:for-each>
          <xsl:for-each select="ordering">
            <DT><I>Ordering_Instructions:</I></DT>
            <DD><xsl:value-of select="."/></DD>
          </xsl:for-each>
          <xsl:for-each select="turnarnd">
            <DT><I>Turnaround:</I> <xsl:value-of select="."/></DT>
          </xsl:for-each>
        </DL>
        </DD>
      </xsl:for-each>

      <xsl:for-each select="custom">
        <DT><I>Custom_Order_Process:</I></DT>
        <DD><xsl:value-of select="."/></DD>
      </xsl:for-each>
      <xsl:for-each select="techpreq">
        <DT><I>Technical_Prerequisites:</I></DT>
        <DD><xsl:value-of select="."/></DD>
      </xsl:for-each>
      <xsl:for-each select="availabl">
        <DT><I>Available_Time_Period:</I></DT>
        <DD>
        <DL>
          <xsl:apply-templates select="timeinfo"/>
        </DL>
        </DD>
      </xsl:for-each>
    </DL>
    </DD>
  </DL>
  <A HREF="#Top">Back to Top</A>
</xsl:template>

<!-- Metadata -->
<xsl:template match="metainfo">
  <A name="Metadata_Reference_Information"><HR/></A>
  <DL>
    <DT><I>Metadata_Reference_Information:</I></DT>
    <DD>
    <DL>
      <xsl:for-each select="metd">
        <DT><I>Metadata_Date:</I> <xsl:value-of select="."/></DT>
      </xsl:for-each>
      <xsl:for-each select="metrd">
        <DT><I>Metadata_Review_Date:</I> <xsl:value-of select="."/></DT>
      </xsl:for-each>
      <xsl:for-each select="metfrd">
        <DT><I>Metadata_Future_Review_Date:</I> <xsl:value-of select="."/></DT>
      </xsl:for-each>

      <xsl:for-each select="metc">
        <DT><I>Metadata_Contact:</I></DT>
        <DD>
        <DL>
          <xsl:apply-templates select="cntinfo"/>
        </DL>
        </DD>
      </xsl:for-each>

      <xsl:for-each select="metstdn">
        <DT><I>Metadata_Standard_Name:</I> <xsl:value-of select="."/></DT>
      </xsl:for-each>
      <xsl:for-each select="metstdv">
        <DT><I>Metadata_Standard_Version:</I> <xsl:value-of select="."/></DT>
      </xsl:for-each>
      <xsl:for-each select="mettc">
        <DT><I>Metadata_Time_Convention:</I> <xsl:value-of select="."/></DT>
      </xsl:for-each>

      <xsl:for-each select="metac">
        <DT><I>Metadata_Access_Constraints:</I> <xsl:value-of select="."/></DT>
      </xsl:for-each>
      <xsl:for-each select="metuc">
        <DT><I>Metadata_Use_Constraints:</I></DT>
        <DD><xsl:value-of select="."/></DD>
      </xsl:for-each>

      <xsl:for-each select="metsi">
        <DT><I>Metadata_Security_Information:</I></DT>
        <DD>
        <DL>
          <xsl:for-each select="metscs">
            <DT><I>Metadata_Security_Classification_System:</I> <xsl:value-of select="."/></DT>
          </xsl:for-each>
          <xsl:for-each select="metsc">
            <DT><I>Metadata_Security_Classification:</I> <xsl:value-of select="."/></DT>
          </xsl:for-each>
          <xsl:for-each select="metshd">
            <DT><I>Metadata_Security_Handling_Description:</I></DT>
            <DD><xsl:value-of select="."/></DD>
          </xsl:for-each>
        </DL>
        </DD>
      </xsl:for-each>

      <xsl:for-each select="metextns">
        <DT><I>Metadata_Extensions:</I></DT>
        <DD>
        <DL>
          <xsl:for-each select="onlink">
            <DT><I>Online_Linkage:</I> <A TARGET="viewer">
              <xsl:attribute name="HREF"><xsl:value-of select="."/></xsl:attribute>
              <xsl:value-of select="."/></A>
            </DT>
          </xsl:for-each>
          <xsl:for-each select="metprof">
            <DT><I>Profile_Name:</I> <xsl:value-of select="."/></DT>
          </xsl:for-each>
        </DL>
        </DD>
      </xsl:for-each>
    </DL>
    </DD>
  </DL>
  <A HREF="#Top">Back to Top</A>
</xsl:template>

<!-- Citation -->
<xsl:template match="citeinfo">
  <DT><I>Citation_Information:</I></DT>
  <DD>
  <DL>

    <xsl:for-each select="origin">
      <DT><I>Originator:</I> <xsl:value-of select="."/></DT>
    </xsl:for-each>

    <xsl:for-each select="pubdate">
      <DT><I>Publication_Date:</I> <xsl:value-of select="."/></DT>
    </xsl:for-each>
    <xsl:for-each select="pubtime">
      <DT><I>Publication_Time:</I> <xsl:value-of select="."/></DT>
    </xsl:for-each>

    <xsl:for-each select="title">
      <DT><I>Title:</I></DT>
      <DD><xsl:value-of select="."/></DD>
    </xsl:for-each>
    <xsl:for-each select="edition">
      <DT><I>Edition:</I> <xsl:value-of select="."/></DT>
    </xsl:for-each>

    <xsl:for-each select="geoform">
      <DT><I>Geospatial_Data_Presentation_Form:</I> <xsl:value-of select="."/></DT>
    </xsl:for-each>

    <xsl:for-each select="serinfo">
      <DT><I>Series_Information:</I></DT>
      <DD>
      <DL>
        <xsl:for-each select="sername">
          <DT><I>Series_Name:</I> <xsl:value-of select="."/></DT>
        </xsl:for-each>
        <xsl:for-each select="issue">
          <DT><I>Issue_Identification:</I> <xsl:value-of select="."/></DT>
        </xsl:for-each>
      </DL>
      </DD>
    </xsl:for-each>

    <xsl:for-each select="pubinfo">
      <DT><I>Publication_Information:</I></DT>
      <DD>
      <DL>
        <xsl:for-each select="pubplace">
          <DT><I>Publication_Place:</I> <xsl:value-of select="."/></DT>
        </xsl:for-each>
        <xsl:for-each select="publish">
          <DT><I>Publisher:</I> <xsl:value-of select="."/></DT>
        </xsl:for-each>
      </DL>
      </DD>
    </xsl:for-each>

    <xsl:for-each select="othercit">
      <DT><I>Other_Citation_Details:</I></DT>
      <DD><xsl:value-of select="."/></DD>
    </xsl:for-each>

    <xsl:for-each select="onlink">
      <DT><I>Online_Linkage:</I> <A TARGET="viewer">
        <xsl:attribute name="HREF"><xsl:value-of select="."/></xsl:attribute>
        <xsl:value-of select="."/></A>
      </DT>
    </xsl:for-each>

    <xsl:for-each select="lworkcit">
      <DT><I>Larger_Work_Citation:</I></DT>
      <DD>
      <DL>
        <xsl:apply-templates select="citeinfo"/>
      </DL>
      </DD>
    </xsl:for-each>

  </DL>
  </DD>
</xsl:template>

<!-- Contact -->
<xsl:template match="cntinfo">
  <DT><I>Contact_Information:</I></DT>
  <DD>
  <DL>
    <xsl:for-each select="cntperp">
      <DT><I>Contact_Person_Primary:</I></DT>
      <DD>
      <DL>
        <xsl:for-each select="cntper">
          <DT><I>Contact_Person:</I> <xsl:value-of select="."/></DT>
        </xsl:for-each>
        <xsl:for-each select="cntorg">
          <DT><I>Contact_Organization:</I> <xsl:value-of select="."/></DT>
        </xsl:for-each>
      </DL>
      </DD>
    </xsl:for-each>
    <xsl:for-each select="cntorgp">
      <DT><I>Contact_Organization_Primary:</I></DT>
      <DD>
      <DL>
        <xsl:for-each select="cntorg">
          <DT><I>Contact_Organization:</I> <xsl:value-of select="."/></DT>
        </xsl:for-each>
        <xsl:for-each select="cntper">
          <DT><I>Contact_Person:</I> <xsl:value-of select="."/></DT>
        </xsl:for-each>
      </DL>
      </DD>
    </xsl:for-each>
    <xsl:for-each select="cntpos">
      <DT><I>Contact_Position:</I> <xsl:value-of select="."/></DT>
    </xsl:for-each>

    <xsl:for-each select="cntaddr">
      <DT><I>Contact_Address:</I></DT>
      <DD>
      <DL>
        <xsl:for-each select="addrtype">
          <DT><I>Address_Type:</I> <xsl:value-of select="."/></DT>
        </xsl:for-each>
        <xsl:for-each select="address">
          <DT><I>Address:</I> <xsl:value-of select="."/></DT>
        </xsl:for-each>
        <xsl:for-each select="city">
          <DT><I>City:</I> <xsl:value-of select="."/></DT>
        </xsl:for-each>
        <xsl:for-each select="state">
          <DT><I>State_or_Province:</I> <xsl:value-of select="."/></DT>
        </xsl:for-each>
        <xsl:for-each select="postal">
          <DT><I>Postal_Code:</I> <xsl:value-of select="."/></DT>
        </xsl:for-each>
        <xsl:for-each select="country">
          <DT><I>Country:</I> <xsl:value-of select="."/></DT>
        </xsl:for-each>
      </DL>
      </DD>
    </xsl:for-each>

    <xsl:for-each select="cntvoice">
      <DT><I>Contact_Voice_Telephone:</I> <xsl:value-of select="."/></DT>
    </xsl:for-each>
    <xsl:for-each select="cnttdd">
      <DT><I>Contact_TDD/TTY_Telephone:</I> <xsl:value-of select="."/></DT>
    </xsl:for-each>
    <xsl:for-each select="cntfax">
      <DT><I>Contact_Facsimile_Telephone:</I> <xsl:value-of select="."/></DT>
    </xsl:for-each>
    <xsl:for-each select="cntemail">
      <DT><I>Contact_Electronic_Mail_Address:</I> <TT><xsl:value-of select="."/></TT></DT>
    </xsl:for-each>

    <xsl:for-each select="hours">
      <DT><I>Hours_of_Service:</I> <xsl:value-of select="."/></DT>
    </xsl:for-each>
    <xsl:for-each select="cntinst">
      <DT><I>Contact Instructions:</I> <xsl:value-of select="."/></DT>
    </xsl:for-each>
  </DL>
  </DD>
</xsl:template>

<!-- Time Period Info -->
<xsl:template match="timeinfo">
  <DT><I>Time_Period_Information:</I></DT>
  <DD>
  <DL>
    <xsl:apply-templates select="sngdate"/>
    <xsl:apply-templates select="mdattim"/>
    <xsl:apply-templates select="rngdates"/>
  </DL>
  </DD>
</xsl:template>

<!-- Single Date/Time -->
<xsl:template match="sngdate">
  <DT><I>Single_Date/Time:</I></DT>
  <DD>
  <DL>
    <xsl:for-each select="caldate">
      <DT><I>Calendar_Date:</I> <xsl:value-of select="."/></DT>
    </xsl:for-each>
    <xsl:for-each select="time">
      <DT><I>Time of Day:</I> <xsl:value-of select="."/></DT>
    </xsl:for-each>
  </DL>
  </DD>
</xsl:template>

<!-- Multiple Date/Time -->
<xsl:template match="mdattim">
  <DT><I>Multiple_Dates/Times:</I></DT>
  <DD>
  <DL>
    <xsl:apply-templates select="sngdate"/>
  </DL>
  </DD>
</xsl:template>

<!-- Range of Dates/Times -->
<xsl:template match="rngdates">
  <DT><I>Range_of_Dates/Times:</I></DT>
  <DD>
  <DL>
    <xsl:for-each select="begdate">
      <DT><I>Beginning_Date:</I> <xsl:value-of select="."/></DT>
    </xsl:for-each>
    <xsl:for-each select="begtime">
      <DT><I>Beginning_Time:</I> <xsl:value-of select="."/></DT>
    </xsl:for-each>
    <xsl:for-each select="enddate">
      <DT><I>Ending_Date:</I> <xsl:value-of select="."/></DT>
    </xsl:for-each>
    <xsl:for-each select="endtime">
      <DT><I>Ending_Time:</I> <xsl:value-of select="."/></DT>
    </xsl:for-each>
  </DL>
  </DD>
</xsl:template>

<!-- G-Ring -->
<xsl:template match="grngpoin">
  <DT><I>G-Ring_Point:</I></DT>
  <DD>
  <DL>
    <xsl:for-each select="gringlat">
      <DT><I>G-Ring_Latitude:</I> <xsl:value-of select="."/></DT>
        </xsl:for-each>
        <xsl:for-each select="gringlon">
      <DT><I>G-Ring_Longitude:</I> <xsl:value-of select="."/></DT>
    </xsl:for-each>
  </DL>
  </DD>
</xsl:template>
<xsl:template match="gring">
  <DT><I>G-Ring:</I></DT>
  <DD><xsl:value-of select="."/></DD>
</xsl:template>


<!-- Map Projections -->
<xsl:template match="albers | equicon | lambertc">
  <DD>
  <DL>
    <xsl:apply-templates select="stdparll"/>
    <xsl:apply-templates select="longcm"/>
    <xsl:apply-templates select="latprjo"/>
    <xsl:apply-templates select="feast"/>
    <xsl:apply-templates select="fnorth"/>
  </DL>
  </DD>
</xsl:template>

<xsl:template match="gnomonic | lamberta | orthogr | stereo | gvnsp">
  <DD>
  <DL>
    <xsl:for-each select="../gvnsp">
      <xsl:apply-templates select="heightpt"/>
    </xsl:for-each>
    <xsl:apply-templates select="longpc"/>
    <xsl:apply-templates select="latprjc"/>
    <xsl:apply-templates select="feast"/>
    <xsl:apply-templates select="fnorth"/>
  </DL>
  </DD>
</xsl:template>

<xsl:template match="miller | sinusoid | vdgrin | equirect | mercator">
  <DD>
  <DL>
    <xsl:for-each select="../equirect">
      <xsl:apply-templates select="stdparll"/>
    </xsl:for-each>
    <xsl:for-each select="../mercator">
      <xsl:apply-templates select="stdparll"/>
      <xsl:apply-templates select="sfequat"/>
    </xsl:for-each>
    <xsl:apply-templates select="longcm"/>
    <xsl:apply-templates select="feast"/>
    <xsl:apply-templates select="fnorth"/>
  </DL>
  </DD>
</xsl:template>

<xsl:template match="azimequi | polycon | transmer">
  <DD>
  <DL>
    <xsl:for-each select="../transmer">
      <xsl:apply-templates select="sfctrmer"/>
    </xsl:for-each>
    <xsl:apply-templates select="longcm"/>
    <xsl:apply-templates select="latprjo"/>
    <xsl:apply-templates select="feast"/>
    <xsl:apply-templates select="fnorth"/>
  </DL>
  </DD>
</xsl:template>

<xsl:template match="polarst">
  <DD>
  <DL>
    <xsl:apply-templates select="svlong"/>
    <xsl:apply-templates select="stdparll"/>
    <xsl:apply-templates select="sfprjorg"/>
    <xsl:apply-templates select="feast"/>
    <xsl:apply-templates select="fnorth"/>
  </DL>
  </DD>
</xsl:template>

<xsl:template match="obqmerc">
  <DD>
  <DL>
    <xsl:apply-templates select="sfctrlin"/>
    <xsl:apply-templates select="obqlazim"/>
    <xsl:apply-templates select="obqlpt"/>
    <xsl:apply-templates select="latprjo"/>
    <xsl:apply-templates select="feast"/>
    <xsl:apply-templates select="fnorth"/>
  </DL>
  </DD>
</xsl:template>
 

<!-- Map Projection Parameters -->
<xsl:template match="stdparll">
  <DT><I>Standard_Parallel:</I> <xsl:value-of select="."/></DT>
</xsl:template>

<xsl:template match="longcm">
  <DT><I>Longitude_of_Central_Meridian:</I> <xsl:value-of select="."/></DT>
</xsl:template>

<xsl:template match="latprjo">
  <DT><I>Latitude_of_Projection_Origin:</I> <xsl:value-of select="."/></DT>
</xsl:template>

<xsl:template match="feast">
  <DT><I>False_Easting:</I> <xsl:value-of select="."/></DT>
</xsl:template>

<xsl:template match="fnorth">
  <DT><I>False_Northing:</I> <xsl:value-of select="."/></DT>
</xsl:template>

<xsl:template match="sfequat">
  <DT><I>Scale_Factor_at_Equator:</I> <xsl:value-of select="."/></DT>
</xsl:template>

<xsl:template match="heightpt">
  <DT><I>Height_of_Perspective_Point_Above_Surface:</I> <xsl:value-of select="."/></DT>
</xsl:template>

<xsl:template match="longpc">
  <DT><I>Longitude_of_Projection_Center:</I> <xsl:value-of select="."/></DT>
</xsl:template>

<xsl:template match="latprjc">
  <DT><I>Latitude_of_Projection_Center:</I> <xsl:value-of select="."/></DT>
</xsl:template>

<xsl:template match="sfctrlin">
  <DT><I>Scale_Factor_at_Center_Line:</I> <xsl:value-of select="."/></DT>
</xsl:template>

<xsl:template match="obqlazim">
  <DT><I>Oblique_Line_Azimuth:</I> <xsl:value-of select="."/></DT>
  <DD>
  <DL>
    <xsl:for-each select="azimangl">
      <DT><I>Azimuthal_Angle:</I> <xsl:value-of select="."/></DT>
    </xsl:for-each>
    <xsl:for-each select="azimptl">
      <DT><I>Azimuthal_Measure_Point_Longitude:</I> <xsl:value-of select="."/></DT>
    </xsl:for-each>
  </DL>
  </DD>
</xsl:template>

<xsl:template match="obqlpt">
  <DT><I>Oblique_Line_Point:</I> <xsl:value-of select="."/></DT>
  <DD>
  <DL>
    <xsl:for-each select="obqllat">
      <DT><I>Oblique_Line_Latitude:</I> <xsl:value-of select="."/></DT>
    </xsl:for-each>
    <xsl:for-each select="obqllong">
       <DT><I>Oblique_Line_Longitude:</I> <xsl:value-of select="."/></DT>
    </xsl:for-each>
  </DL>
  </DD>
</xsl:template>

<xsl:template match="svlong">
  <DT><I>Straight_Vertical_Longitude_from_Pole:</I> <xsl:value-of select="."/></DT>
</xsl:template>

<xsl:template match="sfprjorg">
  <DT><I>Scale_Factor_at_Projection_Origin:</I> <xsl:value-of select="."/></DT>
</xsl:template>

<xsl:template match="landsat">
  <DT><I>Landsat_Number:</I> <xsl:value-of select="."/></DT>
</xsl:template>

<xsl:template match="pathnum">
  <DT><I>Path_Number:</I> <xsl:value-of select="."/></DT>
</xsl:template>

<xsl:template match="sfctrmer">
  <DT><I>Scale_Factor_at_Central_Meridian:</I> <xsl:value-of select="."/></DT>
</xsl:template>

<xsl:template match="otherprj">
  <DT><I>Other_Projection's_Definition:</I></DT>
  <DD><xsl:value-of select="."/></DD>
</xsl:template>

</xsl:stylesheet>
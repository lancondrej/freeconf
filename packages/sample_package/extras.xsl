<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">


<xsl:output method="xml" indent="yes"  encoding="UTF-8"/>

<!-- ############################################################ -->
<!-- ######################TEMPLATES CALLING##################### -->

<!-- calling template on all remaining elements -->
    <xsl:template match="/">
        <extras>
            <xsl:apply-templates/>
        </extras>
    </xsl:template>

    <xsl:template match="entry">
      <!-- print keyword -->
        <xsl:element name="{@name}">
            <xsl:value-of select="."/>
        </xsl:element>
    </xsl:template>

    <!-- ############################################################ -->
    <xsl:template match="container">
        <xsl:element name="{@name}">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>

</xsl:stylesheet>

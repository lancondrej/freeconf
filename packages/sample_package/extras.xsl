<?xml version="1.0"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">


<!-- ############################################################ -->
<xsl:template match="container">
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="entry">
  <xsl:value-of select="."/>
</xsl:template>

</xsl:stylesheet>
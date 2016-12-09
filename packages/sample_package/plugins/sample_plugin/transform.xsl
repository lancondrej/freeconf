<?xml version="1.0"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">


<!-- ############################################################ -->
<xsl:template match="entry[@name='pbool1' or @name='pnumber2']">
  <xsl:value-of select="$comment-sequence" />
  <xsl:text> Plugin key_word </xsl:text>
          <xsl:call-template name="new-lines"/>

      <!-- print keyword -->
      <xsl:value-of select="@name" />
      <xsl:value-of select="$key-value-separator" />
      <!-- print value -->
      <xsl:choose>
        <!-- Translate boolean values -->
        <xsl:when test="string(.) = 'yes'">
          <xsl:value-of select="$boolean-yes" />
        </xsl:when>
        <xsl:when test="string(.) = 'no'">
          <xsl:value-of select="$boolean-no" />
        </xsl:when>
        <!-- Other entries -->
        <xsl:otherwise>
          <xsl:value-of select="." />
        </xsl:otherwise>
      </xsl:choose>
      <!-- output line breaks -->
      <xsl:call-template name="new-lines">
        <xsl:with-param name="repeat" select="$num-new-lines" />
      </xsl:call-template>
</xsl:template>


</xsl:stylesheet>

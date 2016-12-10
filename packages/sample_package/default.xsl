<?xml version="1.0"?>


<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">


<xsl:output method="text" indent="no"/>

<!-- ############################################################ -->
<!-- ##########################HEADER############################ -->

<xsl:variable name="key-value-separator" xml:space="preserve">: </xsl:variable>
<xsl:variable name="fill-char" xml:space="preserve"> </xsl:variable>
<xsl:variable name="num-new-lines">0</xsl:variable>
<xsl:variable name="comment-sequence">#</xsl:variable>


<xsl:variable name="boolean-yes">Enable</xsl:variable>
<xsl:variable name="boolean-no">Disable</xsl:variable>


<!-- ############################################################ -->
<!-- ####################HANDY TEMPLATES######################### -->

<!-- generate new lines, by default $num-new-lines times -->
<xsl:template name="new-lines">
<xsl:param name="repeat">0</xsl:param>
  <xsl:if test="number($repeat) &gt;= 0">
    <xsl:call-template name="new-lines">
      <xsl:with-param name="repeat" select="$repeat - 1"/>
    </xsl:call-template>
    <xsl:text>&#x0A;</xsl:text>
  </xsl:if>
</xsl:template>

<!-- does one indentation step -->
<xsl:template name="indent-step">
  <xsl:param name="repeat">0</xsl:param>
  <xsl:if test="number($repeat) &gt;= 1">
    <xsl:call-template name="indent-step">
      <xsl:with-param name="repeat" select="$repeat - 1"/>
    </xsl:call-template>
    <xsl:value-of select="$fill-char"/>
  </xsl:if>
</xsl:template>



<!-- ############################################################ -->
<!-- ######################TEMPLATES CALLING##################### -->

<!-- calling template on all remaining elements -->
    <xsl:template match="entry">
      <!-- print keyword -->
      <xsl:value-of select="@name"/>
      <xsl:value-of select="$key-value-separator"/>
      <!-- print value -->
      <xsl:choose>
        <!-- Translate boolean values -->
        <xsl:when test="string(.) = 'yes'">
          <xsl:value-of select="$boolean-yes"/>
        </xsl:when>
        <xsl:when test="string(.) = 'no'">
          <xsl:value-of select="$boolean-no"/>
        </xsl:when>
        <!-- Other entries -->
        <xsl:otherwise>
          <xsl:value-of select="."/>
        </xsl:otherwise>
      </xsl:choose>
      <!-- output line breaks -->
      <xsl:call-template name="new-lines">
        <xsl:with-param name="repeat" select="$num-new-lines"/>
      </xsl:call-template>
    </xsl:template>

    <!-- ############################################################ -->
    <xsl:template match="container">
          <xsl:choose>

    <xsl:when test="@name = 'container3'">
      <!-- #### Process section ServerAlias #### -->
      <xsl:value-of select="@name"/>
      <xsl:value-of select="$key-value-separator" />

      <xsl:variable name="name" select="entry[@name = 'string3']"/>
              <xsl:text>&lt;</xsl:text>
        <xsl:value-of select="$name"/>
      <xsl:text>&gt;</xsl:text>
                      <xsl:text>[</xsl:text>
      <xsl:value-of select="entry[@name = 'number3']"/>
      <xsl:text>]</xsl:text>
      <xsl:call-template name="new-lines"/>
    </xsl:when>


    <xsl:otherwise>

      <xsl:value-of select="$comment-sequence"/>
      <xsl:text> Container </xsl:text>
      <xsl:value-of select="@name"/>
      <xsl:call-template name="new-lines"/>

      <xsl:apply-templates/>

      <xsl:value-of select="$comment-sequence"/>
      <xsl:text> End of </xsl:text>
      <xsl:value-of select="@name"/>
      <xsl:call-template name="new-lines">
        <xsl:with-param name="repeat" select="2"/>
      </xsl:call-template>
    </xsl:otherwise>
  </xsl:choose>
    </xsl:template>


    <xsl:template match="container[@name='container-string']">
        <xsl:text>string1</xsl:text>
      <xsl:value-of select="$key-value-separator"/>
        <xsl:for-each select="entry[@name='string1']">
                    <xsl:value-of select="."/>
                    <xsl:if test="position() != last()">
                            <xsl:text>, </xsl:text>
                    </xsl:if>
        </xsl:for-each>
        <xsl:call-template name="new-lines">
             <xsl:with-param name="repeat" select="$num-new-lines"/>
      </xsl:call-template>
    </xsl:template>


</xsl:stylesheet>

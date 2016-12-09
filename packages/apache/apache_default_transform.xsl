<?xml version="1.0"?>


<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">


<xsl:output method="text" indent="no"/>

<!-- ############################################################ -->
<!-- ##########################HEADER############################ -->

<xsl:variable name="page-width">80</xsl:variable>
<xsl:variable name="key-value-width">80</xsl:variable>
<xsl:variable name="key-value-separator" xml:space="preserve"> </xsl:variable>
<xsl:variable name="fill-char" xml:space="preserve"> </xsl:variable>
<xsl:variable name="num-new-lines">2</xsl:variable>
<xsl:variable name="comment-sequence">#</xsl:variable>
<xsl:variable name="output-help">0</xsl:variable>
<xsl:variable name="boolean-yes">On</xsl:variable>
<xsl:variable name="boolean-no">Off</xsl:variable>

<!-- ############################################################ -->
<xsl:variable name="key-value-separator-length" select="string-length($key-value-separator)" />
<xsl:variable name="comment-length" select="string-length($comment-sequence)" />

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
    <xsl:value-of select="$fill-char" />
  </xsl:if>
</xsl:template>


<xsl:template name="wrap">
  <xsl:param name="rest" />
  <xsl:param name="written">0</xsl:param>
  <xsl:param name="new-line">1</xsl:param>
  <!-- one space and the comment sequence -->
  <xsl:variable name="content-width" select="$page-width - 1 - $comment-length" />
  <!-- is there something to parse? -->
  <xsl:if test="$rest">
    <!-- beginning of the new line, need to fill the comment sequence -->
    <xsl:if test="number($new-line) = 1">
      <xsl:value-of select="$comment-sequence" />
      <xsl:value-of select="$fill-char" />
    </xsl:if>
    <!-- the first word from the left of the $rest, separated from $rest by ' ' -->
    <xsl:variable name="word" select="substring-before($rest, ' ')" />
    <xsl:variable name="word-length" select="string-length($word)" />
    
    <xsl:choose>
      <!-- no word found, that means... -->
      <xsl:when test="number($word-length) = 0">
        <xsl:choose>
          <!-- there are more spaces together -->
          <xsl:when test="substring($rest, 1, 1) = ' '">
            <xsl:call-template name="wrap">
              <xsl:with-param name="written" select="number($written)" />
              <xsl:with-param name="new-line">0</xsl:with-param>
              <xsl:with-param name="rest" select="substring($rest, 2)" />
            </xsl:call-template>
          </xsl:when>
          <!-- there is only one word remaining -->
          <xsl:otherwise>
            <!-- OK, the word will fit into the page  -->
            <xsl:if test="number($written) + string-length($rest) &lt; $content-width">
              <xsl:value-of select="$rest" />
            </xsl:if>
            <!-- too long word to fit  -->
            <xsl:if test="not(number($written) + string-length($rest) &lt; $content-width)">
              <xsl:call-template name="new-lines"/>
              <xsl:value-of select="$comment-sequence" />
              <xsl:value-of select="$fill-char" />
              <xsl:value-of select="$rest" />
            </xsl:if>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:when>
      <!-- too long word to fit, it has to overflow -->
      <xsl:when test="number($written) = 0 and number($word-length) &gt;= $content-width">
        <xsl:value-of select="$word" />
        <xsl:call-template name="new-lines"/>
        <xsl:call-template name="wrap">
          <xsl:with-param name="new-line">1</xsl:with-param>
          <xsl:with-param name="rest" select="substring($rest, $word-length + 2)" />
        </xsl:call-template>
      </xsl:when>
      <!-- OK, the word will fit into the page  -->
      <xsl:when test="number($written) + number($word-length) &lt; $content-width">
        <xsl:value-of select="$word" />
        <xsl:text> </xsl:text>
        <xsl:call-template name="wrap">
          <xsl:with-param name="written" select="number($written) + $word-length + 1" />
          <xsl:with-param name="new-line">0</xsl:with-param>
          <xsl:with-param name="rest" select="substring($rest, $word-length + 2)" />
        </xsl:call-template>
      </xsl:when>
      <!-- there is no more room, new line is needed  -->
      <xsl:otherwise>
        <xsl:call-template name="new-lines"/>
        <xsl:call-template name="wrap">
          <xsl:with-param name="new-line">1</xsl:with-param>
          <xsl:with-param name="rest" select="$rest" />
        </xsl:call-template>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:if>
</xsl:template>

<!-- print help above the keyword as a comment, configurable by $output-help -->
<xsl:template name="output-help">
  <!-- print help  -->
  <xsl:if test="number($output-help) = 1">
    <xsl:choose>
      <!-- help fits in the page -->
      <xsl:when test="string-length(help) &lt;= $page-width">
        <xsl:value-of select="$comment-sequence" />
        <xsl:value-of select="$fill-char" />
        <xsl:value-of select="help" />
      </xsl:when>
      <!-- word wrapping is needed -->
      <xsl:otherwise>
        <xsl:call-template name="wrap">
          <xsl:with-param name="rest" select="help" />
        </xsl:call-template>
      </xsl:otherwise>
    </xsl:choose>
    <!-- new line break -->
    <xsl:call-template name="new-lines"/>
  </xsl:if>
</xsl:template>
<!-- ############################################################ -->



<!-- ############################################################ -->
<!-- ######################TEMPLATES CALLING##################### -->

<!-- this drops the whitespace before and after all source tree elements -->
<xsl:strip-space elements="*" />
<!-- calling template on the root element -->
<!-- does nothing, root element will be omitted from the output -->
<xsl:template match="/*">
  <!-- here paste the result from the transformation of the root's children-->
  <xsl:apply-templates />
</xsl:template>

<!--  calling template on every child of the root element
  here paste the result from the transformation of the section's children
  does nothing, section elements will be omitted from the output-->
<!--xsl:template match="/*/*">
  <xsl:apply-templates />
</xsl:template--> 


<!-- calling template on all remaining elements -->
<xsl:template name="process-entry" match="entry">
  <!-- print help if enabled -->
  <xsl:call-template name="output-help" />
  <!-- print keyword -->
  <xsl:value-of select="@name" />
  <xsl:value-of select="$key-value-separator" />
  <!-- print value -->
  <xsl:choose>
    <!-- Entry exceptions -->
    <xsl:when test="@name='Allow' or @name='Deny'">
      <!-- Keywords Allow and Deny must be followed by word 'from' -->
      <xsl:text>from</xsl:text>
      <xsl:value-of select="$key-value-separator" />
      <xsl:value-of select="." />
    </xsl:when>
    <!-- Translate boolean values -->
    <xsl:when test="type = 'bool' and string(.) = 'yes'">
      <xsl:value-of select="$boolean-yes" />
    </xsl:when>
    <xsl:when test="type = 'bool' and string(.) = 'no'">
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


<!-- ############################################################ -->
<xsl:template match="container">

  <xsl:choose>

    <xsl:when test="@name = 'NameVirtualHost'">
      <!-- #### Process section NameVirtual Host #### -->
      <xsl:value-of select="@name" />
      <xsl:value-of select="$key-value-separator" />
      <xsl:value-of select="entry[@name = 'Address']" />
      <xsl:variable name="port" select="entry[@name = 'Port']" />
      <xsl:if test="string-length($port) &gt; 0 and $port != '0'">
        <xsl:text>:</xsl:text>
        <xsl:value-of select="$port"/>
      </xsl:if>
      <xsl:call-template name="new-lines"/>
    </xsl:when>

    <xsl:when test="@name = 'VirtualHost'">
      <!-- #### Process section Virtual Host #### -->
      <!-- Beginning tag -->
      <xsl:text>&lt;</xsl:text>
      <xsl:value-of select="@name" />
      <xsl:text> </xsl:text>
      <xsl:value-of select="entry[@name = 'Address']" />
      <xsl:variable name="port" select="entry[@name = 'Port']" />
      <xsl:if test="string-length($port) &gt; 0">
        <xsl:text>:</xsl:text>
        <xsl:value-of select="$port"/>
      </xsl:if>
      <xsl:text>&gt;</xsl:text>
      <xsl:call-template name="new-lines"/>

      <xsl:apply-templates select="*[@name != 'Address' and @name != 'Port']"/>

      <!-- Ending tag -->
      <xsl:text>&lt;/</xsl:text>
      <xsl:value-of select="@name" />
      <xsl:text>&gt;</xsl:text>
      <xsl:call-template name="new-lines"/>
    </xsl:when>


    <xsl:when test="@name = 'Alias'">
      <!-- #### Process Alias #### -->
      <xsl:call-template name="output-help" />
      <xsl:value-of select="@name" />
      <xsl:value-of select="$key-value-separator" />
      <xsl:value-of select="entry[@name = 'URLPath']" />
      <xsl:value-of select="$key-value-separator" />
      <xsl:value-of select="entry[@name = 'TargetPath']" />
      <xsl:call-template name="new-lines"/>
    </xsl:when>


    <xsl:when test="@name = 'Directory'">
      <!-- #### Process section Directory #### -->
      <!-- Beginning tag -->
      <xsl:text>&lt;</xsl:text>
      <xsl:value-of select="@name" />
      <xsl:text> "</xsl:text>
      <xsl:value-of select="entry[@name = 'Path']" />
      <xsl:text>"&gt;</xsl:text>
      <xsl:call-template name="new-lines"/>

      <xsl:apply-templates select="*[@name != 'Path']"/>

      <!-- Ending tag -->
      <xsl:text>&lt;/</xsl:text>
      <xsl:value-of select="@name" />
      <xsl:text>&gt;</xsl:text>
      <xsl:call-template name="new-lines"/>
    </xsl:when>

    <xsl:when test="@name = 'Options'">
      <!-- #### Process section Options #### -->
      <xsl:value-of select="@name" />
      <!-- Print list of options -->
      <xsl:for-each select="entry">
        <xsl:value-of select="$key-value-separator" />
        <xsl:choose>
          <xsl:when test=". = 'yes'">
            <xsl:value-of select="concat('+', @name)" />
          </xsl:when>
          <xsl:when test=". = 'no'">
            <xsl:value-of select="concat('-', @name)" />
          </xsl:when>
        </xsl:choose>
      </xsl:for-each>
      <xsl:call-template name="new-lines"/>
    </xsl:when>

    <xsl:when test="@name = 'AllowOverride'">
      <!-- #### Process section AllowOverride #### -->
      <xsl:value-of select="@name" />
      <!-- Print list of options -->
      <xsl:choose>
        <xsl:when test="count(entry[. = 'yes']) = 0">
            <xsl:value-of select="$key-value-separator" />
          <xsl:text>None</xsl:text>
        </xsl:when>
        <xsl:when test="count(entry[. = 'no']) = 0">
            <xsl:value-of select="$key-value-separator" />
          <xsl:text>All</xsl:text>
        </xsl:when>
        <xsl:otherwise>
          <xsl:for-each select="entry">
            <xsl:value-of select="$key-value-separator" />
            <xsl:if test=". = 'yes'">
              <xsl:value-of select="@name" />
            </xsl:if>
          </xsl:for-each>
        </xsl:otherwise>
      </xsl:choose>
      <xsl:call-template name="new-lines"/>
    </xsl:when>


    <xsl:when test="@name = 'ServerAlias'">
      <!-- #### Process section ServerAlias #### -->
      <xsl:value-of select="@name" />
      <xsl:value-of select="$key-value-separator" />
      <xsl:value-of select="entry[@name = 'Hostname']" />
      <xsl:call-template name="new-lines"/>
    </xsl:when>

    <xsl:when test="@name = 'Listen'">
      <!-- #### Process section ServerAlias #### -->
      <xsl:value-of select="@name" />
      <xsl:value-of select="$key-value-separator" />

      <xsl:variable name="addr" select="entry[@name = 'Address']" />
      <xsl:if test="string-length($addr) &gt; 0">
        <xsl:value-of select="$addr"/>
        <xsl:text>:</xsl:text>
      </xsl:if>
      <xsl:value-of select="entry[@name = 'Port']" />
      <xsl:call-template name="new-lines"/>
    </xsl:when>


    <xsl:otherwise>

      <xsl:value-of select="$comment-sequence" />
      <xsl:text> Container </xsl:text>
      <xsl:value-of select="@name" />
      <xsl:call-template name="new-lines"/>

      <xsl:apply-templates />

      <xsl:value-of select="$comment-sequence" />
      <xsl:text> End of </xsl:text>
      <xsl:value-of select="@name" />
      <xsl:call-template name="new-lines"/>

    </xsl:otherwise>
  </xsl:choose>

</xsl:template>


<!--xsl:include href="/home/lankvil/.freeconf/packages/apache/test_include.xsl" /-->
</xsl:stylesheet>

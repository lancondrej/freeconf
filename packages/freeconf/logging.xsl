<?xml version="1.0"?>


<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">


<xsl:output method="text" indent="no"/>

<!-- ############################################################ -->
<!-- ######################TEMPLATE CALLING##################### -->


    <xsl:template match="container[@name='logging']">
       <xsl:text>
[loggers]
keys=root, Model, Presenter, View, IO

[handlers]
keys=consoleHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=ERROR
handlers=consoleHandler
        </xsl:text>
        <xsl:for-each select="entry">
            <xsl:text>
[logger_</xsl:text>
            <xsl:value-of select="@name"/>
            <xsl:text>]</xsl:text>
            <xsl:text>
level=</xsl:text>
            <xsl:value-of select="."/>
            <xsl:text>
handlers=consoleHandler
qualname=</xsl:text>
               <xsl:value-of select="@name"/>
            <xsl:text>
propagate=0
            </xsl:text>
        </xsl:for-each>

        <xsl:text>
[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=simpleFormatter
args=(sys.stdout,)

[formatter_simpleFormatter]
format=%(asctime)s %(levelname)s: %(name)s log from %(funcName)s in module %(module)s: %(message)s
        </xsl:text>
    </xsl:template>
</xsl:stylesheet>

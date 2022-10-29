<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:msxsl="urn:schemas-microsoft-com:xslt" exclude-result-prefixes="msxsl" xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xsl:output method="xml" indent="yes" />
    <xsl:param name="root" />
    <xsl:param name="codee-root" />
    <xsl:include href="../CommonXsltTemplates.xslt"/>
    <xsl:param name="exclude-collections" select="'false'" />
    <xsl:param name="relationship-suffix" select="''" />
    <xsl:variable name="airtable" select="/" />
    <xsl:variable name="squot">'</xsl:variable>
    <xsl:variable name="init-space">             </xsl:variable>
    <xsl:include href="GnfCommon.xslt"/>

    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()" />
        </xsl:copy>
    </xsl:template>

    <xsl:template match="/">
        <FileSet>
            <FileSetFiles>
                <xsl:for-each select="$airtable//GtEnums/GtEnum[(normalize-space(Alias) !='' and Status='Active' and (SpaceheatRegistrySchema='true' or BaseGridworksSchema='true'))]">
                    <xsl:variable name="enum-alias" select="Alias" />
                    <xsl:variable name="enum-name-style" select="PythonEnumNameStyle" />
                    <xsl:variable name="class-name">
                        <xsl:call-template name="nt-case">
                            <xsl:with-param name="mp-schema-text" select="Alias" />
                        </xsl:call-template>
                    </xsl:variable>
                    <xsl:variable name="local-class-name">
                        <xsl:call-template name="nt-case">
                            <xsl:with-param name="mp-schema-text" select="LocalName" />
                        </xsl:call-template>
                    </xsl:variable>
                    <xsl:variable name="enum-id" select="GtEnumId"/>
                    <FileSetFile>
                                <xsl:element name="RelativePath"><xsl:text>../../../../python_test/enums/</xsl:text>
                                <xsl:value-of select="translate(LocalName,'.','_')"/><xsl:text>_test.py</xsl:text></xsl:element>

                        <OverwriteMode>Always</OverwriteMode>
                        <xsl:element name="FileContents">


<xsl:text>"""Tests for scehma enum </xsl:text><xsl:value-of select="$enum-alias"/><xsl:text>"""

import pytest

from errors import SchemaError

from enums.</xsl:text><xsl:value-of select="translate(LocalName,'.','_')"/><xsl:text>_map import (
    </xsl:text><xsl:value-of select="$local-class-name"/>
<xsl:text>,
    </xsl:text><xsl:value-of select="$local-class-name"/><xsl:text>SchemaEnum,
    </xsl:text><xsl:value-of select="$local-class-name"/><xsl:text>Map as Map,
)


def test_component_category():

    assert set(</xsl:text><xsl:value-of select="$local-class-name"/><xsl:text>.values()) == set(
        [
            </xsl:text>
    <xsl:for-each select="$airtable//EnumSymbols/EnumSymbol[(Enum = $enum-id)]">
        <xsl:text>"</xsl:text>
        <xsl:value-of select="LocalValue"/>
        <xsl:text>",
            </xsl:text>
        </xsl:for-each>
    <xsl:text>]
    )

    assert set(</xsl:text><xsl:value-of select="$local-class-name"/><xsl:text>SchemaEnum.symbols) == set(
        [
            </xsl:text>
    <xsl:for-each select="$airtable//EnumSymbols/EnumSymbol[(Enum = $enum-id)]">
        <xsl:text>"</xsl:text>
        <xsl:value-of select="Symbol"/>
        <xsl:text>",
            </xsl:text>
        </xsl:for-each>
    <xsl:text>]
    )

    assert len(</xsl:text><xsl:value-of select="$local-class-name"/><xsl:text>.values()) == len(</xsl:text><xsl:value-of select="$local-class-name"/><xsl:text>SchemaEnum.symbols)
</xsl:text>
    <xsl:for-each select="$airtable//EnumSymbols/EnumSymbol[(Enum = $enum-id)]">

    <xsl:text>
    assert Map.type_to_local("</xsl:text>
        <xsl:value-of select="Symbol"/>
        <xsl:text>") == </xsl:text><xsl:value-of select="$local-class-name"/><xsl:text>.</xsl:text>
        <xsl:if test="$enum-name-style = 'Upper'">
        <xsl:value-of select="translate(translate(LocalValue,'-',''),$lcletters, $ucletters)"/>
        </xsl:if>
        <xsl:if test="$enum-name-style ='UpperPython'">
        <xsl:call-template name="upper-python-case">
            <xsl:with-param name="camel-case-text" select="translate(LocalValue,'-','')" />
        </xsl:call-template>
        </xsl:if>
        </xsl:for-each>

    <xsl:text>

    with pytest.raises(SchemaError):
        Map.type_to_local("aaa")

    with pytest.raises(SchemaError):
        Map.local_to_type("Load")

    for symbol in </xsl:text><xsl:value-of select="$local-class-name"/><xsl:text>SchemaEnum.symbols:
        assert Map.local_to_type(Map.type_to_local(symbol)) == symbol
</xsl:text>


                        </xsl:element>
                     </FileSetFile>
                </xsl:for-each>

            </FileSetFiles>
        </FileSet>
    </xsl:template>


</xsl:stylesheet>

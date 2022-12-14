<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:msxsl="urn:schemas-microsoft-com:xslt" exclude-result-prefixes="msxsl" xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xsl:output method="xml" indent="yes" />
    <xsl:param name="root" />
    <xsl:param name="codee-root" />
    <xsl:include href="../CommonXsltTemplates.xslt"/>
    <xsl:param name="exclude-collections" select="'false'" />
    <xsl:param name="relationship-suffix" select="''" />
    <xsl:variable name="airtable" select="document('Airtable.xml')" />
    <xsl:variable name="odxml" select="/" />
    <xsl:variable name="squot">'</xsl:variable>
    <xsl:variable name="init-space">             </xsl:variable>
    <xsl:include href="GwCommon.xslt"/>

    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()" />
        </xsl:copy>
    </xsl:template>

    <xsl:template match="/">
        <FileSet>
            <FileSetFiles>
                <xsl:for-each select="$airtable//GwEntities/GwEntity[(normalize-space(IsNotDataClass) != 'true' and Name != 'DEdge' and Name != 'DNode' and Name != 'DGraph')]">
                    <xsl:variable name="entity" select="." />
                    <xsl:variable name="od" select="$odxml//ObjectDefs/ObjectDef[Name=$entity/Name]"/>
                    <xsl:variable name="lower-name" select="translate(Name, $ucletters, $lcletters)" />
                    <xsl:variable name="python-odname">
                        <xsl:call-template name="python-case"><xsl:with-param name="camel-case-text" select="Name"  /></xsl:call-template>
                    </xsl:variable>
                    <xsl:variable name="primary-key-name">
                        <xsl:call-template name="python-case"><xsl:with-param name="camel-case-text" select="$entity/PrimaryKeyName"/> </xsl:call-template>
                    </xsl:variable>
                    <xsl:variable name="read-only-properties" select="$od//PropertyDef[(normalize-space(IsReadonly) = 'true' or normalize-space(MatchingMetaData/IsReadonly) = 'true')]"/>
                    <xsl:variable name="basic-properties" select="$od//PropertyDef[normalize-space(IsCollection) != 'true' and normalize-space(MatchingMetaData/IsCollection) != 'true' and normalize-space(IsReadonly) != 'true' and normalize-space(MatchingMetaData/IsReadonly) != 'true' and IsPrimaryKey = 0 and count(Relationships)=0 and Name != 'Definition' and Name !='Description' ]"/>
                    <xsl:variable name="foreign-keys" select="$od//PropertyDef[normalize-space(MatchingMetaData/RelationshipType)='One' and normalize-space(IsCollection) != 'true' and count(Relationships)>0 and normalize-space(MatchingMetaData/IsCollection) != 'true']"/>


                    <FileSetFile>
                        <xsl:element name="RelativePath"><xsl:text>../../data_classes/</xsl:text><xsl:value-of select="$python-odname"/><xsl:text>_base.py</xsl:text></xsl:element>
                        <OverwriteMode>Always</OverwriteMode>
                        <xsl:element name="FileContents" ><xsl:text>""" </xsl:text><xsl:value-of select="$od/Name" /><xsl:text> Base Class Definition """
import time
import uuid
from typing import Optional
from abc import ABC, abstractproperty
from gw.mixin import StreamlinedSerializerMixin


class </xsl:text><xsl:value-of select="$od/Name" /><xsl:text>Base(ABC, StreamlinedSerializerMixin):
    by_id = {}
    </xsl:text><xsl:if test="$entity/HasAliasDict ='true'">
    <xsl:text>by_alias = {}</xsl:text>
    </xsl:if>
<xsl:text>
    base_props = []</xsl:text>
            <xsl:if test="($entity/AllObjectsStaticBool = 0)">
<xsl:text>
    base_props.append('</xsl:text><xsl:value-of select="$primary-key-name"/><xsl:text>')</xsl:text>
            </xsl:if>
    <xsl:for-each select="$basic-properties">
<xsl:text>
    base_props.append('</xsl:text>
       <xsl:call-template name="python-case">
        <xsl:with-param name="camel-case-text" select="Name"  />
    </xsl:call-template>
<xsl:text>')</xsl:text>
    </xsl:for-each>
    <xsl:for-each select="$foreign-keys">
        <xsl:variable name="foreign-object-name" select="Relationships/Relationship/ReferencedObjectDef"/>
        <xsl:variable name="foreign-gw-entity" select="$airtable//GwEntities/GwEntity[Name=$foreign-object-name]"/>
        <xsl:variable name="foreign-primary-key-suffix">
            <xsl:if test="$foreign-gw-entity/AllObjectsStaticBool = 0">
                    <xsl:text>id</xsl:text>
            </xsl:if>
            <xsl:if test="$foreign-gw-entity/AllObjectsStaticBool = 1">
                <xsl:call-template name="python-case">
                    <xsl:with-param name="camel-case-text" select="$foreign-gw-entity/PrimaryKeyName"/>
                </xsl:call-template>
            </xsl:if>
        </xsl:variable>
<xsl:text>
    base_props.append('</xsl:text>
        <xsl:call-template name="python-case">
            <xsl:with-param name="camel-case-text" select="Name"  />
        </xsl:call-template><xsl:text>_</xsl:text>  <xsl:value-of select="$foreign-primary-key-suffix"/><xsl:text>')</xsl:text>
    </xsl:for-each>

    <xsl:text>

    def __new__(cls, </xsl:text><xsl:value-of select="$primary-key-name"/><xsl:text>, *args, **kwargs):
        try:
            return cls.by_id[</xsl:text><xsl:value-of select="$primary-key-name"/><xsl:text>]
        except KeyError:
            instance = super().__new__(cls)
            cls.by_id[</xsl:text><xsl:value-of select="$primary-key-name"/><xsl:text>] = instance
            return instance

    def __init__(self</xsl:text>
                <xsl:if test="$entity/AllObjectsStaticBool = 0">
                <xsl:text>,
                 </xsl:text><xsl:value-of select="$primary-key-name"/><xsl:text>: Optional[str] = None</xsl:text>
</xsl:if>
<xsl:for-each select="$basic-properties">
                 <xsl:text>,
                 </xsl:text>
    <xsl:call-template name="python-case">
        <xsl:with-param name="camel-case-text" select="Name"  />
    </xsl:call-template><xsl:text>: </xsl:text> <xsl:call-template name="get-default-value">
        <xsl:with-param name="propertyDef" select="." />
        </xsl:call-template>
<xsl:text>
   </xsl:text>
</xsl:for-each>
<xsl:for-each select="$foreign-keys">
                 <xsl:text>,
                 </xsl:text>
    <xsl:variable name="foreign-object-name" select="Relationships/Relationship/ReferencedObjectDef"/>
    <xsl:variable name="foreign-gw-entity" select="$airtable//GwEntities/GwEntity[Name=$foreign-object-name]"/>
    <xsl:variable name="foreign-primary-key-suffix">
        <xsl:if test="$foreign-gw-entity/AllObjectsStaticBool = 0">
                <xsl:text>id</xsl:text>
        </xsl:if>
        <xsl:if test="$foreign-gw-entity/AllObjectsStaticBool = 1">
            <xsl:call-template name="python-case">
                <xsl:with-param name="camel-case-text" select="$foreign-gw-entity/PrimaryKeyName"/>
            </xsl:call-template>
        </xsl:if>
    </xsl:variable>
    <xsl:call-template name="python-case">
        <xsl:with-param name="camel-case-text" select="Name"  />
    </xsl:call-template><xsl:text>_</xsl:text>  <xsl:value-of select="$foreign-primary-key-suffix"/>


    <xsl:text>: Optional[str] = None</xsl:text>
</xsl:for-each>
<xsl:text>):</xsl:text>
<xsl:if test="$entity/AllObjectsStaticBool = 0">
    <xsl:text>
        self.</xsl:text>
    <xsl:call-template name="python-case">
        <xsl:with-param name="camel-case-text" select="$od/Name" />
    </xsl:call-template><xsl:text>_id = </xsl:text>
    <xsl:call-template name="python-case">
        <xsl:with-param name="camel-case-text" select="$od/Name" />
    </xsl:call-template><xsl:text>_id</xsl:text>
</xsl:if>
<xsl:for-each select="$basic-properties">
    <xsl:variable name="uc-type" select="translate(DataType, $lcletters, $ucletters)" />
    <xsl:variable name="python-prop-name">
        <xsl:call-template name="python-case">
            <xsl:with-param name="camel-case-text" select="Name"  />
        </xsl:call-template>
    </xsl:variable>
    <xsl:choose>
        <xsl:when test="$uc-type = 'DECIMAL' or $uc-type = 'FLOAT' or $uc-type = 'NUMBER'">
            <xsl:text>
        if </xsl:text><xsl:value-of select="$python-prop-name"/><xsl:text>:
            self.</xsl:text><xsl:value-of select="$python-prop-name"/><xsl:text> = float(</xsl:text><xsl:value-of select="$python-prop-name"/><xsl:text>)
        else:
            self.</xsl:text><xsl:value-of select="$python-prop-name"/><xsl:text> = None</xsl:text>
        </xsl:when>
        <xsl:otherwise><xsl:text>
        self.</xsl:text><xsl:value-of select="$python-prop-name"/><xsl:text> = </xsl:text><xsl:value-of select="$python-prop-name"/>
        </xsl:otherwise>
    </xsl:choose>

</xsl:for-each>
<xsl:for-each select="$foreign-keys">
    <xsl:variable name="foreign-object-name" select="Relationships/Relationship/ReferencedObjectDef"/>
    <xsl:variable name="foreign-gw-entity" select="$airtable//GwEntities/GwEntity[Name=$foreign-object-name]"/>
    <xsl:variable name="foreign-primary-key-suffix">
        <xsl:if test="$foreign-gw-entity/AllObjectsStaticBool = 0">
                <xsl:text>id</xsl:text>
        </xsl:if>
        <xsl:if test="$foreign-gw-entity/AllObjectsStaticBool = 1">
            <xsl:call-template name="python-case">
                <xsl:with-param name="camel-case-text" select="$foreign-gw-entity/PrimaryKeyName"/>
            </xsl:call-template>
        </xsl:if>
    </xsl:variable>
    <xsl:text>
        self.</xsl:text>
    <xsl:call-template name="python-case">
        <xsl:with-param name="camel-case-text" select="Name"  />
    </xsl:call-template><xsl:text>_</xsl:text> <xsl:value-of select="$foreign-primary-key-suffix"/>
    <xsl:text> = </xsl:text>
    <xsl:call-template name="python-case">
        <xsl:with-param name="camel-case-text" select="Name"  />
    </xsl:call-template><xsl:text>_</xsl:text> <xsl:value-of select="$foreign-primary-key-suffix"/>
</xsl:for-each>
        <xsl:if test="$entity/HasAliasDict ='true'">
    <xsl:text>
        self.__class__.by_alias[self.alias] = self
            </xsl:text>
        </xsl:if>



<xsl:if test="$entity/AllObjectsStaticBool = 0">
<xsl:text>

    @classmethod
    def check_uniqueness_of_primary_key(cls, attributes):
        if attributes['</xsl:text><xsl:value-of select="$python-odname"/><xsl:text>_id'] in cls.by_id.keys():
            raise Exception(f"</xsl:text><xsl:value-of select="$python-odname"/><xsl:text>_id {attributes['</xsl:text><xsl:value-of select="$python-odname"/><xsl:text>_id']} already in use")

</xsl:text>
</xsl:if>
<xsl:text>
    """ Derived attributes """
</xsl:text>
<xsl:for-each select="$read-only-properties">
    <xsl:variable name="ax-name"><xsl:value-of select="$od/Name"  />__<xsl:value-of select="Name"/></xsl:variable>
<xsl:text>
    @abstractproperty
    def </xsl:text>
    <xsl:call-template name="python-case">
        <xsl:with-param name="camel-case-text" select="Name"  />
    </xsl:call-template><xsl:text>(self):
        </xsl:text>
        <xsl:call-template name="axiom-def">
            <xsl:with-param name="axiom-name" select="$ax-name"/>
        </xsl:call-template>
    &#x20; &#x20; raise NotImplementedError
</xsl:for-each>


</xsl:element>
                    </FileSetFile>
                    <FileSetFile>
                        <xsl:element name="RelativePath"><xsl:text>../../data_classes/</xsl:text><xsl:value-of select="$python-odname"   /><xsl:text>.py</xsl:text></xsl:element>
                        <OverwriteMode>Never</OverwriteMode>
                        <xsl:element name="FileContents"><xsl:text>""" </xsl:text><xsl:value-of select="$od/Name" /><xsl:text> Class Definition """
import time
import uuid
from data_classes.</xsl:text><xsl:value-of select="$python-odname"/><xsl:text>_base import </xsl:text><xsl:value-of select="$od/Name" /><xsl:text>Base

</xsl:text>
<xsl:for-each select="$foreign-keys">
<xsl:variable name="foreign-object-name" select="Relationships/Relationship/ReferencedObjectDef"/>
<xsl:variable name="foreign-gw-entity" select="$airtable//GwEntities/GwEntity[Name=$foreign-object-name]"/>
<xsl:text>from data_classes.</xsl:text>
<xsl:call-template name="python-case">
    <xsl:with-param name="camel-case-text" select="$foreign-gw-entity/Name"  />
</xsl:call-template>
<xsl:text> import </xsl:text><xsl:value-of select="$foreign-gw-entity/Name"/>
<xsl:text> #
</xsl:text>
<xsl:if test="$foreign-gw-entity/AllObjectsStaticBool = 1">
<xsl:text>from data_classes.</xsl:text>
<xsl:call-template name="python-case">
    <xsl:with-param name="camel-case-text" select="$foreign-gw-entity/Name"  />
</xsl:call-template><xsl:text>_static import Platform</xsl:text><xsl:value-of select="$foreign-gw-entity/Name"/>
<xsl:text> #
</xsl:text>
</xsl:if>

</xsl:for-each>
<xsl:text>
class </xsl:text><xsl:value-of select="$od/Name" /><xsl:text>(</xsl:text><xsl:value-of select="$od/Name" /><xsl:text>Base):
</xsl:text>
<xsl:if test="$entity/AllObjectsStaticBool = 0">
<xsl:text>
    @classmethod
    def check_existence_of_certain_attributes(cls, attributes):
        if not '</xsl:text><xsl:value-of select="$python-odname"/><xsl:text>_id' in attributes.keys():
            raise Exception('</xsl:text><xsl:value-of select="$python-odname"/><xsl:text>_id must exist')

    @classmethod
    def check_initialization_consistency(cls, attributes):
        </xsl:text><xsl:value-of select="$od/Name" /><xsl:text>.check_uniqueness_of_primary_key(attributes)
        </xsl:text><xsl:value-of select="$od/Name" /><xsl:text>.check_existence_of_certain_attributes(attributes)

    def check_immutability_for_existing_attributes(self, new_attributes):
        if self.</xsl:text><xsl:value-of select="$python-odname"/><xsl:text>_id:
            if new_attributes['</xsl:text><xsl:value-of select="$python-odname"/><xsl:text>_id'] != self.</xsl:text><xsl:value-of select="$python-odname"/><xsl:text>_id:
                raise Exception('</xsl:text><xsl:value-of select="$python-odname"/><xsl:text>_id is Immutable')

    def check_update_consistency(self, new_attributes):
        self.check_immutability_for_existing_attributes(new_attributes)
</xsl:text>
</xsl:if>
<xsl:text>

    """ Derived attributes """
</xsl:text>

<xsl:for-each select="$read-only-properties">
<xsl:text>    @property
    def </xsl:text>
        <xsl:call-template name="python-case">
            <xsl:with-param name="camel-case-text" select="Name"  />
        </xsl:call-template><xsl:text>(self) -> str:
        raise NotImplementedError

</xsl:text>

</xsl:for-each>
<xsl:text>
    """Static foreign objects referenced by their keys """

</xsl:text>
<xsl:for-each select="$foreign-keys">
    <xsl:variable name="foreign-object-name" select="Relationships/Relationship/ReferencedObjectDef"/>
    <xsl:variable name="foreign-gw-entity" select="$airtable//GwEntities/GwEntity[Name=$foreign-object-name]"/>
    <xsl:if test="$foreign-gw-entity/AllObjectsStaticBool = 1">
    <xsl:variable name="primary-key">
        <xsl:call-template name="python-case">
            <xsl:with-param name="camel-case-text" select="Name"  />
        </xsl:call-template><xsl:text>_</xsl:text>
        <xsl:call-template name="python-case">
            <xsl:with-param name="camel-case-text" select="$foreign-gw-entity/PrimaryKeyName"/>
        </xsl:call-template>
    </xsl:variable>
    <xsl:text>    @property
    def </xsl:text>
    <xsl:call-template name="python-case">
        <xsl:with-param name="camel-case-text" select="Name"  />
    </xsl:call-template>
    <xsl:text>(self):
        if (self.</xsl:text><xsl:value-of select="$primary-key"/><xsl:text> is None):
            return None
        elif not(self.</xsl:text><xsl:value-of select="$primary-key"/><xsl:text> in Platform</xsl:text>
        <xsl:value-of select="$foreign-gw-entity/Name"/><xsl:text>.keys()):
            raise TypeError('</xsl:text><xsl:value-of select="$foreign-gw-entity/Name"/><xsl:text> must belong to Static List')
        else:
            return Platform</xsl:text><xsl:value-of select="$foreign-gw-entity/Name"/><xsl:text>[self.</xsl:text>
        <xsl:value-of select="$primary-key"/>  <xsl:text>]

</xsl:text>

    </xsl:if>

</xsl:for-each>
</xsl:element>
                    </FileSetFile>
                </xsl:for-each>

            </FileSetFiles>
        </FileSet>
    </xsl:template>
    <xsl:template name="get-default-value">
        <xsl:param name="propertyDef" />
        <xsl:variable name="uc-type" select="translate($propertyDef/DataType, $lcletters, $ucletters)" />
        <xsl:choose>
            <xsl:when test="$uc-type = 'NTEXT' or $uc-type = 'TEXT' or $uc-type = 'STRING'"><xsl:text>Optional[str] = None</xsl:text>
            </xsl:when>
            <xsl:when test="$uc-type = 'INT16' or $uc-type = 'INT32' or $uc-type = 'INT64' or $uc-type = 'INT'"><xsl:text>Optional[int] = None</xsl:text></xsl:when>
            <xsl:when test="$uc-type = 'BOOLEAN' or $uc-type = 'BOOL'"><xsl:text>Optional[bool] = None</xsl:text></xsl:when>
            <xsl:when test="$uc-type = 'DECIMAL' or $uc-type = 'FLOAT' or $uc-type = 'NUMBER'"><xsl:text>Optional[float] = None</xsl:text> </xsl:when>
            <xsl:when test="$uc-type = 'DATE'"><xsl:text>time = time.time()</xsl:text> </xsl:when>
            <xsl:when test="$uc-type = 'DATETIME'"><xsl:text>time = time.time()</xsl:text> </xsl:when>
            <xsl:when test="$uc-type = 'GUID'"><xsl:text>uuid.uuid4() = uuid.uuid4()</xsl:text></xsl:when>
            <xsl:otherwise><xsl:text>None</xsl:text>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>





</xsl:stylesheet>

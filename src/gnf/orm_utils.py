from typing import List
from typing import Optional

import gnf.property_format as property_format
from gnf.data_classes import BaseGNode
from gnf.django_related.models import BaseGNodeDb
from gnf.django_related.models import GpsPointDb
from gnf.schemata import BasegnodeGt
from gnf.schemata import BasegnodeGt_Maker


def load_g_nodes_as_data_classes():
    """Loads all objects in GNodeFactoryDb and GpsPointDb into
    the respective class Dicts
    """
    for gpsdb in GpsPointDb.objects.all():
        gpsdb.dc
    for gndb in BaseGNodeDb.objects.all():
        gndb.dc


def retrieve_all_gns() -> List[BasegnodeGt]:
    gns = BaseGNodeDb.objects.all()
    gn_gt_list = []
    for gn in gns:
        gn_gt = BasegnodeGt_Maker.dc_to_tuple(gn.dc)
        gn_gt_list.append(gn_gt)
    return gn_gt_list


def retrieve_gn(lrh_g_node_alias: str) -> Optional[BasegnodeGt]:
    if not property_format.is_lrh_alias_format(lrh_g_node_alias):
        raise ValueError(f"{lrh_g_node_alias} must have LRH Alias Format")
    g_node_alias = lrh_g_node_alias.replace("-", ".")
    gn = BaseGNodeDb.objects.filter(alias=g_node_alias).first()
    if not gn:
        return None
    gn_gt = BasegnodeGt_Maker.dc_to_tuple(gn.dc)
    return gn_gt


def gn_from_alias(g_node_alias: str) -> Optional[BaseGNode]:
    r = BaseGNodeDb.objects.filter(alias=g_node_alias)
    if len(r) == 0:
        return None
    gndb = r[0]
    return gndb.dc

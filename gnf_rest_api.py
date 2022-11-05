from fastapi import FastAPI
from fastapi import HTTPException

import gnf.config as config
import gnf.property_format as property_format
from gnf.g_node_factory_db import GNodeFactoryDb
from gnf.schemata import BasegnodeGt
from gnf.schemata import BasegnodeGt_Maker
from gnf.schemata import InitialTadeedAlgoOptin
from gnf.schemata import NewTadeedAlgoOptin
from gnf.schemata import OldTadeedAlgoReturn
from gnf.utils import RestfulResponse


app = FastAPI()

factory = GNodeFactoryDb(config.GnfSettings())


@app.get("/base-g-nodes/{lrh_g_node_alias}", response_model=BasegnodeGt)
async def read_base_g_node(lrh_g_node_alias: str):
    if not property_format.is_lrh_alias_format(lrh_g_node_alias):
        raise ValueError(f"{lrh_g_node_alias} must have LRH Alias Format")
    g_node_alias = lrh_g_node_alias.replace("-", ".")
    gn = factory.get_base_g_node(g_node_alias)
    gn_gt = BasegnodeGt_Maker.dc_to_tuple(gn)
    return gn_gt

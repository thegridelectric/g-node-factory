from typing import List
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI

import gnf.orm_utils as orm_utils
from gnf.schemata import BasegnodeGt


# Create FasatAPI instance
app = FastAPI()


@app.get("/base-g-nodes/")
async def get_base_g_nodes(
    gns: List[BasegnodeGt] = Depends(orm_utils.retrieve_all_gns),
):
    return gns


@app.get("/base-g-nodes/{lrh_g_node_alias}")
async def get_base_g_node(gn: BasegnodeGt = Depends(orm_utils.retrieve_gn)):
    return gn

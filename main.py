from functools import lru_cache

from fastapi import Depends
from fastapi import FastAPI
from pydantic import BaseModel

import gnf.property_format as property_format
from gnf.config import FastAPISettings as Settings
from gnf.data_classes import BaseGNode
from gnf.schemata import BasegnodeGt
from gnf.schemata import BasegnodeGt_Maker
from gnf.schemata import NewTadeedAlgoOptin


class Item(BaseModel):
    name: str
    description: str | None = None


app = FastAPI()


@app.post("/optin-tadeed-algo/")
async def optin_tadeed_algo_received(payload: NewTadeedAlgoOptin):
    return payload


#####################
# using settings
#####################


@lru_cache()
def get_settings():
    return Settings()


@app.get("/info")
async def info(settings: Settings = Depends(get_settings)):
    return {
        "port": settings.port,
    }


d = {
    "GNodeId": "7b1df82e-10c5-49d9-8d02-1e837e31b87e",
    "Alias": "d1",
    "StatusGtEnumSymbol": "153d3475",
    "RoleGtEnumSymbol": "00000000",
    "GNodeRegistryAddr": "MONSDN5MXG4VMIOHJNCJJBVASG7HEZQSCEIKJAPEPVI5ZJUMQGXQKSOAYU",
    "TypeName": "basegnode.gt",
    "Version": "020",
}

root_dc = BasegnodeGt_Maker.dict_to_dc(d)

d = {
    "GNodeId": "c0119953-a48f-495d-87cc-58fb92eb4cee",
    "Alias": "d1.isone",
    "StatusGtEnumSymbol": "153d3475",
    "RoleGtEnumSymbol": "4502e355",
    "GNodeRegistryAddr": "MONSDN5MXG4VMIOHJNCJJBVASG7HEZQSCEIKJAPEPVI5ZJUMQGXQKSOAYU",
    "TypeName": "basegnode.gt",
    "Version": "020",
}
isone = BasegnodeGt_Maker.dict_to_dc(d)


@app.get("/")
async def root():
    return {"message": "Hello World"}


# http://127.0.0.1:8000/items/foo
@app.get("/items/{item_id}")
async def read_item(item_id: str):
    return {"item_id": item_id}


# http://127.0.0.1:8000/items/foo produces an error
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


# http://127.0.0.1:8000/basegnodes/d1
@app.get("/basegnodes/{lrh_g_node_alias}", response_model=BasegnodeGt)
async def read_base_g_node(lrh_g_node_alias: str):
    if not property_format.is_lrh_alias_format(lrh_g_node_alias):
        raise ValueError(f"{lrh_g_node_alias} must have LRH Alias Format")
    g_node_alias = lrh_g_node_alias.replace("-", ".")
    if g_node_alias in BaseGNode.by_alias.keys():
        gn = BaseGNode.by_alias[g_node_alias]
        gn_gt = BasegnodeGt_Maker.dc_to_tuple(gn)
    return gn_gt

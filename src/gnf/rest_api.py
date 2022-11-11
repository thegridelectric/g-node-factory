from functools import lru_cache
from typing import List

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException

import gnf.config as config
import gnf.gnf_db as gnf_db
from gnf.schemata import BasegnodeGt
from gnf.schemata import InitialTadeedAlgoCreate
from gnf.schemata import InitialTadeedAlgoTransfer
from gnf.schemata import TavalidatorcertAlgoCreate
from gnf.schemata import TavalidatorcertAlgoTransfer
from gnf.utils import RestfulResponse


# Create FasatAPI instance
app = FastAPI()


@lru_cache()
def get_settings():
    return config.GnfSettings()


@app.get("/base-g-nodes/{lrh_g_node_alias}", response_model=BasegnodeGt)
async def get_base_g_node(lrh_g_node_alias: str):
    gn = await gnf_db.g_node_from_alias(lrh_g_node_alias)
    return gn


@app.get("/base-g-nodes/", response_model=List[BasegnodeGt])
async def get_base_g_nodes():
    gns = await gnf_db.retrieve_all_gns()
    return gns


@app.get("/base-g-nodes/by-id/{g_node_id}", response_model=BasegnodeGt)
async def get_base_g_node(g_node_id: str):
    gn = await gnf_db.g_node_from_id(g_node_id)
    return gn


@app.post("/tavalidatorcert-algo-create/", response_model=RestfulResponse)
async def tavalidatorcert_algo_create_received(
    payload: TavalidatorcertAlgoCreate,
    settings: config.GnfSettings = Depends(get_settings),
):
    r = gnf_db.tavalidatorcert_algo_create_received(payload=payload, settings=settings)
    if r.HttpStatusCode > 200:
        raise HTTPException(
            status_code=r.HttpStatusCode, detail=f"[{r.HttpStatusCode}]: {r.Note}"
        )
    return r


@app.post("/tavalidatorcert-algo-transfer/", response_model=RestfulResponse)
async def tavalidatorcert_algo_transfer_received(
    payload: TavalidatorcertAlgoTransfer,
    settings: config.GnfSettings = Depends(get_settings),
):
    r = gnf_db.tavalidatorcert_algo_transfer_received(
        payload=payload, settings=settings
    )
    if r.HttpStatusCode > 200:
        raise HTTPException(
            status_code=r.HttpStatusCode, detail=f"[{r.HttpStatusCode}]: {r.Note}"
        )
    return r


@app.post("/initial-tadeed-algo-create/", response_model=RestfulResponse)
async def initial_tadeed_algo_create_received(
    payload: InitialTadeedAlgoCreate,
    settings: config.GnfSettings = Depends(get_settings),
):
    r = await gnf_db.initial_tadeed_algo_create_received(
        payload=payload,
        settings=settings,
    )
    if r.HttpStatusCode > 200:
        raise HTTPException(
            status_code=r.HttpStatusCode, detail=f"[{r.HttpStatusCode}]: {r.Note}"
        )
    return r


@app.post("/initial-tadeed-algo-transfer/", response_model=RestfulResponse)
async def initial_tadeed_algo_transfer_received(
    payload: InitialTadeedAlgoTransfer,
    settings: config.GnfSettings = Depends(get_settings),
):
    r = await gnf_db.initial_tadeed_algo_transfer_received(
        payload=payload,
        settings=settings,
    )
    if r.HttpStatusCode > 200:
        raise HTTPException(
            status_code=r.HttpStatusCode, detail=f"[{r.HttpStatusCode}]: {r.Note}"
        )
    return r

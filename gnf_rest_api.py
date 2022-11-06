from functools import lru_cache
from typing import List
from typing import Optional

from algosdk import encoding
from algosdk.v2client.algod import AlgodClient
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException

import gnf.algo_utils as algo_utils
import gnf.config as config
import gnf.orm_utils as orm_utils
from gnf.algo_utils import PendingTxnResponse
from gnf.schemata import BasegnodeGt
from gnf.schemata import InitialTadeedAlgoCreate
from gnf.schemata import TavalidatorcertAlgoCreate
from gnf.schemata import TavalidatorcertAlgoTransfer
from gnf.utils import RestfulResponse


# Create FasatAPI instance
app = FastAPI()


@lru_cache()
def get_settings():
    return config.GnfSettings()


@app.get("/base-g-nodes/")
async def get_base_g_nodes(
    gns: List[BasegnodeGt] = Depends(orm_utils.retrieve_all_gns),
):
    return gns


@app.get("/base-g-nodes/{lrh_g_node_alias}")
async def get_base_g_node(gn: BasegnodeGt = Depends(orm_utils.g_node_from_alias)):
    return gn


@app.get("/base-g-nodes/by-id/{g_node_id}")
async def get_base_g_node(gn: BasegnodeGt = Depends(orm_utils.g_node_from_id)):
    return gn


@app.post("/tavalidatorcert-algo-create/", response_model=RestfulResponse)
async def tavalidatorcert_algo_create_received(
    payload: TavalidatorcertAlgoCreate,
    settings: config.GnfSettings = Depends(get_settings),
):
    r = orm_utils.tavalidatorcert_algo_create_received(
        payload=payload, settings=settings
    )
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
    r = orm_utils.tavalidatorcert_algo_transfer_received(
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
    r = orm_utils.initial_tadeed_algo_create_received(
        payload=payload,
        settings=settings,
    )
    if r.HttpStatusCode > 200:
        raise HTTPException(
            status_code=r.HttpStatusCode, detail=f"[{r.HttpStatusCode}]: {r.Note}"
        )
    return r


@app.get(
    "/hack-create-atomic-metering-node/{lrh_ta_alias}/{ta_deed_idx}",
    response_model=RestfulResponse,
)
async def hack_create_pending_atomic_metering_node(
    r=Depends(orm_utils.create_pending_atomic_metering_node),
):
    return r

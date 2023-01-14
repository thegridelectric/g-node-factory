from functools import lru_cache
from typing import Dict
from typing import List

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import FileResponse
from pydantic import ValidationError

import gnf.config as config
from gnf.gnf_db import GNodeFactory
from gnf.types import BaseGNodeGt
from gnf.types import DiscoverycertAlgoCreate
from gnf.types import DiscoverycertAlgoCreate_Maker
from gnf.types import InitialTadeedAlgoCreate
from gnf.types import InitialTadeedAlgoTransfer
from gnf.types import TavalidatorcertAlgoCreate
from gnf.types import TavalidatorcertAlgoTransfer
from gnf.utils import RestfulResponse


# Create FasatAPI instance
app = FastAPI()

gnf = GNodeFactory()


@lru_cache()
def get_settings():
    return config.Public()


@app.get("/settings/")
async def settings():
    settings = get_settings()
    return settings


@app.get("/base-g-nodes/{g_node_alias}", response_model=BaseGNodeGt)
async def get_base_g_node(g_node_alias: str):
    gn = await gnf.g_node_from_alias(g_node_alias)
    return gn


@app.get("/base-g-nodes/", response_model=List[BaseGNodeGt])
async def get_base_g_nodes():
    gns = await gnf.retrieve_all_gns()
    return gns


@app.get("/base-g-nodes/by-id/{g_node_id}", response_model=BaseGNodeGt)
async def get_base_g_node(g_node_id: str):
    gn = await gnf.g_node_from_id(g_node_id)
    return gn


@app.post(f"/pause-time/")
async def pause_time():
    gnf.pause_time()


@app.post(f"/resume-time/")
async def resume_time():
    gnf.resume_time()


@app.post(f"/debug-tc-reinitialize-time/")
async def debug_tc_reinitialize_time():
    gnf.debug_tc_reinitialize_time()


@app.post("/tavalidatorcert-algo-create/", response_model=RestfulResponse)
async def tavalidatorcert_algo_create_received(
    payload: TavalidatorcertAlgoCreate,
):
    r = gnf.tavalidatorcert_algo_create_received(payload=payload)
    if r.HttpStatusCode > 200:
        raise HTTPException(
            status_code=r.HttpStatusCode, detail=f"[{r.HttpStatusCode}]: {r.Note}"
        )
    return r


@app.post("/tavalidatorcert-algo-transfer/", response_model=RestfulResponse)
async def tavalidatorcert_algo_transfer_received(
    payload: TavalidatorcertAlgoTransfer,
):
    r = gnf.tavalidatorcert_algo_transfer_received(payload=payload)
    if r.HttpStatusCode > 200:
        raise HTTPException(
            status_code=r.HttpStatusCode, detail=f"[{r.HttpStatusCode}]: {r.Note}"
        )
    return r


@app.post("/initial-tadeed-algo-create/", response_model=RestfulResponse)
async def initial_tadeed_algo_create_received(
    payload: InitialTadeedAlgoCreate,
):
    r = await gnf.initial_tadeed_algo_create_received(
        payload=payload,
    )

    if r.HttpStatusCode > 200:
        raise HTTPException(
            status_code=r.HttpStatusCode,
            detail=f"[{r.HttpStatusCode}]: /initial-tadeed-algo-create/ {r.Note}",
        )

    return RestfulResponse(
        Note="/initial-tadeed-algo-create/: " + r.Note,
        HttpStatusCode=r.HttpStatusCode,
        PayloadTypeName=r.PayloadTypeName,
        PayloadAsDict=r.PayloadAsDict,
    )


@app.post("/initial-tadeed-algo-transfer/", response_model=RestfulResponse)
async def initial_tadeed_algo_transfer_received(
    payload: InitialTadeedAlgoTransfer,
):
    r = await gnf.initial_tadeed_algo_transfer_received(
        payload=payload,
    )
    if r.HttpStatusCode > 200:
        raise HTTPException(
            status_code=r.HttpStatusCode, detail=f"[{r.HttpStatusCode}]: {r.Note}"
        )
    return r


@app.post("/discoverycert-algo-create/")
async def discovercert_algo_create_received(
    payload_dict: Dict,
):
    try:
        payload = DiscoverycertAlgoCreate_Maker.dict_to_tuple(payload_dict)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"{e}")
    r = await gnf.discoverycert_algo_create_received(
        payload=payload,
    )
    if r is None:
        return None
    if r.HttpStatusCode > 200:
        raise HTTPException(
            status_code=r.HttpStatusCode, detail=f"[{r.HttpStatusCode}]: {r.Note}"
        )
    return r

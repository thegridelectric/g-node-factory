from fastapi import FastAPI
from fastapi import HTTPException

import gnf.config as config
from gnf.python_ta_daemon import PythonTaDaemon
from gnf.schemata import InitialTadeedAlgoOptin
from gnf.schemata import NewTadeedAlgoOptin
from gnf.schemata import OldTadeedAlgoReturn
from gnf.utils import RestfulResponse


app = FastAPI()

daemon = PythonTaDaemon(
    sk=config.HollyTaDaemonSettings().sk.get_secret_value(),
    ta_owner_addr=config.SandboxDemo().holly_homeowner_addr,
    algo_settings=config.Algo(),
)


@app.post("/initial-tadeed-algo-optin/", response_model=RestfulResponse)
async def initial_tadeed_algo_optin_received(payload: InitialTadeedAlgoOptin):
    r = daemon.initial_tadeed_algo_optin_received(payload)
    if r.HttpStatusCode > 200:
        raise HTTPException(
            status_code=r.HttpStatusCode, detail=f"[{r.HttpStatusCode}]: {r.Note}"
        )
    return r


@app.post("/new-tadeed-algo-optin/", response_model=RestfulResponse)
async def new_tadeed_algo_received(payload: NewTadeedAlgoOptin):
    r = daemon.new_tadeed_algo_optin_received(payload)
    if r.HttpStatusCode > 200:
        raise HTTPException(
            status_code=r.HttpStatusCode, detail=f"[{r.HttpStatusCode}]: {r.Note}"
        )
    return r


@app.post("/old-tadeed-algo-return/", response_model=RestfulResponse)
async def old_tadeed_algo_return_received(payload: OldTadeedAlgoReturn):
    r = daemon.old_tadeed_algo_return_received(payload)
    if r.HttpStatusCode > 200:
        raise HTTPException(
            status_code=r.HttpStatusCode, detail=f"[{r.HttpStatusCode}]: {r.Note}"
        )
    return r

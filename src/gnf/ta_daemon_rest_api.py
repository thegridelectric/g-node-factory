from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi import HTTPException

from gnf.python_ta_daemon import PythonTaDaemon
from gnf.schemata import InitialTadeedAlgoOptin
from gnf.schemata import NewTadeedAlgoOptin
from gnf.schemata import OldTadeedAlgoReturn
from gnf.utils import RestfulResponse


app = FastAPI()
daemon = PythonTaDaemon()

@app.get("/")
async def main():
    if not daemon.has_real_acct():
        return {"TaDaemonAddr": "None Yet"}
    #return {"TaDaemonAddr": daemon.acct.addr}
    #return {"Owned deeds": daemon.ta_deed_alias_list()}
    return FileResponse("docs/wiki/img/terminal-asset-deed-icon.png")

@app.get("/env/")
async def show_env():
    return daemon.settings

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

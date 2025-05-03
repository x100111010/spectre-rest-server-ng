# encoding: utf-8
import hashlib

from pydantic import BaseModel

from server import app, spectred_client


class SpectredInfoResponse(BaseModel):
    mempoolSize: str = "1"
    serverVersion: str = "0.3.14"
    isUtxoIndexed: bool = True
    isSynced: bool = True
    p2pIdHashed: str = (
        "60e486d2ae827248a67a68e9123509204a8b6d9bbb14809347914c9d2873740c"
    )


@app.get(
    "/info/spectred", response_model=SpectredInfoResponse, tags=["Spectre network info"]
)
async def get_spectred_info():
    """
    Get some information for Spectred instance, which is currently connected.
    """
    resp = await spectred_client.request("getInfoRequest")
    p2p_id = resp["getInfoResponse"].pop("p2pId")
    resp["getInfoResponse"]["p2pIdHashed"] = hashlib.sha256(p2p_id.encode()).hexdigest()
    return resp["getInfoResponse"]

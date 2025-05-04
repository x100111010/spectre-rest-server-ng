# encoding: utf-8
from typing import List

from fastapi import HTTPException
from pydantic import BaseModel

from server import app, spectred_client


class AcceptedTransactionIdsModel(BaseModel):
    acceptingBlockHash: str = (
        "78c1492fa4c88f3ef1c3b14d3bc228a09fdd49c9b224571924b8e256806a495b"
    )
    acceptedTransactionIds: List[str] = [
        "eb5b16f01d209e036c5b7e2674fb9fd63c4c5b399b1b10d8daef2369c07e676c",
        "2f37c0fb935cfcee07cfe2494453a4899f2415fad77dd2cfc058d9109de52e71",
    ]


class VscpResponse(BaseModel):
    removedChainBlockHashes: List[str] = []
    addedChainBlockHashes: List[str] = []
    acceptedTransactionIds: List[AcceptedTransactionIdsModel]


@app.get(
    "/info/get-vscp-from-block",
    response_model=VscpResponse,
    tags=["Spectre network info"],
)
async def get_virtual_selected_parent_chain_from_block(
    startHash: str, includeAcceptedTransactionIds: bool = True
):
    """
    getVirtualChainFromBlockRequest requests the virtual selected parent chain from a specified
    startHash to the current virtual block in Spectred.
    """
    resp = await spectred_client.request(
        "getVirtualChainFromBlockRequest",
        params={
            "startHash": startHash,
            "includeAcceptedTransactionIds": includeAcceptedTransactionIds,
        },
    )
    resp = resp["getVirtualChainFromBlockResponse"]

    if resp.get("error"):
        raise HTTPException(400, detail=resp.get("error").get("message"))

    return resp

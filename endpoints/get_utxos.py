# encoding: utf-8
import re
from typing import List

from fastapi import Path, HTTPException
from spectre_script_address import to_script
from pydantic import BaseModel
from starlette.responses import Response

from constants import REGEX_SPECTRE_ADDRESS, ADDRESS_EXAMPLE
from server import app, spectred_client


class OutpointModel(BaseModel):
    transactionId: str = (
        "ef62efbc2825d3ef9ec1cf9b80506876ac077b64b11a39c8ef5e028415444dc9"
    )
    index: int = 0


class ScriptPublicKeyModel(BaseModel):
    scriptPublicKey: str = (
        "20c5629ce85f6618cd3ed1ac1c99dc6d3064ed244013555c51385d9efab0d0072fac"
    )


class UtxoModel(BaseModel):
    amount: str = ("11501593788",)
    scriptPublicKey: ScriptPublicKeyModel
    blockDaaScore: str = "18867232"
    isCoinbase: bool = False


class UtxoResponse(BaseModel):
    address: str = ADDRESS_EXAMPLE
    outpoint: OutpointModel
    utxoEntry: UtxoModel


@app.get(
    "/addresses/{spectreAddress}/utxos",
    response_model=List[UtxoResponse],
    tags=["Spectre addresses"],
    openapi_extra={"strict_query_params": True},
)
async def get_utxos_for_address(
    response: Response,
    spectreAddress: str = Path(
        description=f"Spectre address as string e.g. {ADDRESS_EXAMPLE}",
        regex=REGEX_SPECTRE_ADDRESS,
    ),
):
    """
    Lists all open utxo for a given spectre address
    """
    try:
        to_script(spectreAddress)
    except ValueError:
        raise HTTPException(
            status_code=400, detail=f"Invalid address: {spectreAddress}"
        )

    resp = await spectred_client.request(
        "getUtxosByAddressesRequest",
        params={"addresses": [spectreAddress]},
        timeout=120,
    )
    try:
        if (
            "getUtxosByAddressesResponse" in resp
            and "error" in resp["getUtxosByAddressesResponse"]
        ):
            raise HTTPException(
                status_code=400, detail=resp["getUtxosByAddressesResponse"]["error"]
            )

        ttl = 8
        if len(resp["getUtxosByAddressesResponse"]["entries"]) > 100_000:
            ttl = 3600
        elif len(resp["getUtxosByAddressesResponse"]["entries"]) > 10_000:
            ttl = 600
        elif len(resp["getUtxosByAddressesResponse"]["entries"]) > 1_000:
            ttl = 20

        response.headers["Cache-Control"] = f"public, max-age={ttl}"
        return (
            utxo
            for utxo in resp["getUtxosByAddressesResponse"]["entries"]
            if utxo["address"] == spectreAddress
        )
    except KeyError:
        return []


class UtxoRequest(BaseModel):
    addresses: list[str] = [ADDRESS_EXAMPLE]


@app.post(
    "/addresses/utxos",
    response_model=List[UtxoResponse],
    tags=["Spectre addresses"],
    openapi_extra={"strict_query_params": True},
)
async def get_utxos_for_addresses(body: UtxoRequest):
    """
    List all unspent transaction outputs (UTXOs) for the specified Spectre address.
    """
    if body.addresses is None:
        return []

    for spectreAddress in body.addresses:
        try:
            if not re.search(REGEX_SPECTRE_ADDRESS, spectreAddress):
                raise ValueError
            to_script(spectreAddress)
        except ValueError:
            raise HTTPException(
                status_code=400, detail=f"Invalid address: {spectreAddress}"
            )

    resp = await spectred_client.request(
        "getUtxosByAddressesRequest", params={"addresses": body.addresses}, timeout=120
    )
    try:
        if (
            "getUtxosByAddressesResponse" in resp
            and "error" in resp["getUtxosByAddressesResponse"]
        ):
            raise HTTPException(
                status_code=400, detail=resp["getUtxosByAddressesResponse"]["error"]
            )

        return (utxo for utxo in resp["getUtxosByAddressesResponse"]["entries"])
    except KeyError:
        return []

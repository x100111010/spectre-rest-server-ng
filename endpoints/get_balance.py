# encoding: utf-8

from fastapi import Path, HTTPException
from pydantic import BaseModel

from constants import ADDRESS_EXAMPLE, REGEX_SPECTRE_ADDRESS
from server import app, spectred_client


class BalanceResponse(BaseModel):
    address: str = ADDRESS_EXAMPLE
    balance: int = 31415926535


@app.get(
    "/addresses/{spectreAddress}/balance",
    response_model=BalanceResponse,
    tags=["Spectre addresses"],
)
async def get_balance_from_spectre_address(
    spectreAddress: str = Path(
        description=f"Spectre address as string e.g. {ADDRESS_EXAMPLE}",
        regex=REGEX_SPECTRE_ADDRESS,
    ),
):
    """
    Get balance for a given spectre address
    """
    resp = await spectred_client.request(
        "getBalanceByAddressRequest", params={"address": spectreAddress}
    )

    try:
        resp = resp["getBalanceByAddressResponse"]
    except KeyError:
        if (
            "getUtxosByAddressesResponse" in resp
            and "error" in resp["getUtxosByAddressesResponse"]
        ):
            raise HTTPException(
                status_code=400, detail=resp["getUtxosByAddressesResponse"]["error"]
            )
        else:
            raise

    if resp.get("error"):
        raise HTTPException(500, resp["error"])

    try:
        balance = int(resp["balance"])

    # return 0 if address is ok, but no utxos there
    except KeyError:
        balance = 0

    return {"address": spectreAddress, "balance": balance}

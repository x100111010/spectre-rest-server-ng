# encoding: utf-8
import os
from pydantic import BaseModel
from starlette.responses import PlainTextResponse

from endpoints import mainnet_only
from helper import get_spr_price, get_spr_market_data
from server import app

DISABLE_PRICE = os.getenv("DISABLE_PRICE", "false").lower() == "true"


class PriceResponse(BaseModel):
    price: float = 0.0314


@app.get(
    "/info/price", response_model=PriceResponse | str, tags=["Spectre network info"]
)
@mainnet_only
async def get_price(stringOnly: bool = False):
    """
    Returns the current price for Spectre in USD. Price info is from coingecko.com
    """
    price = await get_spr_price() if not DISABLE_PRICE else 0
    if stringOnly:
        return PlainTextResponse(content=str(price))

    return {"price": price}


@app.get("/info/market-data", tags=["Spectre network info"], include_in_schema=False)
@mainnet_only
async def get_market_data():
    """
    Returns market data for Spectre.
    """
    return await get_spr_market_data() if not DISABLE_PRICE else {}

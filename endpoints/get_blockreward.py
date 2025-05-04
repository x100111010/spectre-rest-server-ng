# encoding: utf-8

from pydantic import BaseModel

from helper.deflationary_table import DEFLATIONARY_TABLE
from server import app, spectred_client


class BlockRewardResponse(BaseModel):
    blockreward: float = 12000132


@app.get(
    "/info/blockreward",
    response_model=BlockRewardResponse | str,
    tags=["Spectre network info"],
)
async def get_blockreward(stringOnly: bool = False):
    """
    Returns the current blockreward in SPR/block
    """
    resp = await spectred_client.request("getBlockDagInfoRequest")
    daa_score = int(resp["getBlockDagInfoResponse"]["virtualDaaScore"])

    reward = 0

    for to_break_score in sorted(DEFLATIONARY_TABLE):
        reward = DEFLATIONARY_TABLE[to_break_score]
        if daa_score < to_break_score:
            break

    if not stringOnly:
        return {"blockreward": reward}

    else:
        return f"{reward:.2f}"

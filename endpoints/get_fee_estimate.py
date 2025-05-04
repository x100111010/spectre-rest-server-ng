# encoding: utf-8

from fastapi import HTTPException
from typing import List
from server import app, spectred_client
from pydantic import BaseModel


class FeeEstimateBucket(BaseModel):
    feerate: int = 1
    estimatedSeconds: float = 0.004


class FeeEstimateResponse(BaseModel):
    priorityBucket: FeeEstimateBucket
    normalBuckets: List[FeeEstimateBucket]
    lowBuckets: List[FeeEstimateBucket]


@app.get(
    "/info/fee-estimate",
    response_model=FeeEstimateResponse,
    tags=["Spectre network info"],
)
async def get_fee_estimate():
    """
    Get fee estimate from Spectred.

    For all buckets, feerate values represent fee/mass of a transaction in `sompi/gram` units.<br>
    Given a feerate value recommendation, calculate the required fee by
    taking the transaction mass and multiplying it by feerate: `fee = feerate * mass(tx)`
    """
    resp = await spectred_client.request("getFeeEstimateRequest")
    if resp is None:
        raise HTTPException(
            status_code=501, detail="Spectred does not support fee estimate"
        )
    return resp["getFeeEstimateResponse"]["estimate"]

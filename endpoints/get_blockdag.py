# encoding: utf-8
from typing import List

from pydantic import BaseModel

from server import app, spectred_client


class BlockdagResponse(BaseModel):
    networkName: str = "spectre-mainnet"
    blockCount: str = "241192"
    headerCount: str = "241192"
    tipHashes: List[str] = [
        "6b928169424e447e7c3e0b473ee2c65d0592577cbb6725b5c1bb67e7f57dce35",
        "d73f185ef5e922fe44b2e050bb18b748ecc3d48a3be6956486bd7d4d1483b062",
        "2c68abd35ab071dc291320791000af8414ae681d055e4f10c75907c3e42c97eb",
        "60cbe79469f0ff3d0d833356dfeba35c9baf20c4c9b50e4dac8f66301d74930c",
        "bbe6572ec2bc02c9f6e0f1f38de3e92b9081a611e542ade6ef520c764603704c",
        "192c7adfda5721316a74bce99e938f901b4835f8f0893f1b1683e889e2d2a203",
        "07db215582f8b0820c2fe7795f6d1d68b6d7e022e99130bc377e24ff26a06453",
        "dc08c1fc6069f56b79aff2e2f6764b76d8021c261c97f4affc09f7e7a468ed8c",
    ]
    difficulty: float = 49735974.21745123
    pastMedianTime: str = "1746313781365"
    virtualParentHashes: List[str] = [
        "2c68abd35ab071dc291320791000af8414ae681d055e4f10c75907c3e42c97eb",
    ]
    pruningPointHash: str = (
        "ccc4ea96a34b35f1e995b83c0f540d0eb31728bcacb261b3d8c9b4328bc53597",
    )
    virtualDaaScore: str = "32056815"


@app.get(
    "/info/blockdag", response_model=BlockdagResponse, tags=["Spectre network info"]
)
async def get_blockdag():
    """
    Get some global Spectre BlockDAG information
    """
    resp = await spectred_client.request("getBlockDagInfoRequest")
    return resp["getBlockDagInfoResponse"]

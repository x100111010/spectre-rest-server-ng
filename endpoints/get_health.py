# encoding: utf-8
import hashlib
import time
from typing import List

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select

from constants import BPS, HEALTH_TOLERANCE_DOWN
from dbsession import async_session_blocks, async_session
from endpoints.get_virtual_chain_blue_score import current_blue_score_data
from models.Block import Block
from models.Transaction import Transaction
from models.TransactionAcceptance import TransactionAcceptance
from server import app, spectred_client


class SpectredResponse(BaseModel):
    spectredHost: str = ""
    serverVersion: str = "0.3.14"
    isUtxoIndexed: bool = True
    isSynced: bool = True
    p2pId: str = "1231312"
    blueScore: int = 101065625


class DBCheckStatus(BaseModel):
    isSynced: bool = True
    blueScore: int | None
    blueScoreDiff: int | None
    acceptedTxBlockTime: int | None
    acceptedTxBlockTimeDiff: int | None


class HealthResponse(BaseModel):
    spectredServers: List[SpectredResponse]
    database: DBCheckStatus


@app.get("/info/health", response_model=HealthResponse, tags=["Spectre network info"])
async def health_state():
    """
    Checks node and database health by comparing blue score and sync status.
    Returns health details or 503 if the database lags by ~10min or no nodes are synced.
    """
    current_blue_score_node = current_blue_score_data.get("blue_score")

    try:
        async with async_session_blocks() as s:
            last_blue_score_db = (
                await s.execute(
                    select(Block.blue_score).order_by(Block.blue_score.desc()).limit(1)
                )
            ).scalar()
        if last_blue_score_db is None or current_blue_score_node is None:
            db_check_status = DBCheckStatus(
                isSynced=False, blueScore=last_blue_score_db
            )
        else:
            blue_score_diff = abs(current_blue_score_node - last_blue_score_db)
            is_synced = blue_score_diff < HEALTH_TOLERANCE_DOWN * BPS
            db_check_status = DBCheckStatus(
                isSynced=is_synced,
                blueScore=last_blue_score_db,
                blueScoreDiff=blue_score_diff,
            )
        async with async_session() as s:
            last_accepted_tx_block_time_db = (
                await s.execute(
                    select(Transaction.block_time)
                    .join(
                        TransactionAcceptance,
                        Transaction.transaction_id
                        == TransactionAcceptance.transaction_id,
                    )
                    .order_by(Transaction.block_time.desc())
                    .limit(1)
                )
            ).scalar()
            time_diff = abs(
                int(time.time()) - int(last_accepted_tx_block_time_db) / 1000
            )
            db_check_status.isSynced = (
                db_check_status.isSynced and time_diff < HEALTH_TOLERANCE_DOWN
            )
            db_check_status.acceptedTxBlockTime = last_accepted_tx_block_time_db
            db_check_status.acceptedTxBlockTimeDiff = time_diff

    except Exception:
        db_check_status = DBCheckStatus(isSynced=False)

    await spectred_client.initialize_all()

    spectreds = [
        {
            "spectredHost": f"SPECTRED_HOST_{i + 1}",
            "serverVersion": spectred.server_version,
            "isUtxoIndexed": spectred.is_utxo_indexed,
            "isSynced": spectred.is_synced,
            "p2pId": hashlib.sha256(spectred.p2p_id.encode()).hexdigest(),
            "blueScore": current_blue_score_node,
        }
        for i, spectred in enumerate(spectred_client.spectreds)
    ]
    result = {
        "spectredServers": spectreds,
        "database": db_check_status.dict(),
    }

    if not db_check_status.isSynced or not any(
        spectred["isSynced"] for spectred in spectreds
    ):
        raise HTTPException(status_code=503, detail=result)

    return result

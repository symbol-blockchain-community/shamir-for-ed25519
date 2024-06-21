from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Tuple
from server.service.symbol import generate_new_private_key
from server.service.shamir import generate_shamir_keys, recover_shamir_keys
from fastapi.responses import FileResponse
import os

app = FastAPI()


class KeyShares(BaseModel):
    shares: List[Tuple[int, int, str]]


@app.post("/generate_shamir_keys")
def generate_keys():
    key = generate_new_private_key()
    try:
        shamir_keys = generate_shamir_keys(key)
        return {"original_key": key, "shamir_keys": shamir_keys}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/recover_shamir_keys")
def recover_keys(key_shares: KeyShares):
    try:
        recovered_key = recover_shamir_keys(key_shares.shares)
        return {"recovered_key": recovered_key}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


script_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(script_dir, "static", "index.html")


@app.get("/")
async def read_root():
    return FileResponse(static_dir)

import uvicorn
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from mlBackend import *

app = FastAPI()

class DB(BaseModel):
    dbName : str

@app.get("/")
async def app():
    return {"message":"main api"}

@app.get("/app")
async def app():
    return {"message":"hi app"}

@app.post("/app/analyze")
async def analyze(database: DB):
    user_data = walkingML.fetch_firebase(database.dbName)
    user_data = walkingML.fillData(user_data)
    result = walkingML.detect(user_data)
    walkingML.setResult(result,database.dbName)
    return {"message" : "success"}
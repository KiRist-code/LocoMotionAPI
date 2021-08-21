from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
# from mlBackend import walkingML

app = FastAPI()
# ml = walkingML()

class firebase(BaseModel):
    dbname : str

@app.get("/")
def read_root():
    return {"message": "Hello"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.post("/app/analyze")
async def analyze(database: firebase):
    user_data = ml.fetch_firebase(database.dbName)
    user_data = ml.fillData(user_data)
    result = ml.detect(user_data)
    ml.setResult(result,database.dbName)
    return {"message" : "success"}

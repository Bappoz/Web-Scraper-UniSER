import os 
import uvicorn
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

app = FastAPI()

mongo_url = os.getenv("MONGO_URL")
PORT = int(os.getenv("PORT_DB", 4000))


client = MongoClient(mongo_url)
db = client.get_database()
collection = db["researchers-data"]


@app.get("/health", status_code=200)
def db_healthcheck():
    """
    Checar conexão com banco de dados
    """

    if db is None:
        raise HTTPException(status_code=500, detail="Banco de dados não encontrado")
    
    try:
        server_info = client.server_info()
        return {"status": "OK", "mongo_version": server_info["version"]}
    except:
        raise HTTPException(status_code=500, detail="Não foi possível conectar ao MongoDB")
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
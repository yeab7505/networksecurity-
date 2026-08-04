import os 
import sys

import certifi
import pandas as pd
import pymongo

import Networksecurity
from Networksecurity.utils.main_util.utils import load_object
from Networksecurity.utils.ml_utils.model.estimator import NetworkModel
from Networksecurity.exception.exception import NetworkSecurityException
from Networksecurity.logger.logger import logging
from Networksecurity.pipeline.training_pipeline import TrainingPipeline
from Networksecurity.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DATABASE_NAME

from dotenv import load_dotenv
load_dotenv()

ca = certifi.where()
mongo_db_url = os.getenv("mongo_db_url")

client = None
if mongo_db_url:
    try:
        client = pymongo.MongoClient(mongo_db_url, tls=True, tlsCAFile=ca, tlsAllowInvalidCertificates=True)
        database = client[DATA_INGESTION_DATABASE_NAME]
        collection = database[DATA_INGESTION_COLLECTION_NAME]
    except Exception as err:
        logging.warning(f"MongoDB connection warning: {err}")

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, Response

app = FastAPI(title="Cyber Security Network Prediction API")
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],    
)   

@app.get("/", tags=["authentication"])
async def index():
    template_path = os.path.join("templates", "index.html")
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    return HTMLResponse(content="<h1>Templates not found.</h1>", status_code=444)

@app.get("/train", tags=["train"])
async def train_route():
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
        return Response(content="Training successful!!", status_code=200)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e

@app.post("/predict", tags=["predict"])
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        if 'Result' in df.columns:
            df.drop(columns=['Result'], axis=1, inplace=True)
            
        preprocessor = load_object(file_path="final_models/preprocessor.pkl")
        final_model = load_object(file_path="final_models/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)
        
        y_pred = network_model.predict(df)
        df['predicted_column'] = y_pred
        
        os.makedirs("prediction_data", exist_ok=True)
        df.to_csv("prediction_data/predicted_output.csv", index=False)

        total_records = len(df)
        threat_mask = (df['predicted_column'] == 0) | (df['predicted_column'] == -1)
        threats = int(threat_mask.sum())
        safe = int((df['predicted_column'] == 1).sum())

        df_clean = df.fillna("")
        data_records = df_clean.to_dict(orient="records")
        columns = list(df_clean.columns)

        return JSONResponse(content={
            "status": "success",
            "total": total_records,
            "threats": threats,
            "safe": safe,
            "columns": columns,
            "data": data_records
        })

    except Exception as e:
        logging.error(f"Prediction exception: {str(e)}")
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@app.get("/download-prediction", tags=["predict"])
async def download_prediction():
    file_path = "prediction_data/predicted_output.csv"
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename="predicted_output.csv", media_type="text/csv")
    else:
        return Response(content="Prediction output file not found.", status_code=404)


if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=8000)
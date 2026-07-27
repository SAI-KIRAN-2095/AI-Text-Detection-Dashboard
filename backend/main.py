from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from backend.ml_models import TripleModelDetector

app = FastAPI(title="LLM Text Detection Backend API", version="1.0.0")

# Enable CORS for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Detector Engine
detector = TripleModelDetector()

class PredictRequest(BaseModel):
    text: str
    model: Optional[str] = "all"  # Options: 'all', 'model_1', 'model_2', 'model_3'

@app.get("/")
def read_root():
    return {"message": "LLM Text Detection API is active and running!"}

@app.get("/health")
def health_check():
    return {
        "status": "online",
        "models_loaded": {
            "model_1": "BERT Transformer",
            "model_2": detector.m2_ensemble is not None,
            "model_3": detector.m3_ensemble is not None
        }
    }

@app.post("/predict")
def predict_text(payload: PredictRequest):
    text = payload.text
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Text parameter cannot be empty.")
    
    result = detector.analyze_full(text, selected_model=payload.model)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)

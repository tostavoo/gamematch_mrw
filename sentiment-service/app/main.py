from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from app.analyzer import SentimentAnalyzer

# Crear app
app = FastAPI(
    title="Sentiment Analysis Microservice",
    description="Microservicio de análisis de sentimientos para GameMatch",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos
class TextInput(BaseModel):
    text: str

class BatchTextInput(BaseModel):
    texts: List[str]

# Analizador
analyzer = SentimentAnalyzer()

# ============= ENDPOINTS =============

@app.get("/")
def root():
    return {
        "service": "Sentiment Analysis Microservice",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "analyze": "/analyze",
            "batch": "/analyze/batch",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health():
    return {"status": "healthy", "service": "sentiment-service"}

@app.post("/analyze")
def analyze_sentiment(data: TextInput):
    """Analiza el sentimiento de un texto"""
    try:
        result = analyzer.analyze(data.text)
        return {
            "success": True,
            "data": result,
            "input_text": data.text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/batch")
def analyze_batch(data: BatchTextInput):
    """Analiza múltiples textos"""
    try:
        results = analyzer.batch_analyze(data.texts)
        return {
            "success": True,
            "count": len(results),
            "data": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
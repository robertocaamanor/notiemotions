from typing import Dict, Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from analyzer import EmotionAnalyzer
from scraper import fetch_article


class AnalyzeRequest(BaseModel):
    url: str = Field(..., example="https://httpbin.org/html", description="URL del artículo a analizar")


class AnalyzeResponse(BaseModel):
    url: str
    title: str
    text: str
    dominant: Optional[str]
    scores: Dict[str, float]


app = FastAPI(
    title="emotions-farandula API",
    description="API para extraer un artículo y analizar emociones en español. Devuelve título, texto, scores y emoción dominante.",
    version="0.1",
)

analyzer = EmotionAnalyzer()


@app.get(
    "/analyze",
    response_model=AnalyzeResponse,
    summary="Analiza una URL (GET)",
    tags=["analyze"],
)
async def analyze_get(url: str = Query(..., description="URL a analizar", example="https://httpbin.org/html")):
    """Analiza el artículo en la URL proporcionada y devuelve los scores de emoción.

    - Parámetros: url (query)
    - Respuesta: objeto con `title`, `text`, `dominant` y `scores`.
    """
    if not url:
        raise HTTPException(status_code=400, detail="missing_url")
    art = fetch_article(url)
    if not art:
        raise HTTPException(status_code=502, detail="fetch_failed")
    title = art.get("title", "")
    text = art.get("text", "")
    scores = analyzer.analyze_text(title + "\n\n" + text)
    dominant = analyzer.dominant_emotion(title + "\n\n" + text)
    return {"url": url, "title": title, "text": text, "dominant": dominant, "scores": scores}


@app.post(
    "/analyze",
    response_model=AnalyzeResponse,
    summary="Analiza una URL (POST)",
    tags=["analyze"],
)
async def analyze_post(payload: AnalyzeRequest):
    """Analiza la URL recibida en el body JSON {"url": ...}."""
    url = payload.url
    if not url:
        raise HTTPException(status_code=400, detail="missing_url")
    art = fetch_article(url)
    if not art:
        raise HTTPException(status_code=502, detail="fetch_failed")
    title = art.get("title", "")
    text = art.get("text", "")
    scores = analyzer.analyze_text(title + "\n\n" + text)
    dominant = analyzer.dominant_emotion(title + "\n\n" + text)
    return {"url": url, "title": title, "text": text, "dominant": dominant, "scores": scores}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

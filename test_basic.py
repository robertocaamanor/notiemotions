"""Pruebas básicas para el proyecto.

Estas pruebas son intentionally simples: comprueban el analizador y la función
de scraping en su modo fallback (no requieren newspaper3k ni pysentimiento
instalados para pasar).
"""
from analyzer import EmotionAnalyzer
from scraper import fetch_article


def test_analyzer_lexicon():
    a = EmotionAnalyzer(use_pysentimiento=False)
    text = "Estoy muy feliz y alegre, aunque un poco asustado."
    scores = a.analyze_text(text)
    assert scores["joy"] > 0
    assert scores["fear"] > 0


def test_scraper_fallback():
    # Usar una pequeña página estática que siempre tiene <p> para no depender
    # de newspaper3k. No hacemos asserting del contenido exacto, solo que
    # devuelve un diccionario o None.
    result = fetch_article("https://httpbin.org/html")
    assert result is not None
    assert "text" in result


if __name__ == "__main__":
    test_analyzer_lexicon()
    test_scraper_fallback()
    print("Tests passed")

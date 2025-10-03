"""crawler.py

Procesa múltiples URLs desde un archivo de texto (una URL por línea) o desde RSS
y guarda los resultados (title, text, emotion scores) en un JSON.

Uso básico:
    python crawler.py urls.txt results.json

Formato de salida: lista JSON con objetos {url, title, text, dominant, scores}
"""
import json
import sys
from typing import List

from scraper import fetch_article
from analyzer import EmotionAnalyzer


def process_urls(urls: List[str], analyzer: EmotionAnalyzer):
    results = []
    for url in urls:
        url = url.strip()
        if not url:
            continue
        print(f"Procesando: {url}")
        art = fetch_article(url)
        if not art:
            print(f"  Error: no se pudo obtener {url}")
            results.append({"url": url, "error": "fetch_failed"})
            continue

        text = art.get("text", "")
        title = art.get("title", "")
        scores = analyzer.analyze_text(title + "\n\n" + text)
        dominant = analyzer.dominant_emotion(title + "\n\n" + text)
        results.append({
            "url": url,
            "title": title,
            "text": text,
            "dominant": dominant,
            "scores": scores,
        })

    return results


def read_urls_file(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]


def save_results(path: str, results):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


def main(argv=None):
    argv = argv or sys.argv[1:]
    if not argv or len(argv) < 2:
        print("Uso: python crawler.py <urls.txt> <out.json>")
        return 1

    urls_file = argv[0]
    out_file = argv[1]

    urls = read_urls_file(urls_file)
    analyzer = EmotionAnalyzer()
    results = process_urls(urls, analyzer)
    save_results(out_file, results)
    print(f"Guardado {len(results)} resultados en {out_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""scraper.py

Funciones de scraping simples para extraer títulos y contenido de noticias.

Usa newspaper3k si está disponible; si no, hace un request + BeautifulSoup básico.
"""
from typing import Optional, Dict
import requests
from bs4 import BeautifulSoup


def fetch_article(url: str, timeout: int = 10) -> Optional[Dict[str, str]]:
    """Intenta obtener título y texto principal de un artículo dada su URL.

    Devuelve {'title': str, 'text': str} o None si falla.
    """
    try:
        # Intentar usar newspaper3k
        try:
            from newspaper import Article

            art = Article(url)
            art.download()
            art.parse()
            title = art.title or ""
            text = art.text or ""
            return {"title": title, "text": text}
        except Exception:
            # Fallback a requests + BeautifulSoup
            resp = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"})
            if resp.status_code != 200:
                return None
            soup = BeautifulSoup(resp.text, "html.parser")
            title_tag = soup.find("title")
            title = title_tag.get_text().strip() if title_tag else ""

            # Extraer <article> si existe; si no, buscar elementos con la
            # clase 'article-body' (puede haber varios); si tampoco existe,
            # concatenar todos los <p> de la página.
            article_tag = soup.find("article")
            paragraphs = []
            if article_tag:
                paragraphs = article_tag.find_all("p")

            # Si no encontramos <p> dentro de <article>, intentar otras clases
            if not paragraphs:
                # Buscar elementos cuya clase incluya 'article-body' o
                # buscar <div> cuya clase contenga la subcadena 'content'
                # (maneja múltiples elementos y nombres de clase compuestos).
                def class_has(sub):
                    def _check(c):
                        if not c:
                            return False
                        # BeautifulSoup puede pasar listas de clases o strings
                        if isinstance(c, (list, tuple)):
                            cs = " ".join(c).lower()
                        else:
                            cs = str(c).lower()
                        return sub in cs
                    return _check

                body_tags = soup.find_all(class_=class_has("article-body"))
                if not body_tags:
                    # Buscar <div> con clase que contenga 'content'
                        # Buscar cualquier elemento cuya clase contenga la subcadena 'content'
                        # (ej. 'post-content', 'mainContent', etc.)
                        body_tags = soup.find_all(class_=class_has("content"))
                if body_tags:
                    paragraphs = []
                    for bt in body_tags:
                        paragraphs.extend(bt.find_all("p"))

                # Si aun así no se encontraron <p>, fallback a todos los <p>
                if not paragraphs:
                    paragraphs = soup.find_all("p")

            text = "\n\n".join(p.get_text().strip() for p in paragraphs if p.get_text().strip())
            return {"title": title, "text": text}
    except Exception:
        return None


if __name__ == "__main__":
    url = "https://www.t13.cl/noticias/"
    print(fetch_article(url))

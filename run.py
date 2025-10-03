
"""run.py

Pequeña interfaz de línea de comandos para realizar scraping de una URL y
mostrar la emoción dominante del artículo.
"""
import sys
from analyzer import EmotionAnalyzer
from scraper import fetch_article


def main(argv=None):
	argv = argv or sys.argv[1:]
	if not argv:
		print("Uso: python run.py <url>")
		return 1

	url = argv[0]
	art = fetch_article(url)
	if not art:
		print("No se pudo obtener el artículo.")
		return 2

	text = art.get("text", "")
	title = art.get("title", "")
	analyzer = EmotionAnalyzer()
	dominant = analyzer.dominant_emotion(title + "\n\n" + text)

	print("Título:", title)
	print("\n--- TEXTO ---")
	print(text)
	print("--- FIN TEXTO ---\n")
	print("Emoción dominante:", dominant)
	print("Scores:", analyzer.analyze_text(title + "\n\n" + text))
	return 0


if __name__ == "__main__":
	raise SystemExit(main())

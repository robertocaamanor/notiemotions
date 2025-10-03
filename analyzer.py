"""analyzer.py

Herramientas para el análisis de emociones en textos en español.

Comportamiento:
- Intenta crear un analizador de emociones en español usando `pysentimiento`.
- Si no está disponible (sin internet o paquete), usa un lexicón pequeño como fallback.

Funciones principales:
- EmotionAnalyzer.analyze_text(text) -> dict de scores por emoción
- EmotionAnalyzer.dominant_emotion(text) -> str
"""
from typing import Dict, Optional
import re


class EmotionAnalyzer:
	"""Analizador de emociones.

	Intenta usar pysentimiento (mejor para español). Si no está instalado o falla
	al cargar el modelo, se activa un analizador por lexicón simple incluido.
	"""

	PY_SENT_LABELS = ["anger", "fear", "joy", "sadness"]

	def __init__(self, use_pysentimiento: bool = True):
		# Si use_pysentimiento=True, intentaremos usar pysentimiento pero la
		# carga del modelo se hace de forma perezosa (cuando se analice el
		# primer texto o cuando se llame a preload()). Esto evita descargas
		# automáticas al importar el módulo.
		self.use_pysentimiento = bool(use_pysentimiento)
		self._analyzer = None
		self._pysent_ready = False

		# Lexicón simple en español (fallback). Map de palabra -> emoción.
		# Esta lista es intencionalmente pequeña; se puede ampliar.
		self.lexicon = {
			"feliz": "joy",
			"contento": "joy",
			"alegre": "joy",
			"entusiasmado": "joy",
			"amor": "joy",
			"enojado": "anger",
			"ira": "anger",
			"molesto": "anger",
			"furioso": "anger",
			"triste": "sadness",
			"lamenta": "sadness",
			"llora": "sadness",
			"miedo": "fear",
			"asustado": "fear",
			"teme": "fear",
			"susto": "fear",
			"sorprendido": "surprise",
			"sorpresa": "surprise",
			"asco": "disgust",
			"disgustado": "disgust",
		}

	def analyze_text(self, text: str) -> Dict[str, float]:
		"""Analiza un texto y devuelve un diccionario {emocion: puntaje}.

		Si pysentimiento está disponible devolverá probabilidades; si no, usará
		el lexicón y contará ocurrencias normalizadas.
		"""
		if not text:
			return {}

		text = text.strip()

		# Intentar usar pysentimiento si está habilitado (carga perezosa)
		if self.use_pysentimiento:
			# Intentar inicializar el analizador pysentimiento si aún no se hizo
			if not self._pysent_ready:
				try:
					from pysentimiento import create_analyzer

					self._analyzer = create_analyzer(task="emotion", lang="es")
					self._pysent_ready = True
				except Exception:
					# No se pudo cargar pysentimiento; desactivar para futuros intentos
					self.use_pysentimiento = False
					self._pysent_ready = True

			if self._analyzer is not None:
				try:
					res = self._analyzer.predict(text)
					probas = {}
					if hasattr(res, "probas") and res.probas:
						probas = res.probas
					elif hasattr(res, "scores") and res.scores:
						probas = res.scores
					else:
						probas = {getattr(res, 'output', 'others'): 1.0}

					out = {k: float(probas.get(k, 0.0)) for k in self.PY_SENT_LABELS}
					return out
				except Exception:
					# Si el predict falla por cualquier razón, hacer fallback lexicón
					pass

		# Si llegamos aquí, usar el fallback lexicón simple

		# Fallback lexicón simple (método basado en conteo)
		text_lower = re.sub(r"[^\wáéíóúüñÁÉÍÓÚÜÑ]+", " ", text.lower())
		tokens = text_lower.split()
		counts = {}
		for t in tokens:
			emo = self.lexicon.get(t)
			if emo:
				counts[emo] = counts.get(emo, 0) + 1

		total = sum(counts.values())
		if total == 0:
			# Devolver zeros para emociones principales si no hay matches
			# (sin la categoría 'others')
			return {"anger": 0.0, "fear": 0.0, "joy": 0.0, "sadness": 0.0}

		# Normalizar a probabilidades
		out = {"anger": 0.0, "fear": 0.0, "joy": 0.0, "sadness": 0.0}
		for k, v in counts.items():
			if k in out:
				out[k] = v / total
			# Si la emoción del lexicón no está en las etiquetas principales,
			# la ignoramos (no acumulamos en 'others').

		return out

	def dominant_emotion(self, text: str) -> Optional[str]:
		"""Devuelve la emoción dominante (clave) o None si no hay texto."""
		scores = self.analyze_text(text)
		if not scores:
			return None
		# Si todos los puntajes son cero, no hay emoción dominante
		max_k, max_v = max(scores.items(), key=lambda x: x[1])
		if max_v == 0.0:
			return None
		return max_k

	def preload(self) -> bool:
		"""Forzar la carga del modelo de pysentimiento.

		Devuelve True si el modelo quedó cargado, False en caso de fallback.
		"""
		if not self.use_pysentimiento:
			return False
		if self._pysent_ready and self._analyzer is not None:
			return True
		try:
			from pysentimiento import create_analyzer

			self._analyzer = create_analyzer(task="emotion", lang="es")
			self._pysent_ready = True
			return True
		except Exception:
			self.use_pysentimiento = False
			self._pysent_ready = True
			return False


if __name__ == "__main__":
	# Pequeña demo
	a = EmotionAnalyzer()
	sample = "Estoy muy feliz y emocionado, aunque un poco asustado por el cambio."
	print(a.analyze_text(sample))
	print("Dominante:", a.dominant_emotion(sample))


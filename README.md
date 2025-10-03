Proyecto: notiemotions

Objetivo: hacer web scraping de noticias de farándula chilena y analizar emociones.

Cómo usar:
- Instalar dependencias: pip install -r requirements.txt
- Ejecutar: python run.py <url-de-noticia>

API
---
También hay una API HTTP que expone el endpoint `/analyze`.

Ejecutar con uvicorn:

```powershell
uvicorn api:app --host 127.0.0.1 --port 8000
```

O usando el script incluido:

```powershell
python serve.py
```

Documentación OpenAPI:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc


Uso en lote (crawler):
- Crear un archivo `urls.txt` con una URL por línea.
- Ejecutar: python crawler.py urls.txt results.json

El archivo `results.json` contendrá una lista con los artículos procesados y
las emociones detectadas.

Notas:
- `pysentimiento` mejora la clasificación en español; si no está disponible se usa un lexicón simple.

Contribuir
---------

Si quieres contribuir al proyecto, sigue estos pasos básicos para trabajar en un entorno reproducible y con formateo/linters automáticos.

1) Crear y activar un virtualenv (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Instalar dependencias (producción y desarrollo):

```powershell
pip install -r requirements.txt
pip install --upgrade pre-commit black isort flake8
```

3) Añadir un archivo `.pre-commit-config.yaml` en el repo (ejemplo mínimo):

```yaml
repos:
	- repo: https://github.com/psf/black
		rev: stable
		hooks:
			- id: black
	- repo: https://github.com/PyCQA/isort
		rev: 5.12.0
		hooks:
			- id: isort
	- repo: https://github.com/PyCQA/flake8
		rev: 6.1.0
		hooks:
			- id: flake8
```

4) Habilitar los hooks:

```powershell
pre-commit install
```

Con esto, `black`/`isort`/`flake8` se ejecutarán automáticamente antes de cada commit. También puedes ejecutar los formateadores manualmente:

```powershell
black .
isort .
flake8
```

Si quieres, puedo crear el archivo `.pre-commit-config.yaml` y añadir un `requirements-dev.txt` con las dependencias de desarrollo. ¿Lo hago ahora?

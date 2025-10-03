Despliegue recomendado: Render + DNS en cPanel
=============================================

Este documento explica cómo desplegar la API FastAPI en Render (o servicios similares) y cómo apuntar un subdominio desde tu cPanel (tvenserio.com) hacia la app desplegada.

Preparación local
------------------
1. Fija tus dependencias de producción:

```bash
pip freeze > requirements-prod.txt
```

2. Asegúrate de que `requirements.txt` contiene todas las dependencias necesarias. Si usas `requirements-prod.txt`, sube ese archivo y pon `pip install -r requirements-prod.txt` como comando de build.

3. Comprueba tests localmente:

```bash
python -m pytest
```

Deploy en Render
-----------------
1. Crea una cuenta en https://render.com y conecta tu repositorio (GitHub/GitLab).
2. Nuevo servicio → "Web Service".
   - Branch: `main`
   - Build Command: `pip install -r requirements.txt` (o `requirements-prod.txt` si lo subes)
   - Start Command: `gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:$PORT api:app`
3. Deploy. Render te dará una URL pública (p. ej. `notiemotions.onrender.com`).

Configurar DNS en cPanel (apuntar subdominio)
-------------------------------------------
1. Entra en cPanel → Zone Editor o Dominios → Editor de Zonas.
2. Añade un registro CNAME:
   - Nombre: `api` (esto creará `api.tvenserio.com`)
   - Tipo: CNAME
   - Destino: el hostname que Render te dio (por ejemplo `notiemotions.onrender.com`)
3. Guarda y espera propagación DNS (minutes–hours).
4. Si Render te pide un A record en lugar de CNAME, crea un A record apuntando a la IP que te indiquen.

Verificar
---------
- Visita `https://api.tvenserio.com/docs` para ver Swagger UI.
- Revisa logs de Render para depurar fallos.

Notas sobre `pysentimiento` y modelos grandes
--------------------------------------------
Si mantienes `pysentimiento` / `transformers` / `torch` en producción, Render o el servicio PaaS necesitará suficiente memoria/CPU. Como alternativa puedes:

- Mantener un modo "lexicon-only" para la API en producción.
- Separar el análisis pesado a un worker o microservicio con más recursos.

Opciones adicionales
--------------------
- Si quieres, preparo un `Procfile`, `Dockerfile` optimizado y un `requirements-prod.txt` generado. También puedo preparar un `README_DEPLOY_cpanel.md` con instrucciones paso-a-paso para crear el registro DNS en cPanel con capturas de ejemplo.

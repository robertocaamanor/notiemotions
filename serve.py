"""Launcher sencillo para ejecutar la API con Uvicorn.

Uso:
    python serve.py           # arranca en 127.0.0.1:8000
    python serve.py 0.0.0.0 80 --reload
"""
import sys
import uvicorn

def main(argv=None):
    argv = argv or sys.argv[1:]
    host = argv[0] if len(argv) > 0 else '127.0.0.1'
    port = int(argv[1]) if len(argv) > 1 else 8000
    reload_flag = '--reload' in argv

    uvicorn.run('api:app', host=host, port=port, reload=reload_flag)


if __name__ == '__main__':
    main()

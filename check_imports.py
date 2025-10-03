try:
    import uvicorn
    from api import app
    print('uvicorn and api.app import OK')
except Exception as e:
    print('IMPORT ERROR:', e)
    raise

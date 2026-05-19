"""
File principale del sito web
"""
# Import delle librerie necessarie
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Health check endpoint
@app.get("/health")
async def health_check():
	"""
	Endpoint per verificare lo stato del server
	"""
	return {"status": "ok"}

# Router



# Gestione globale degli errori 

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
	"""
	Gestore globale degli errori
	"""

	logger.error(f"Errore non gestito: {exc}")
	
	return JSONResponse(
		status_code=500,
		content=
		{
			"message": "Si è verificato un errore interno al server.", 
			"details": str(exc), 
			"type": type(exc).__name__, 
			"request": 
			{
				"method": request.method, 
				"url": str(request.url), 
				"headers": dict(request.headers)
			}
		},
	)
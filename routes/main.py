from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from loguru import logger
from datetime import datetime


# Inizializzazione del router
router = APIRouter()
templates = Jinja2Templates(directory="static/html")


# Homepage 
@router.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
	
	return templates.TemplateResponse(
		request=request,
		name="homepage.html",
		context=
		{
			"logo": "SUCA"
		}
	)
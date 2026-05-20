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
		context= {
			"title": "Home"
		}
	)

# Pagine secondarie
@router.get("/strumenti", response_class=HTMLResponse)
async def strumenti(request: Request):
	return templates.TemplateResponse(
		request=request,
		name="homepage.html",
		context= {
			"title": "Strumenti"
		}
	)

@router.get("/progetto", response_class=HTMLResponse)
async def progetto(request: Request):
	return templates.TemplateResponse(
		request=request,
		name="homepage.html",
		context= {
			"title": "Il progetto"
		}
	)

@router.get("/risultati", response_class=HTMLResponse)
async def risultati(request: Request):
	return templates.TemplateResponse(
		request=request,
		name="homepage.html",
		context= {
			"title": "Risultati"
		}
	)

@router.get("/team", response_class=HTMLResponse)
async def team(request: Request):
	return templates.TemplateResponse(
		request=request,
		name="homepage.html",
		context= {
			"title": "Il team"
		}
	)

@router.get("/download", response_class=HTMLResponse)
async def download(request: Request):
	return templates.TemplateResponse(
		request=request,
		name="homepage.html",
		context= {
			"title": "Download"
		}
	)
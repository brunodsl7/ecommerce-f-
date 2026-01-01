import os
from dotenv import load_dotenv
from supabase import create_client, Client
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# 1. Carrega as variáveis (no Render elas vêm das Settings)
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# 2. Cria a conexão com o Supabase
supabase: Client = create_client(url, key)

app = FastAPI()

# --- AQUI ESTAVA O ERRO (PRECISA DESSAS LINHAS ABAIXO) ---
# Isso avisa o FastAPI onde estão os arquivos de visual
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root(request: Request):
    # Aqui ele busca os produtos no seu banco do Supabase
    response = supabase.table("produtos").select("*").execute()
    produtos = response.data
    
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "produtos": produtos}
    )

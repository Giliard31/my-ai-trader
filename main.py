import os
import random
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Simulação de análise de mercado em tempo real (substitua futuramente pelo client WebSocket da IQ Option)
ASSETS = ["EUR/USD", "GBP/USD", "BTC/USD", "EUR/JPY"]

COMMENTARIES = [
    "O preço bateu na banda de Bollinger inferior e o RSI entrou em sobrevenda extrema. Vejo exaustão de baixa dos ursos.",
    "Fluxo de ordens institucional pesado empurrando o ativo para cima. Rompimento de resistência confirmada no gráfico de 1 minuto.",
    "Mercado consolidado em range estreito. Cuidado com falsos rompimentos (fakeouts). Aguardando volume comprador.",
    "Candle de reversão (Martelo) formado com volume acima da média. Forte pressão compradora entrando agora!"
]

def generate_ai_signal(asset):
    action = random.choice(["CALL (COMPRA)", "PUT (VENDA)"])
    confidence = random.randint(78, 99)
    commentary = random.choice(COMMENTARIES)
    price = round(random.uniform(1.0500, 1.1200), 5)
    
    return {
        "asset": asset,
        "price": price,
        "action": action,
        "confidence": f"{confidence}%",
        "commentary": commentary,
        "timestamp": asyncio.get_event_loop().time()
    }

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            asset = random.choice(ASSETS)
            signal_data = generate_ai_signal(asset)
            await websocket.send_json(signal_data)
            await asyncio.sleep(4) # Envia uma nova análise a cada 4 segundos
    except WebSocketDisconnect:
        print("Cliente desconectado")

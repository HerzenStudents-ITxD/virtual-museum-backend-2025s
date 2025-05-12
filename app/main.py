from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import os
import shutil
from uuid import uuid4
from app.api.routers import exhibits, photos, exhibit_links, culture, culture_links, auth

# Подключаем все необходимые маршруты
from app.database.database import engine, init_db


# Папка для хранения загруженных изображений
UPLOAD_FOLDER = '../uploads/images' 
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Логика подключения к базе данных
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    engine.dispose()

app = FastAPI(lifespan=lifespan, middleware=[  
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    Middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"],
    )
])

# Монтируем папку для обслуживания статических файлов
app.mount("/static", StaticFiles(directory=UPLOAD_FOLDER), name="static")

# Подключение роутеров API
app.include_router(exhibits.router)

app.include_router(photos.router)

app.include_router(exhibit_links.router)

app.include_router(culture.router)
app.include_router(culture_links.router)
app.include_router(auth.router)

print("✅ main.py загружен")
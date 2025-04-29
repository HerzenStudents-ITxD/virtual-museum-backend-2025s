from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import engine, init_db
from app.api.routers import exhibits, photos, exhibit_links, culture, culture_links

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    engine.dispose()

app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(exhibits.router)
app.include_router(photos.router)
app.include_router(exhibit_links.router)
app.include_router(culture.router)
app.include_router(culture_links.router)




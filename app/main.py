from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database.database import engine, init_db
from app.api.routers import exhibits, photos, exhibit_links, culture, culture_links

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    engine.dispose()

app = FastAPI(lifespan=lifespan)
app.include_router(exhibits.router)
app.include_router(photos.router)
app.include_router(exhibit_links.router)
app.include_router(culture.router)
app.include_router(culture_links.router)




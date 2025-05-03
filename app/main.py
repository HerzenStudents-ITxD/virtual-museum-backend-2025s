from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database.database import engine, init_db
from app.api.routers import exhibits, photos, exhibit_links, culture, culture_links, auth
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    engine.dispose()

middleware = [
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
]


app = FastAPI(lifespan=lifespan, middleware=middleware)
app.include_router(exhibits.router)
app.include_router(photos.router)
app.include_router(exhibit_links.router)
app.include_router(culture.router)
app.include_router(culture_links.router)
app.include_router(auth.router)




import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from conf import settings
from services.http.urls import routers

app = FastAPI(title=settings.TITLE)

root_router = APIRouter(prefix="/api/v1{{cookiecutter.repo_name}}")
for i in routers:
    root_router.include_router(i, tags=[i.prefix.lstrip("/").title()])
app.include_router(root_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

if __name__ == "__main__":
    uvicorn.run("web:app", host="0.0.0.0", port=8000, reload=True, access_log=True)

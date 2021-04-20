import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from conf import settings
from services.http.urls import routers

app = FastAPI(title=settings.TITLE)
for i in routers:
    app.include_router(i, tags=[i.prefix.lstrip("/").title()])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True, access_log=True)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import user_router

app = FastAPI()

app.include_router(router=user_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

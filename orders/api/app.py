from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import category_router, product_router, order_router

app = FastAPI()

app.include_router(router=category_router)
app.include_router(router=product_router)
app.include_router(router=order_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

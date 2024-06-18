from fastapi import FastAPI
# import asyncio 
from db.db_connector import create_db_and_tables

from routers.token_route import token_router
from routers.oauth_route import oauth_router

from starlette.middleware.sessions import SessionMiddleware


# async def task_initiator():
#     asyncio.create_task(user_consumer())

async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key="add any string...")


@app.get("/")
def home():
    return "Welcome to Google Ads services"

app.include_router(router=token_router)
app.include_router(router=oauth_router)


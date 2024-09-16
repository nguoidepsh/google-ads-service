from routers.email_route import email_router
from fastapi import FastAPI, Depends
from starlette.middleware.sessions import SessionMiddleware
from middlewares.auth_middleware import check_permission



app = FastAPI()


@app.get("/")
async def home():
    return "Welcome to Google Ads services"


app.add_middleware(SessionMiddleware, secret_key="add any string...")

app.include_router(router=email_router, dependencies=[Depends(check_permission)]) 

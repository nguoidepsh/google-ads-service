from fastapi import Depends, FastAPI
from middlewares.auth_middleware import check_permission
from routers.ads_route import ads_router
from routers.email_route import email_router
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()


@app.get("/")
async def home():
    return "Welcome to Google Ads services"


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key="add any string...")

app.include_router(router=email_router, dependencies=[Depends(check_permission)])

app.include_router(
    router=ads_router, prefix="/ads", dependencies=[Depends(check_permission)]
)

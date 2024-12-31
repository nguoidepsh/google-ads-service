import logging

from fastapi import APIRouter, Depends, FastAPI, Request, Response
from fastapi.routing import APIRoute
from middlewares.auth_middleware import check_permission
from routers.account_route import router as account_router
from routers.ads_route import ads_router
from routers.email_route import email_router
from routers.provider_route import router as provider_router
from routers.request_route import router as request_router
from starlette.background import BackgroundTask
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import StreamingResponse


def log_info(req_body, res_body):
    logging.info(req_body)
    logging.info(res_body)


class LoggingRoute(APIRoute):
    def get_route_handler(self):
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            req_body = request.headers
            # req_body = await request.body()
            response = await original_route_handler(request)
            tasks = response.background

            if isinstance(response, StreamingResponse):
                res_body = b""
                async for item in response.body_iterator:
                    res_body += item

                task = BackgroundTask(log_info, req_body, res_body)
                response = Response(
                    content=res_body,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=response.media_type,
                )
            else:
                task = BackgroundTask(log_info, req_body, response.body)

            # check if the original response had background tasks already attached to it
            if tasks:
                tasks.add_task(task)  # add the new task to the tasks list
                response.background = tasks
            else:
                response.background = task

            return response

        return custom_route_handler


app = FastAPI()
router = APIRouter(route_class=LoggingRoute)
logging.basicConfig(filename="info.log", level=logging.DEBUG)


@router.get("/")
async def home():
    return "Welcome to Google Ads services"


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.add_middleware(SessionMiddleware, secret_key="add any string...")

app.include_router(router=email_router, dependencies=[Depends(check_permission)])

app.include_router(
    router=ads_router, prefix="/ads", dependencies=[Depends(check_permission)]
)

app.include_router(
    router=account_router, prefix="/account", dependencies=[Depends(check_permission)]
)


app.include_router(
    router=provider_router, prefix="/provider", dependencies=[Depends(check_permission)]
)

app.include_router(
    router=request_router, prefix="/request", dependencies=[Depends(check_permission)]
)

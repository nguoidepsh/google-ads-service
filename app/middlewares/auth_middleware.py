from typing import Annotated

import requests
from fastapi import Header, HTTPException, Request


async def check_permission(
    request: Request,
    Authorization: str = Header(default=None),
    x_client_id: str = Header(default=None),
):
    # request.state.auth_data = {"uuid": "130995", "email": "nguoidepsh@gmail.com"}
    response = requests.post(
        "https://authoritysitemaster.com/wp-json/api/v2/checkPermission",
        data={"Authorization": Authorization, "x-client-id": x_client_id},
        headers={"User-Agent": "Mozilla/5.0"},
        verify=False,
    )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    # Add response data to request state
    request.state.auth_data = response.json()

from typing import Any, Optional

from asgi_correlation_id.context import correlation_id
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel


def response_handler(
    data=None, status: int = status.HTTP_200_OK, message: Optional[str] = None
) -> dict[str, Any]:
    """
    This function is used to handle responses in a unified way

    :param data: data to be returned in the response
    :param status: status code of the response
    :param message: message to be returned in the response

    :return: dict[str, Any]
    """

    if not message:
        match status:
            case 200:
                message = "Data retrieved successfully"
            case 201:
                message = "Data created successfully"
            case 202:
                message = "Data updated successfully"
            case 400:
                message = "Bad Request"
            case 401:
                message = "Unauthorized"
            case 403:
                message = "Forbidden"
            case 404:
                message = "Not Found"
            case 500:
                message = "Internal Server Error"
            case _:
                message = None

    #  in case the status code is not provided
    if not message:
        if 200 <= status < 300:
            message = "Data retrieved successfully"
        elif 300 <= status < 400:
            message = "User redirected"
        elif 400 <= status < 500:
            message = "Bad Request"
        else:
            message = "OK"

    return JSONResponse(
        status_code=status,
        content=jsonable_encoder(
            ResponseModel(
                data=data,
                status=status,
                message=message,
                request_id=correlation_id.get(),
            )
        ),
    )


class ResponseModel(BaseModel):
    """
    Response Model to be used in responses
    """

    data: Any
    status: int
    message: str
    request_id: str

import structlog
from asgi_correlation_id.context import correlation_id
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            structlog.stdlib.get_logger("api.error").exception(e, exc_info=False)
            if len(e.args) != 2:
                return JSONResponse(
                    status_code=500,
                    content=jsonable_encoder(
                        {
                            "status": 500,
                            "message": str(e),
                            "data": None,
                            "request_id": correlation_id.get(),
                        },
                    ),
                )

            return JSONResponse(
                status_code=e.args[0],
                content={
                    "status": e.args[0],
                    "message": e.args[1],
                    "data": None,
                    "request_id": correlation_id.get(),
                },
            )

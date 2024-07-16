from typing import Any
from fastapi import APIRouter, Depends, status

from app.api.v1 import dependencies as deps
from app.core.constants import ResponseMessages
from app.core.database import check_mongo_connection
from app.core.utils import ResponseModel, response_handler

router = APIRouter()


@router.get(
    "", dependencies=[Depends(check_mongo_connection)], response_model=ResponseModel
)
async def health_check(
    msg: str = Depends(deps.message_locale(ResponseMessages.Healthy)),
) -> dict[str, Any]:
    return response_handler(status=status.HTTP_200_OK, message=msg)

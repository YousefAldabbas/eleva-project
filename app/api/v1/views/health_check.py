from fastapi import APIRouter, Depends, status

from app.core.constants import ResponseMessages
from app.core.database import check_mongo_connection
from app.core.utils import ResponseModel, response_handler

router = APIRouter()


@router.get(
    "", dependencies=[Depends(check_mongo_connection)], response_model=ResponseModel
)
async def health_check():
    """
    API endpoint to check the health of the application.
    """
    return response_handler(status=status.HTTP_200_OK, message=ResponseMessages.Healthy)

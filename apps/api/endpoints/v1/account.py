from fastapi import APIRouter, Request

from apps.api import schemas
from apps.db_model.statistics import Statistics

router = APIRouter()


@router.get(
    "/me",
    response_model=schemas.AccountInfo,
    responses={**schemas.code_401},
)
async def account_info(request: Request):
    """
    # Retrieve account information.

    ## Exceptions:
    - `401` : If the user is not authorized.
    """
    user = request.user
    data = await Statistics.async_account_info(user)
    return data

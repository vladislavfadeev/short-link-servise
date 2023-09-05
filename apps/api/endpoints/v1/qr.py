from typing import Annotated
from pydantic import UUID4

from fastapi import APIRouter, Request, Response, HTTPException, status, Query
from asgiref.sync import sync_to_async

from apps.api import schemas
from apps.db_model.models import QRCodeModel

router = APIRouter()


@router.get(
    "/", response_model=list[schemas.QRCodeRetrieve], responses={**schemas.code_401}
)
async def qr_list(
    request: Request,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=0)] = 10,
):
    """
    # Get a list of QR-Codes created by the user.

    ## Parameters:
    - `skip` : The count of codes to skip from the beginning. Defaults to 0.
    - `limit` : The maximum count of codes to show. Defaults to 10.

    ## Exceptions:
    - `401` : If the user is not authorized.
    """
    user = request.user
    data = await sync_to_async(list)(QRCodeModel.objects.filter(user=user)[skip:limit])
    return data


@router.get(
    "/{uuid}",
    response_model=schemas.QRCodeRetrieve,
    responses={**schemas.code_401, **schemas.code_404},
)
async def qr_detail(request: Request, uuid: UUID4):
    """
    # Retrieve QR-Code information.

    ## Exceptions:
    - `401` : If the user is not authorized.
    - `404` : If the qr does not exist.
    """
    user = request.user
    try:
        data = await QRCodeModel.objects.aget(user=user, slug=uuid)
    except QRCodeModel.DoesNotExist:
        raise HTTPException(
            status_code=404, detail="You do not have created qr with such a uuid"
        )
    return data


@router.post("/", response_model=schemas.QRCodeRetrieve, responses={**schemas.code_401})
async def qr_create(item: schemas.QRCodeCreate, request: Request):
    """
    # Create a new qr-code.

    ## Exceptions:
    - `401` : If the user is not authorized.
    - `422` : If you have validation error.
    """
    obj = await QRCodeModel.objects.acreate(user=request.user, **item.dict())
    return obj


@router.post(
    "/multiple",
    response_model=list[schemas.QRCodeRetrieve],
    responses={**schemas.code_401, **schemas.code_413},
)
async def qr_multiple_create(items: list[schemas.QRCodeCreate], request: Request):
    """
    # Multiple create a new qr-codes.

    ## Items quantity must be less or equal 70.
    ## For free use, requests quantity cannot exceed 5 per minute and 50 per day. If you need more email us.
    
    ## Exceptions:
    - `401` : If the user is not authorized.
    - `413` : If you send too much items.
    - `422` : If you have validation error.
    """
    if len(items) > 70:
        return Response(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
    models = [QRCodeModel(user=request.user, **item.dict()) for item in items]
    obj = await QRCodeModel.objects.abulk_create(models)
    return obj


@router.delete("/{uuid}", status_code=204, responses={**schemas.code_401})
async def qr_delete(uuid: UUID4, request: Request):
    """
    # Delete a qr-code by its uuid.

    ## Parameters:
    - `uuid` : The unique identifier of the qr-code.

    ## Exceptions:
    - `401` : If the user is not authorized.
    - `404` : If the specified qr-code does not exist.
    """
    user = request.user
    try:
        await QRCodeModel.objects.get(user=user, slug=uuid).adelete()
    except QRCodeModel.DoesNotExist:
        raise HTTPException(status_code=404, detail="QR does not exist")
    else:
        return Response(status_code=204)

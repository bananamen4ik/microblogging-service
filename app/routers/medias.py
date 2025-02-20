"""API medias for interaction with medias."""

from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Header,
    HTTPException,
    status,
    UploadFile,
    File
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_session
from app.crud.users import get_user_by_api_key
from app.models.users import User
from app.schemas.medias import MediaSchema
from app.logic.medias import upload_image
from app.config import (
    RESULT_KEY,
    HTTP_EXCEPTION_USER_API_KEY_INVALID
)

router: APIRouter = APIRouter(prefix="/api/medias")


@router.post("")
async def api_upload_image(
        session: Annotated[AsyncSession, Depends(get_session)],
        api_key: Annotated[str, Header()],
        image_file: Annotated[UploadFile, File(alias="file")]
) -> dict:
    """Upload image."""
    user_model: User | None = await get_user_by_api_key(
        session,
        api_key
    )

    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=HTTP_EXCEPTION_USER_API_KEY_INVALID
        )

    image: MediaSchema | None = await upload_image(
        session,
        user_model.id,
        image_file
    )

    if image is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=HTTP_EXCEPTION_USER_API_KEY_INVALID
        )

    return {
        RESULT_KEY: True,
        "media_id": image.id
    }

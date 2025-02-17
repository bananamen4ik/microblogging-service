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
from app.schemas.users import UserSchema
from app.crud.users import get_user_by_api_key
from app.crud.medias import upload_image

router: APIRouter = APIRouter(prefix="/api/medias")


@router.post("")
async def api_upload_image(
        session: Annotated[AsyncSession, Depends(get_session)],
        api_key: Annotated[str, Header()],
        image_file: Annotated[UploadFile, File(alias="file")]
) -> dict:
    """Upload image."""
    user: UserSchema | None = await get_user_by_api_key(
        session,
        api_key
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user was not found by api_key."
        )

    media_id: int | None = await upload_image(
        session,
        user,
        image_file
    )

    if media_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The file is not valid image."
        )

    return {
        "result": True,
        "media_id": media_id
    }

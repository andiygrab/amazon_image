from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session

from amazon import s3_client
from core.config import settings
from utils.crud import get_images, get_image, delete_image, create_image
from utils.schemas import Image
from app.auth.route_login import get_current_user
from db.engine import get_db
from db.models import User

router = APIRouter()


@router.get("/images/", response_model=list[Image])
async def images(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    images = get_images(db, skip=skip, limit=limit)
    params = {
        "Bucket": settings.BUCKET_NAME,
    }
    for image in images:
        params["Key"] = image.image_url
        image.upload_url = s3_client.generate_presigned_url(
            "get_object",
            Params=params,
            ExpiresIn=300
        )
        # add presigned url to image for send it to front-end, for every request we make new url without store in db
    return images


@router.delete("/images/{image_id}")
async def delete_image_api(
        image_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.role != "Admin":
        raise HTTPException(status_code=403, detail="You don`t have permission")

    image = get_image(db, image_id=image_id)

    if not image:
        raise HTTPException(status_code=400, detail="Image does not exist")
    elif image.is_deleted:
        raise HTTPException(status_code=400, detail="Image is already deleted")
    delete_image(db, image_id=image_id, user=current_user)
    return HTTPException(status_code=200, detail="Image deleted")


@router.post("/images/", response_model=Image)
async def create_image_api(
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return create_image(db, file, current_user)

from utils.crud import create_new_user, get_user
from db.engine import get_db
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi import status
from utils.schemas import User
from utils.schemas import UserCreate
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_exist = get_user(db, user.username)
    if user_exist:
        raise HTTPException(status_code=400, detail="User with this username already exist")
    else:
        user = create_new_user(user=user, db=db)
        return user

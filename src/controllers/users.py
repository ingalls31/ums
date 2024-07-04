from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

# from src.routes.auth.service import get_current_active_user
from src.util.db_dependency import get_db
from src.services.users import *
from src.schemas.users import User

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)
# @router.get("/")
# async def get_all_users(user: User = Depends(get_current_active_user),
#                         db: Session = Depends(get_db)):
#     if user.super_admin:
#         return get_users_admin(db=db)
#     else:
#         return get_users(db=db)


def get_user_by_id(user_id: int, db: Session):
    user = db.query(User.id, User.first_name, User.last_name, User.email, User.super_admin, User.disabled).filter(
        User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="There is no user with this id."
        )

    return user

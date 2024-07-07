from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

# from src.routes.auth.service import get_current_active_user
from src.config.database import SessionLocal
from src.util.db_dependency import get_db
from src.services.users import *
from src.schemas.users import UserSchema

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# @router.get("/")
# async def get_all_users(user: User = Depends(get_current_active_user),
#                         db: Session = Depends(get_db)):
#     if user.super_admin:
#         return get_users_admin(db=db)
#     else:
#         return get_users(db=db)

@router.post("/", response_model=UserSchema)
def create_user(user_data: UserSchema, db: Session = Depends(get_db)):
    """
    Creates a new user in the database with the provided user data.

    Args:
        user_data (UserSchema): The data of the user to be created.
        db (Session): The database session to use.

    Returns:
        UserSchema: The newly created user.

    Raises:
        None.
    """
    # Create a new User object with the provided user data
    user = User(
        id=123,  # TODO: Generate a unique id
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        password=user_data.password,
        gender=user_data.gender,
        phone=user_data.phone,
        dob=user_data.dob,
        address=user_data.address,
        super_admin=user_data.super_admin,
        disabled=user_data.disabled
    )

    # Add the new user to the database
    db.add(user)
    db.commit()

    # Refresh the user object to get the updated database values
    db.refresh(user)

    return user

# def get_user_by_id(user_id: int, db: Session):
#     user = db.query(User.id, User.first_name, User.last_name, User.email, User.super_admin, User.disabled).filter(
#         User.id == user_id).first()

#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="There is no user with this id."
#         )

#     return user

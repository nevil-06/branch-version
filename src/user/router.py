from typing import List
from src.user.model import User
from sqlalchemy.orm import Session
from src.utils.current_user import JWTBearer
from src.utils.token import create_access_token, create_refresh_token, decode_access_token
from src.utils.db_session_create import get_db
from fastapi import APIRouter, Depends, status, HTTPException, Request
from src.utils.hahspassword import get_password_hash, verify_password
from src.user.schema import UserTable, UserResponse, UserCreate, UserLogin, LoggedInUser
from src.utils.hahspassword import outh2_scheme

user_router = APIRouter()


# user routes
# get all users that are not deleted 
@user_router.get('/users/all', status_code = status.HTTP_200_OK, response_model= List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).filter(User.is_deleted != True).all()
    return users


# get 1 user that is not not deleted 
@user_router.get('/get/user/{id}', status_code = status.HTTP_200_OK)
def get_user(id: str, db: Session = Depends(get_db)):
    one_user = db.query(User).filter(
        User.id == id, User.is_deleted != True).first()
    if one_user:
        return one_user
    else: 
        return {"message" :  "user is already deleted"}



# get only users that are deleted 
@user_router.get('/users/del', status_code=200, response_model= List[UserResponse])
def get_all_deleted_users(db: Session = Depends(get_db)):
    users = db.query(User).filter(User.is_deleted == True).all()
    if users:
        return users
    else:
        return {"message": "User might not be deleted or some other error"}


#admin function to see full data 
@user_router.get('/admin/users/all')
def admin_get_all(db: Session = Depends(get_db)):
        users = db.query(User).filter(User.is_deleted != True).all()
        return users


# create new user and provide their details
@user_router.post('/users', status_code= status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(
        User.email == user.email).first()
    try:    
        if db_user:
            return {"message": "user already exists with this email id"}
        else:
            new_user = User(
                name = user.name,
                password = get_password_hash(user.password),
                email = user.email)
            
            db.add(new_user)
            
            db.commit()
            return {"message" : "user created successfully"}
    except Exception as e:
        return e



# update user and their desired values
@user_router.put('/user/{id}', status_code= status.HTTP_202_ACCEPTED)
def update_user(id: str, user: UserTable, db: Session = Depends(get_db)):
    updateuser = db.query(User).filter(
        User.id == id, User.is_deleted == False).first()

    if updateuser:
        updateuser.update_fields(user.dict())
        db.add(updateuser)
        db.commit()
        return {"message" : "user details updated"}
        
    else:
        return {"message : User is deleted so cannot update"}



# delete user that you want to
@user_router.delete('/user/del/{id}')
def delete_user(id: str, db: Session = Depends(get_db)):
    deleteuser = db.query(User).filter(
        User.id == id).first()

    if deleteuser.is_deleted != True:
        deleteuser.is_deleted = True
        db.commit()
        return {"message" : "user deleted successfully"}

    elif deleteuser.is_deleted == True:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail ="user is already deleted")


# user login api
@user_router.post('/user/login', status_code= status.HTTP_200_OK)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User.password, User.email).filter(
        User.email == user.email).first()

    if db_user and verify_password(user.password, db_user.password): 
        return{ "message" : "user login successful",
                "access_token": create_access_token(User.email),
                "refresh_token": create_refresh_token(User.email)
            }   
    elif  db_user.password != user.password:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "user not found, please check credentials and try again")


@user_router.get(
    "/user/me",
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_200_OK,
)
def display_user(request: Request, db: Session = Depends(get_db)):
    access_token = request.headers["authorization"][7:]
    payload = decode_access_token(access_token)

    try:
        user_id = payload["sub"]
        user = db.query(User).filter(User.id == user_id).first()

    except KeyError as exception:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="Access token is expired"
        ) from exception

    return {user: "successful login"}

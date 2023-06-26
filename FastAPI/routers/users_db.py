from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId, errors


# Inicia el server: $ uvicorn users:app --reload

router = APIRouter(prefix='/userdb',
                   tags = ['users_db'], 
                   responses={status.HTTP_404_NOT_FOUND: {'message': 'No encontrado'}})




@router.get('/all', response_model=list[User])
async def users():
    return users_schema(db_client.users.find())

# Path
@router.get('/{id}', response_model=User, status_code=status.HTTP_200_OK)
async def user(id: str):
    try:
        user = search_user('_id', ObjectId(id))
        return user
    except errors.InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='ID no válido')

# Query
@router.get('/', response_model=User, status_code=status.HTTP_200_OK)
async def user(id: str):
    try:
        user = search_user('_id', ObjectId(id))
        return user
    except errors.InvalidId:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='ID no válido')

def search_user(field: str, value):
    db_user = db_client.users.find_one({field: value})
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuario no encontrado')
    user = user_schema(db_user)
    return User(**user)

# ---- POST ----
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user: User):
    user_dict = dict(user)
    del user_dict['id']
    if db_client.users.find_one({"username": user_dict['username']}) != None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists')
    id = db_client.users.insert_one(user_dict).inserted_id
    new_user = user_schema(db_client.users.find_one({"_id": id}))
    return User(**new_user)
    

# ---- PUT ----
@router.put('/')
async def update_user(user: User):
    user_dict = dict(user)
    del user_dict['id']
    updated_user = db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict, return_document=True)
    if updated_user == None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found')
    return User(**user_schema(updated_user))


@router.delete('/{username}')
async def delete_user(username: str):
    deleted_count = db_client.users.delete_one({'username': username}).deleted_count
    if deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found')
    return deleted_count
    
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from db.models.user import User
from db.schemas.user import user_schema 
from db.client import db_client


# Inicia el server: $ uvicorn users:app --reload

router = APIRouter(prefix='/userdb',
                   tags = ['users_db'], 
                   responses={status.HTTP_404_NOT_FOUND: {'message': 'No encontrado'}})








@router.get('/all')
async def users():
    all_users = db_client.test_db.users.find()
    return all_users
# Path
@router.get('/{username}')
async def user(username: str):
    return search_user(username)


# Query
@router.get('/')
async def user(username: str):
    return search_user(username)

def search_user(username: str):
    user = user_schema(db_client.test_db.users.find_one({'username': username}))
    return User(**user)

# ---- POST ----
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user: User):
    #if type(search_user(user.id)) == User:
    #    raise HTTPException(status_code=404, detail='User already exists')
    #else:
        #users_list.append(user)
    user_dict = dict(user)
    del user_dict['id']
    id = db_client.test_db.users.insert_one(user_dict).inserted_id
    new_user = user_schema(db_client.test_db.users.find_one({"_id": id}))
    return User(**new_user)
    

# ---- PUT ----
@router.put('/')
async def update_user(user: User):
    for i, user_saved in enumerate(users_list):
        if user.id == user_saved.id:
            users_list[i] = user
            return user
    return {'error': 'No se ha encontrado el usuario'}


@router.delete('/{user_id}')
async def delete_user(user_id: int):
    try:
        users_list.remove(search_user(user_id))
        return {'User deleted'}
    except:
        return {'Error': 'User not found'}
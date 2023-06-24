from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Inicia el server: $ uvicorn users:app --reload
router = APIRouter(tags=['users'])


# Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


users_list = [User(id=1, name='Pepito', surname='Pepe', url='pepe.com', age=18),
         User(id=2, name='Pedro', surname='Paco', url='pedro.com', age=23),
         User(id=3, name='Juan', surname='Juancho', url='juan.com', age=50)]


@router.get('/usersjson')
async def usersjson():
    return 'Hola Users!'


@router.get('/users')
async def users():
    return users_list

# Path
@router.get('/user/{id}')
async def user(id: int):
    return search_user(id)


# Query
@router.get('/user/')
async def user(id: int):
    return search_user(id)

def search_user(id: int):
    try: 
        return list(filter(lambda x: x.id == id, users_list))[0]
    except: 
        return {'error': 'No se ha encontrado el usuario'}

# ---- POST ----
@router.post('/user/', status_code=201, response_model=User)
async def create_user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail='User already exists')
        
    else:
        users_list.append(user)
        return user

# ---- PUT ----
@router.put('/user/')
async def update_user(user: User):
    for i, user_saved in enumerate(users_list):
        if user.id == user_saved.id:
            users_list[i] = user
            return user
    return {'error': 'No se ha encontrado el usuario'}


@router.delete('/user/{user_id}')
async def delete_user(user_id: int):
    try:
        users_list.remove(search_user(user_id))
        return {'User deleted'}
    except:
        return {'Error': 'User not found'}
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl='login')


# Entidad user
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    'martin_o': {
        'username': 'martin_o',
        'full_name': 'Martin Ostios',
        'email': 'martin@gmail.com',
        'disabled': False,
        'password': '123456'
    },
    'pepito123': {
        'username': 'pepito123',
        'full_name': 'Pepito Perez',
        'email': 'pepe@gmail.com',
        'disabled': True,
        'password': '654321'
    },
    'carlos123': {
        'username': 'carlos123',
        'full_name': 'Carlos Antonio',
        'email': 'carlos@gmail.com',
        'disabled': False,
        'password': '123456'
    },
}



def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Credenciales de autenticación inválidas', 
                            headers={'WWW-Authenticate': 'Bearer'})

    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Usuario inactivo')
    return user

@app.post('/login')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail='User not found')
    
    user = search_user(form.username)
    if not form.password == user_db['password']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail='Incorrect password')

    return {'access_token': user.username, 'token_type': 'bearer'}

@app.get('/users/me')
async def me(user: User = Depends(current_user)):
    return user


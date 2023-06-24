from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 1
SECRET = 'a4c8a2ee345cf78f21016aafdf27b3b349bf2ecf6a3e52ea420a58a4c96a9052'

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl='login')

crypt = CryptContext(schemes=['bcrypt'])


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
        'password': '$2a$12$WYDHiVcq8QTjHYl26Cns/eQ.fj.ukjrRJwlQZo2RfHPW0ob2o4g/.'
    },
    'pepito123': {
        'username': 'pepito123',
        'full_name': 'Pepito Perez',
        'email': 'pepe@gmail.com',
        'disabled': True,
        'password': '$2a$12$zFCq3O.l8bCFXJURQbt2k./e9kvBUNACm/wzAzhXf99wJ0X290Qoa'
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
    
async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Credenciales de autenticación inválidas')
    try:
        token_data = jwt.decode(token, key=SECRET, algorithms=[ALGORITHM])
        username = token_data['sub']
        if username is None:
            raise exception
        user = search_user(username)
    except JWTError:
        raise exception
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Credenciales de autenticación inválidas', 
                            headers={'WWW-Authenticate': 'Bearer'})
    return user

async def current_user(user: User = Depends(auth_user)):
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

    if not crypt.verify(form.password, user_db['password']):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail='Incorrect password')


    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = {
        'sub': user.username,
        'exp': expire
    }

    return {'access_token': jwt.encode(access_token, SECRET ,algorithm=ALGORITHM), 'token_type': 'bearer'}


@app.get('/users/me')
async def me(user: User = Depends(current_user)):
    return user
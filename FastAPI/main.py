from fastapi import FastAPI
from routers import products, users
from fastapi.staticfiles import StaticFiles
# $ uvicorn main:app --reload
app = FastAPI(title='Proyecto', description='Probando la descripción')

# Routers

app.include_router(products.router)
app.include_router(users.router)

app.mount('/resources', StaticFiles(directory='static/images'), name='static')


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/url")
async def url():
    return {
        'name': 'Antonio',
        'age': 18,
        'city': 'Manizales'
    }
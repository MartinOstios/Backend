from fastapi import APIRouter

router = APIRouter(prefix='/products',
                   tags = ['products'], 
                   responses={404: {'message': 'No encontrado'}})

products_list = ['Producto 1', 'Producto 2', 'Producto 3', 'Producto 4', 'Producto 5']

@router.get('/')
async def get_products():
    return products_list

@router.get('/{id}', description='Get products by ID', name='Obtiene los productos por el ID')
async def get_products(id: int):
    return products_list[id]
from pymongo import MongoClient

# Conexión a base de datos local
#db_client = MongoClient().test_db

# Conexión a base de datos remota
uri = "mongodb+srv://test:test@cluster0.hcwvvuq.mongodb.net/?retryWrites=true&w=majority"
db_client = MongoClient(uri).test


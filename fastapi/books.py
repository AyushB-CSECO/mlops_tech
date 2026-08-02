from fastapi import FastAPI 

app = FastAPI()

BOOKS = [
    {'title':"T_1", 'author':"Auth_1", 'category': "Fiction"},
    {'title':"T_2", 'author':"Auth_2", 'category': "Self Help"},
    {'title':"T_3", 'author':"Auth_3", 'category': "Fiction"},
    {'title':"T_4", 'author':"Auth_4", 'category': "Mythology"},
    {'title':"T_5", 'author':"Auth_5", 'category': "Fiction"},
    {'title':"T_6", 'author':"Auth_6", 'category': "Self Help"}
]

@app.get("/books")
async def read_all_books():
    return BOOKS

# Create API with dynamic parameter
@app.get("/books/{dynamic_param}")
async def read_book(dynamic_param):
    return {"dynamic_param": dynamic_param}
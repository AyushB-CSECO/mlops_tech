from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {'title':"T 1", 'author':"Auth_1", 'category': "Fiction"},
    {'title':"T 2", 'author':"Auth_2", 'category': "Self Help"},
    {'title':"T 3", 'author':"Auth_3", 'category': "Fiction"},
    {'title':"T 4", 'author':"Auth_4", 'category': "Mythology"},
    {'title':"T 5", 'author':"Auth_5", 'category': "Fiction"},
    {'title':"T 6", 'author':"Auth_6", 'category': "Self Help"}
]

@app.get("/books")
async def read_all_books():
    return BOOKS

# Get a particular book dynamically
@app.get("/books/{book_title}")
async def read_book(book_title):
    for book in BOOKS:
        if book['title'] == book_title.upper():
            return book

# Return all the books of a specific category
@app.get("/books/")
async def read_category_by_query(category: str) -> list:
    output = []
    for book in BOOKS:
        if book['category'] == category.title():
            output.append(book)
    return output

# Return all books with queried author and category
@app.get("/books/{book_author}/")
async def read_author_category_by_query(
    book_author: str,
    category: str
    ) -> list:
    output = []
    for book in BOOKS:
        if ( (book['author'] == book_author.title())  
            and (book['category'] == category.title())): 
            output.append(book)
    return output

# Create a POST API to add new book to the books list
@app.post("/books/create_book")
async def create_book(new_book = Body()):
    BOOKS.append(new_book)

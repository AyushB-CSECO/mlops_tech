from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {'title':"T 1", 'author':"Auth_1", 'category': "Fiction"},
    {'title':"T 2", 'author':"Auth_2", 'category': "Self Help"},
    {'title':"T 3", 'author':"Auth_1", 'category': "Fiction"},
    {'title':"T 4", 'author':"Auth_3", 'category': "Mythology"},
    {'title':"T 5", 'author':"Auth_1", 'category': "Fiction"},
    {'title':"T 6", 'author':"Auth_2", 'category': "Self Help"}
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

# Create a PUT API to update existing book
@app.put("/books/update_book")
async def update_book(updated_book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title") == updated_book.get('title').upper():
            BOOKS[i] = updated_book

# Create a DELETE API to delete an existing book
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title:str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title") == book_title.upper():
            BOOKS.pop(i)
            break

# Create a GET API that can fetch all books from a specific author
# using either Path Parameter or Query Parameter
@app.get("/books/get_author/{author}")
async def get_books_by_author_path(author:str):
    output = []
    for book in BOOKS:
        if book.get("author") == author.title():
            output.append(book)
    return output
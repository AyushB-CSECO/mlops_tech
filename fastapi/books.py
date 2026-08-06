from fastapi import FastAPI
from fastapi import Path, Query
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

class Book:
    id: int 
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description
                 , rating, published_date):
        self.id = id 
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

# Create a class for new books from user. Use pydantic for validation
class BookRequest(BaseModel):
    id: Optional[int] = Field(description = "ID is not necessary at create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length= 1)
    description: str = Field(min_length=1, max_length=100 )
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(lt=2027)

BOOKS = [
    Book(1, "Animal Farm", "George Orwell", "Political Satire", 5, 1947),
    Book(2, "Atomic Habbits", "James Clear", "Helps in building good habbits", 4, 2004),
    Book(3, "Five Point Someone", "Chetan Bhagat", "Story about College Friends", 3, 2009),
    Book(4, "Revolution 2020", "Chetan Bhagat", "Struggles of an average middle class boy", 4, 2010),
    Book(5, "The Rudest Book Ever", "Shwetabh Gangwar", "Self Help Book on Life", 5, 2016),
    Book(6, "Let Us C", "Yashwant Kanetkar", "Book on C++ coding", 4, 1999)
]

def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book 

@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}")
async def read_book(book_id:int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book

@app.get("/books/")
async def read_book_by_rating(rating: int = Query(gt=0, lt=6)):
    output = [book for book in BOOKS if book.rating == rating]
    return output

@app.get("/books/publish/{published_date}")
async def read_book_by_date(published_date: int = Path(lt=2027)):
    output = [book for book in BOOKS if book.published_date == published_date]
    return output

# Create POST API to create book
@app.post("/create-book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    new_book = find_book_id(new_book)
    BOOKS.append(new_book)

@app.put("/books/update_book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book

@app.delete("/books/delete_book/{book_id}")
async def delete_book(book_id:int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break
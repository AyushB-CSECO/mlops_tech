from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

posts: list[dict] = [
    {
        "id": 1,
        "author":"Corey Schafer",
        "title": "FastAPI is awesome",
        "content":"This framework is easy to use and superfast",
        "date_posted": "April 20, 2025"

    },
    {
        "id": 2,
        "author": "Jane Doe",
        "title": "Python is great for Web Development",
        "content":"Python is great for developing FastAPIs",
        "date_posted": "April 21, 2025"
    },
]

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
@app.get("/posts", response_class=HTMLResponse, include_in_schema=False)
def home():
    return "<h1>This is home page</h1>"

@app.get("/api/posts")
def get_posts():
    return posts
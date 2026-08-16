from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

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

@app.get("/", include_in_schema=False)
@app.get("/posts", include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(request,"home.html", {"posts":posts})

@app.get("/api/posts")
def get_posts():
    return posts
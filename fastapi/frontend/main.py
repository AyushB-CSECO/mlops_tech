from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
def home_page():
    return FileResponse(path='index.html')
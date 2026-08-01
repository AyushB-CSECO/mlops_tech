from fastapi import FastAPI 

app = FastAPI()

@app.get("/")
async def greet_user():
    return {"message": "Hello, World"}
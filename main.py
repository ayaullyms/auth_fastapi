from fastapi import FastAPI, Body, Depends
from app.model import *
from app.auth.handler import signJWT
from app.auth.bearer import Bearer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

users = []
posts = [
    {
        "title": "Cats",
        "description": "All about cats.",
        "author": "Ayaulym"
    }
]


@app.get("/")
def root():
    return {"message": "heyyyyy"}

def verify_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False

@app.get("/posts")
def get_posts():
    return posts

@app.post("/posts", dependencies=[Depends(Bearer())])
def create_post(post: PostSchema = Body(...)):
    posts.append(post)
    return post

@app.post("/user/signup")
def create_user(user: UserSchema = Body(...)):
    users.append(user)
    return signJWT(user.email)

@app.post("/user/signin")
def login_user(user: UserLoginSchema = Body(...)):
    if verify_user(user):
        return signJWT(user.email)
    return {"error": "Invalid credentials :("}

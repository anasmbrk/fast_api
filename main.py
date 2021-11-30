from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel


app = FastAPI()


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

@app.post('/blog')
def create_blog(request: Blog):
    return {'data':f'blog created with title {request.title}'}

@app.get('/')
def index():
    return {'data': 'Blog list'} 

@app.get('/about')
def about():
    return {'data':'about page'}

@app.get('/blog/unpublished')
def unpublished():
    return {'data':'unpublished'}

@app.get('/blog/{id}')
def show(id:int):
    return {'data': id}



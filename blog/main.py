from fastapi import FastAPI, Depends, status, Response,\
    HTTPException
from fastapi.param_functions import Body
from sqlalchemy.orm.session import Session
from .schemas import Blog
from .database import SessionLocal, engine
from . import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create_blog(request: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog')
def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}')
def all_blogs(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog {id} not found')

    return blog

@app.delete('/blog/{id}',status_code= status.HTTP_204_NO_CONTENT)
def delete_blog(id:int,db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return Response()

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id:int, request: Blog,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if  blog.first():
        blog.update({'title':request.title, 'body':request.body})
        db.commit() 

        return {'data':'Updated'}
    else:

        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail = 'Not found')
   
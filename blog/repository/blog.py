
from fastapi import Depends,HTTPException,status
from .. import models, schemas
from sqlalchemy.orm.session import Session

def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create(request:schemas,db: Session):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def destroy(id:int,db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id ==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog {id} not found')
    
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'

def update(id:int,request:schemas, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if blog.first():
        blog.update({'title': request.title, 'body': request.body})
        db.commit()
        return {'data': 'Updated'}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Not found')

def show(id:int,db: Session):
        blog = db.query(models.Blog).filter(models.Blog.id == id).first()
        if not blog:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog {id} not found')

        return blog
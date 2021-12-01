from fastapi import Depends, status, Response, APIRouter
from typing import List

from blog.oauth2 import get_current_user
from .. import schemas, database
from sqlalchemy.orm.session import Session

from ..repository import blog

from .. import oauth2

router = APIRouter(prefix="/blog", tags=["blog"])


@router.get('/', response_model=List[schemas.ShowBlog])
def all_blogs(db: Session = Depends(database.get_db),
              current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.get_all(db)


@router.post('/', status_code=status.HTTP_201_CREATED,)
def create_blog(request: schemas.Blog,
                db: Session = Depends(database.get_db),
                current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.create(request, db)


@router.get('/{id}', response_model=schemas.ShowBlog,)
def get_blogs(id: int, response: Response,
              db: Session = Depends(database.get_db),
              current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.show(id, db)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT,)
def delete_blog(id: int,
                db: Session = Depends(database.get_db),
                current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.destroy(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED,)
def update(id: int, request: schemas.Blog,
           db: Session = Depends(database.get_db),
           current_user: schemas.User = Depends(oauth2.get_current_user)):

    return blog.update(id, request, db)

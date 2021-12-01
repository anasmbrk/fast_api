
from fastapi import Depends, status, Response,\
    APIRouter
from typing import List
from .. import schemas, database
from sqlalchemy.orm.session import Session
from ..repository import user
router = APIRouter(prefix="/user", tags=["user"])


@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    return user.create(request, db)


@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id: int, response: Response, db: Session = Depends(database.get_db)):
    return user.get(id, db)

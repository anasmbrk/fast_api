from fastapi import FastAPI



from .routers import blog,user, authentication
from .database import  engine
from . import models


app = FastAPI()
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)
models.Base.metadata.create_all(bind=engine)







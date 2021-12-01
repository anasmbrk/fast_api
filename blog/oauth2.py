from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer,\
    OAuth2PasswordRequestForm
from .token import verity_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verity_token(token,credentials_exception)


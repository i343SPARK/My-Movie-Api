from fastapi.security import HTTPBearer
from utils.jwt_manager import validate_token
from fastapi import HTTPException, Request


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@hotmail.com":
            raise HTTPException(status_code=403, detail="No tienes permisos para acceder a este recurso")

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, FastAPI, Response
from fastapi.responses import JSONResponse

class Error_handler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    async def dispatch(self, request: Response, call_next) -> Response | JSONResponse:
        try:
            return await call_next(request)
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": str(e)})
from fastapi import FastAPI
from config.database import engine, Base
from middlewares.error_handler import Error_handler
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()
app.title = "Mi aplicación con  FastAPI"
app.version = "0.0.1"

app.add_middleware(Error_handler)
app.include_router(movie_router)
app.include_router(user_router)


Base.metadata.create_all(bind=engine)

movies_list = [
    {
		"id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	},
    {
		"id": 2,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	}
]
from pydantic import BaseModel, Field
from typing import Optional

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(max_length=15, min_length=5)
    overview: str = Field(max_length=50, min_length=15)
    year: int = Field(le=2023, ge=1900)
    rating: float = Field(ge=1, le=10)
    category: str = Field(max_length=30, min_length=5)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Tu pelicula",
                "overview": "La descripcion de tu pelicula",
                "year": 2023,
                "rating": 7.8,
                "category": "La categoria de tu pelicula"
            }
        }
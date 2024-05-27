from pydantic import BaseModel


class CategoryScheme(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True



class CategoryAddScheme(BaseModel):
    name: str


class CategoryUpdateScheme(BaseModel):
    name: str | None = None

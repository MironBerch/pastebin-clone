from pydantic import BaseModel


class CustomBaseSchema(BaseModel):
    class Config:
        from_attributes = True
        populate_by_name = True

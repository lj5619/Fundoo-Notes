from pydantic import BaseModel

class LabelBase(BaseModel):
    name: str
    user_id: int

class LabelCreate(LabelBase):
    pass

class LabelOut(LabelBase):
    id: int

    class Config:
        orm_mode = True

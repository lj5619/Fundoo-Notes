from pydantic import BaseModel

class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    user_id: int

class NoteOut(NoteBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

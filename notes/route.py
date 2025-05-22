from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from notes import model, schema
from db.database import get_db

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)

@router.post("/", response_model=schema.NoteOut)
def create_note(note: schema.NoteCreate, db: Session = Depends(get_db)):
    db_note = model.Note(title=note.title, content=note.content, user_id=note.user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.get("/{note_id}", response_model=schema.NoteOut)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(model.Note).filter(model.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/{note_id}", response_model=schema.NoteOut)
def update_note(note_id: int, updated_note: schema.NoteBase, db: Session = Depends(get_db)):
    note = db.query(model.Note).filter(model.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note.title = updated_note.title
    note.content = updated_note.content
    db.commit()
    db.refresh(note)
    return note

@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(model.Note).filter(model.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"detail": "Note deleted successfully"}

@router.get("/user/{user_id}", response_model=list[schema.NoteOut])
def get_notes_by_user(user_id: int, db: Session = Depends(get_db)):
    notes = db.query(model.Note).filter(model.Note.user_id == user_id).all()
    return notes

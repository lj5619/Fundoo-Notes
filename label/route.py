from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from label import model, schema
from db.database import get_db

label_router = APIRouter(
    prefix="/labels",
    tags=["Labels"]
)

@label_router.post("/", response_model=schema.LabelOut)
def create_label(label: schema.LabelCreate, db: Session = Depends(get_db)):
    db_label = model.Label(name=label.name, user_id=label.user_id)
    db.add(db_label)
    db.commit()
    db.refresh(db_label)
    return db_label

@label_router.get("/{label_id}", response_model=schema.LabelOut)
def get_label(label_id: int, db: Session = Depends(get_db)):
    label = db.query(model.Label).filter(model.Label.id == label_id).first()
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")
    return label

@label_router.put("/{label_id}", response_model=schema.LabelOut)
def update_label(label_id: int, updated_label: schema.LabelBase, db: Session = Depends(get_db)):
    label = db.query(model.Label).filter(model.Label.id == label_id).first()
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")
    label.name = updated_label.name
    label.user_id = updated_label.user_id
    db.commit()
    db.refresh(label)
    return label

@label_router.delete("/{label_id}")
def delete_label(label_id: int, db: Session = Depends(get_db)):
    label = db.query(model.Label).filter(model.Label.id == label_id).first()
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")
    db.delete(label)
    db.commit()
    return {"detail": "Label deleted successfully"}

@label_router.get("/user/{user_id}", response_model=list[schema.LabelOut])
def get_labels_by_user(user_id: int, db: Session = Depends(get_db)):
    labels = db.query(model.Label).filter(model.Label.user_id == user_id).all()
    return labels

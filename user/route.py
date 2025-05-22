from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from user import model, schema, hash
from db.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/register", response_model=schema.UserOut)
def register(user: schema.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(model.User).filter((model.User.email == user.email) | (model.User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered with this email or username.")
    hashed_password = hash.hash_password(user.password)
    db_user = model.User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login")
def login(user: schema.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(model.User).filter(model.User.email == user.email).first()
    if not db_user or not hash.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return {"message": "Login successful", "user_id": db_user.id, "username": db_user.username, "email": db_user.email}

@router.get("/{user_id}", response_model=schema.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=schema.UserOut)
def update_user(user_id: int, updated_user: schema.UserCreate, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.username = updated_user.username
    user.email = updated_user.email
    user.password = hash.hash_password(updated_user.password)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}

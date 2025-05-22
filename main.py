from fastapi import FastAPI
from db.database import engine, Base
from user import route as user_route
from notes import route as notes_route
from label.route import label_router

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(user_route.router)
app.include_router(notes_route.router)
app.include_router(label_router)

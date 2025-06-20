from fastapi import FastAPI
from app.database import Base, engine
from app.routers import users, surveys

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Encuestas")

app.include_router(users.router)
app.include_router(surveys.router)


@app.get("/")
def read_root():
    return {"message": "Encuestas API"}

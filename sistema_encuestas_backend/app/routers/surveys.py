from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import SessionLocal

router = APIRouter(prefix="/surveys", tags=["surveys"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Survey)
def create_survey(survey: schemas.SurveyCreate, creator_id: str, db: Session = Depends(get_db)):
    return crud.create_survey(db, survey, creator_id)


@router.get("/", response_model=list[schemas.Survey])
def read_surveys(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_surveys(db, skip=skip, limit=limit)

from sqlalchemy.orm import Session
from . import models, schemas
import uuid
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(
        id=uuid.uuid4(),
        email=user.email,
        hashed_password=get_password_hash(user.password),
        full_name=user.full_name,
        role_id=user.role_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_survey(db: Session, survey: schemas.SurveyCreate, creator_id):
    db_survey = models.Survey(
        id=uuid.uuid4(),
        title=survey.title,
        description=survey.description,
        status=survey.status,
        creator_id=creator_id,
    )
    db.add(db_survey)
    db.commit()
    db.refresh(db_survey)
    return db_survey


def get_surveys(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Survey).offset(skip).limit(limit).all()

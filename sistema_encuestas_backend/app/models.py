import uuid
from sqlalchemy import Column, String, Integer, Boolean, Text, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .database import Base


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    users = relationship('User', back_populates='role')


class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(Text)
    full_name = Column(String(255))
    role_id = Column(Integer, ForeignKey('roles.id'))

    role = relationship('Role', back_populates='users')
    auth_providers = relationship('AuthProvider', back_populates='user')
    surveys = relationship('Survey', back_populates='creator')


class AuthProvider(Base):
    __tablename__ = 'auth_providers'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    provider = Column(String(50), nullable=False)
    provider_user_id = Column(String(255))

    user = relationship('User', back_populates='auth_providers')


class Survey(Base):
    __tablename__ = 'surveys'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50))
    creator_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))

    creator = relationship('User', back_populates='surveys')
    questions = relationship('Question', back_populates='survey')
    responses = relationship('Response', back_populates='survey')


class Question(Base):
    __tablename__ = 'questions'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    survey_id = Column(UUID(as_uuid=True), ForeignKey('surveys.id'))
    text = Column(Text, nullable=False)
    type = Column(String(50), nullable=False)

    survey = relationship('Survey', back_populates='questions')
    options = relationship('Option', back_populates='question')
    answers = relationship('Answer', back_populates='question')


class Option(Base):
    __tablename__ = 'options'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_id = Column(UUID(as_uuid=True), ForeignKey('questions.id'))
    text = Column(Text, nullable=False)

    question = relationship('Question', back_populates='options')
    answers = relationship('Answer', back_populates='option')


class Response(Base):
    __tablename__ = 'responses'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    survey_id = Column(UUID(as_uuid=True), ForeignKey('surveys.id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    created_at = Column(TIMESTAMP)

    survey = relationship('Survey', back_populates='responses')
    answers = relationship('Answer', back_populates='response')


class Answer(Base):
    __tablename__ = 'answers'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    response_id = Column(UUID(as_uuid=True), ForeignKey('responses.id'))
    question_id = Column(UUID(as_uuid=True), ForeignKey('questions.id'))
    option_id = Column(UUID(as_uuid=True), ForeignKey('options.id'))
    text_answer = Column(Text)

    response = relationship('Response', back_populates='answers')
    question = relationship('Question', back_populates='answers')
    option = relationship('Option', back_populates='answers')


class PointsTransaction(Base):
    __tablename__ = 'points_transactions'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    amount = Column(Integer, nullable=False)
    description = Column(Text)
    created_at = Column(TIMESTAMP)


class Reward(Base):
    __tablename__ = 'rewards'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    points_required = Column(Integer, nullable=False)
    available = Column(Boolean, default=True)


class UserReward(Base):
    __tablename__ = 'user_rewards'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    reward_id = Column(Integer, ForeignKey('rewards.id'))
    redeemed_at = Column(TIMESTAMP)

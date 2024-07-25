import os
import bcrypt
from datetime import datetime
from dotenv import load_dotenv
from sqlmodel import Field, SQLModel, create_engine, Session, select
from model import User,RegisterModel

load_dotenv()

DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_URL = (
    f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"
)

engine = create_engine(DATABASE_URL, echo=True)

# DATABASE_URL = 'sqlite:///./database.db'

engine = create_engine(DATABASE_URL, echo=True)

# Create the database tables
SQLModel.metadata.create_all(engine)

def get_user_by_username(username: str):
    with Session(engine) as db_session:
        statement = select(User).where(User.username == username)
        return db_session.exec(statement).first()
    
def create_user(user_data: RegisterModel):
        password_bytes = user_data.password.encode('utf-8')
        password_hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            username=user_data.username,
            age=user_data.age,
            city=user_data.city,
            country=user_data.country,
            jon_time = datetime.datetime.now(),
            password_hash=password_hash
        )
        with Session(engine) as db_session:
            db_session.add(user)
            db_session.commit()
            db_session.refresh(user)
        return user


def verify_password(password: str, password_hash: str) -> bool:
        password_bytes = password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, password_hash)

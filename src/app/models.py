from sqlalchemy import Column, Integer, String


from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class Tongue(Base):
    __tablename__ = "tongues"

    id = Column(Integer, primary_key=True, index=True)
    raw_string = Column(String)
    tongues_string = Column(String)

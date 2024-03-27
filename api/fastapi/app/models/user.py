from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship



class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    hashed_password = Column(String)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    # items = relationship("Item", back_populates="owner")



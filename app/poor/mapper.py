from sqlalchemy import (
    Column,
    String,
    DateTime,
    Integer
)
from bakery.lib.orm import metabase
from sqlalchemy.orm import relationship
from datetime import datetime

Basis = metabase()

"""
    User
    - 이메일
    - 닉네임
    - 프로필(사진 url?)
    - dbid
    - 가입일시
    - point
"""
class User(Basis):
    email = Column(String(255), nullable=False, unique=True)
    nickname = Column(String(15), nullable=False)
    point = Column(Integer, nullable=False, default=0)
    # my_trial = relationship("Trial", back_populates="Trial")

class Trial(Basis):
    title = Column(String(20), nullable=False)
    item = Column(String(20), nullable=False)
    price = Column(Integer, nullable=False)
    reason = Column(String(50), nullable=False)
    user = Column(String(255), nullable=False)
    # comments = relationship("TrialComment", back_populates="")
    # user = relationship("User", back_populates="")
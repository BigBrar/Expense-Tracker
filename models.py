# models.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import date

today = date.today()
formatted_date = today.strftime("%B %d, %Y")

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    data = relationship('ExpenseData', back_populates='user_data')

class ExpenseData(Base):
    __tablename__ = 'expense_data'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    payment_type = Column(Text, nullable=False)
    date = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user_data = relationship('User', back_populates='data')

engine = create_engine('sqlite:///expense.db', echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

def add_user(username, email, password):
    user = User(username=username, email=email, password=password)
    session.add(user)
    session.commit()

def add_data(username, title, amount, description, payment_type):
    user = session.query(User).filter_by(username=username).first()
    if user:
        new_data = ExpenseData(title=title, amount=amount, description=description, payment_type=payment_type, date=formatted_date, user_data=user)
        session.add(new_data)
        session.commit()

def user_exists(username, password):
    user = session.query(User).filter_by(username=username, password=password).first()
    return user is not None

def username_check(username):
    return session.query(User).filter_by(username=username).first() is not None

def get_user_data(username):
    user = session.query(User).filter_by(username=username).first()
    if user:
        user_data = session.query(ExpenseData).filter_by(user_data=user).all()
        return [{'title': entry.title, 'amount': entry.amount, 'description': entry.description,
                 'payment_type': entry.payment_type, 'date': entry.date} for entry in user_data]
    return []

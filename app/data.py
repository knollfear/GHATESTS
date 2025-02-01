import sqlalchemy as db
import os

DBConn = os.environ.get("DBConn") or "sqlite:///users2.db"

engine = db.create_engine(DBConn)

conn = engine.connect()
metadata = db.MetaData()
User = db.Table('User', metadata,
                db.Column('Id', db.Integer(), primary_key=True),
                db.Column('Name', db.String(255), nullable=False),
                db.Column('Email', db.String(255), default="Math"),
                db.Column('HighScore', db.Integer(), default=True)
                )
metadata.create_all(engine)
try:
    query = db.insert(User).values( Name='Alma', Email="a@example.com", HighScore=2019)
    conn.execute(query)
    query = db.insert(User).values( Name='Beta', Email="b@example.com", HighScore=2015)
    conn.execute(query)
except Exception as e:
    print(e)
finally:
    conn.commit()

def init():
    print("Init DB")

def get_users():
    users = conn.execute(User.select()).fetchall()
    print(users)
    return users


def add_user(name, email, highscore):
    query = db.insert(User).values(Name=name, Email=email, HighScore=highscore)
    engine = db.create_engine(DBConn)
    conn = engine.connect()
    result = conn.execute(query)
    conn.commit()

    return result
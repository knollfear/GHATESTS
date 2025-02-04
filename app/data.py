import sqlalchemy as db
import os
import models.recipe

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASS = os.environ.get('DB_PASSWORD', 'postgres')
DB_NAME = os.environ.get('DB_NAME', 'scarf')

DBConn = os.environ.get("DBConn") or f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = db.create_engine(DBConn)
conn = engine.connect()

metadata = db.MetaData()
User = db.Table('User', metadata,
        db.Column('Id', db.Integer(), primary_key=True),
        db.Column('Name', db.String(255), nullable=False),
        db.Column('Email', db.String(255), default="Math"),
        db.Column('HighScore', db.Integer(), default=True)
        )
Recipe = db.Table('Recipe', metadata,
      db.Column('Id', db.Integer(), primary_key=True),
      db.Column('Name', db.String(255), nullable=False),
      db.Column('PrimaryColor', db.String(255), nullable=False),
      db.Column('SecondaryColor', db.String(255), nullable=False),
      db.Column('AccentColor', db.String(255), nullable=True),
      db.Column('Veil', db.Boolean, default=True),
      db.Column('Triangle', db.Boolean, default=True),
      db.Column('Shawl', db.Boolean, default=True),
      db.Column('Infinity', db.Boolean, default=True),
      db.Column('Notes', db.String(511), nullable=True),
      )

metadata.create_all(engine)
print(User.columns.values())
print(Recipe.columns.values())


def init():
    print("Init DB Start")
    try:
        query = db.insert(User).values(Name='Alma', Email="a@example.com", HighScore=2019)
        conn.execute(query)
        query = db.insert(User).values(Name='Beta', Email="b@example.com", HighScore=2015)
        conn.execute(query)
    except Exception as e:
        print(e)
    finally:
        conn.commit()
    print("Init DB Complete")

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

def add_recipe(recipe: models.recipe.Recipe):
    query = db.insert(Recipe).values(
        Name=recipe.Name,
        PrimaryColor=recipe.PrimaryColor,
        SecondaryColor=recipe.SecondaryColor,
        AccentColor=recipe.AccentColor,
        Veil=recipe.Veil,
        Triangle=recipe.Triangle,
        Shawl=recipe.Shawl,
        Infinity=recipe.Infinity,
        Notes=recipe.Notes,
    )
    engine = db.create_engine(DBConn)
    conn = engine.connect()
    result = conn.execute(query)
    conn.commit()

    return result

def update_recipe(recipe: models.recipe.Recipe):
    query = db.update(Recipe).values(
        Name=recipe.Name,
        PrimaryColor=recipe.PrimaryColor,
        SecondaryColor=recipe.SecondaryColor,
        AccentColor=recipe.AccentColor,
        Veil=recipe.Veil,
        Triangle=recipe.Triangle,
        Shawl=recipe.Shawl,
        Infinity=recipe.Infinity,
        Notes=recipe.Notes,
    ).where(Recipe.c.Id==recipe.Id)
    engine = db.create_engine(DBConn)
    conn = engine.connect()
    result = conn.execute(query)
    conn.commit()

    return result

def get_recipe(id:int):
    recipe = conn.execute(Recipe.select().where(Recipe.c.Id == id)).fetchone()
    print(recipe)
    return recipe

def get_recipes():
    recipes = conn.execute(Recipe.select()).fetchall()
    print(recipes)
    return recipes
import time

from fastapi import FastAPI, Body, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

# models.Base.metadata.create_all(bind=engine)
app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='cpims2', user='postgres',
                                password='123Bowen', cursor_factory=RealDictCursor)
        curr = conn.cursor()
        print("Database connection was successful!!")
        break

    except Exception as error:
        print("Database connection failed!!")
        print("Error: ", error)
        time.sleep(2)


@app.get("/reg")
async def get_reg_org_unit():
    """
        used to READ all posts
    """
    curr.execute(""" SELECT * FROM ovc_facility """)
    posts = curr.fetchall()
    # posts = db.query(models.Post).all()
    return posts

# app.include_router(regperson.router)
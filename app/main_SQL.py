from fastapi import FastAPI
from fastapi import status, HTTPException, Response
from typing import Optional, List

from pydantic import BaseModel
import random
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:

    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="L1verp00lfc",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)


def find_post(post_id):
    for post in my_posts:
        if post["id"] == post_id:
            return post


def find_post_index(post_id):
    for index, post in enumerate(my_posts):
        if post["id"] == post_id:
            return index


@app.get("/posts", response_model=List[Post])
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return posts


@app.get("/posts/{post_id}")
def get_post(post_id: int):

    cursor.execute("""SELECT * FROM posts WHERE id = %s""", str(post_id))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {post_id} was not found")
    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):

    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
        (post.title, post.content, post.published)
    )
    new_post = cursor.fetchone()
    conn.commit()

    return new_post


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):

    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", str(post_id))
    post = cursor.fetchone()
    conn.commit()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {post_id} was not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(post_id)))
    post = cursor.fetchone()
    conn.commit()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {post_id} was not found")

    return post



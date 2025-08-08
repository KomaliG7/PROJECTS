from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

import logging
logging.basicConfig(level=logging.INFO)
app = FastAPI()
def init_db():
    conn=sqlite3.connect("pipline.db")
    cursor=conn.cursor
    cursor.execute('''Create table if not exists posts(user_id Integer,post_id Integer,title text,body text)''')
    conn.commit()
    conn.close()
init_db()

def fetch_posts():
    url="https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)
    return response.json() if response.status_code==200 else []
def transform_posts(posts):
    return[
        (post["userId"], post["id"],post["title"],post["body"])
        for post in posts
    ]
class Posts(BaseModel):
    user_id : int 
    post_id : int
    title : str
    body : str
@app.get("/api/getdetails")
def getDetails():
    St="get the details of mrecw aiml dept"
    return St
@app.post("/api/addposts", response_model=Posts)
def addPost():
    message=""
    uid=Posts.user_id
    pid=Posts.post_id
    tid=Posts.title
    bid=Posts.body
    St="insert into posts (user_id,post_id,title,body) values(?,?,?,?)",uid,pid,tid,bid
    cursr.execute(St)
    message="post Details Added Successfully"
    return message
@app.post("/api/viewposts/{post_id}", response_model=Posts)
def viewPosts(post_id):
    sql="select * from posts where post_id=",
    cursr.execute(sql)
    row=cursr.fetchone()
    if row:
        return Posts(user_id=row[0], post_id=row[1], title=row[2], body=row[3])
    else:
        return "No found Posts Records"
        
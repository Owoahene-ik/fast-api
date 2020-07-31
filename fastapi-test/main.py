from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import psycopg2

from pydantic import BaseModel

app = FastAPI()


conn = psycopg2.connect(database="Flask", user = "postgres", password = "1234", host = "127.0.0.1", port = "5432")

if conn:
    print('connection successful')
else:
    print('connection unsuccessful')
    

app = FastAPI(title="REST API using FastAPI POSTGRESQL Async EndPoints by Derrick")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}

class User(BaseModel):
    first_name : str
    last_name : str
    age : int
    country : str
    email : str

class delt(BaseModel):
    email : str



@app.get("/")
def student():
    cur = conn.cursor()
    cur.execute("select GET_FULLNAME('UNIONADMIN')")
    data = cur.fetchall()
    return{"responseCode":  "00", "message": "Students fetched successfully", "data": data}


@app.post("/user")
async def create(name :User ):
    cur = conn.cursor()   
    varg = "INSERT INTO STUDENTS (first_name,last_name, age, country, email) VALUES (%s, %s, %s, %s,%s)"
    cur.execute(varg, (name.first_name,name.last_name, name.age, name.country, name.email))
    conn.commit()
    return{"responseCode":  "00", "message": "Students fetched successfully", "data": name}



@app.put("/update_stud/{email_id}")
async def update(email_id:str, email : User):
    cur = conn.cursor()
    thun = "SELECT email FROM STUDENTS where email = %s"
    cur.execute(thun,(email_id,))
    tes = cur.fetchone()
    # return email.email
    if tes[0] == email.email:
        guess ="UPDATE STUDENTS SET first_name = %s, last_name = %s,age = %s, country = %s, email = %s where email = %s"
        cur.execute(guess, (email.first_name,email.last_name, email.age,email.country,email.email,(email_id,) ))
        conn.commit()
        return{"responseCode":  "00", "message": "Students fetched successfully", "data": email}
    else:
        return{"responseCode":  "404", "message": "Students fetched successfully", "data": None}
    

@app.delete("/del_student/{email_no}")
async def delete_f(email_no : str, email :delt):
    cur = conn.cursor()
    thun = "SELECT email FROM STUDENTS where email = %s"
    cur.execute(thun,(email_no,))
    tes = cur.fetchone()
    # return email.email
    if tes[0] == email.email:
        guess ="delete from students where email = %s"
        cur.execute(guess,(email_no,) )
        conn.commit()
        return{"responseCode":  "00", "message": "Students fetched successfully", "data": email}
    else:
        return{"responseCode":  "404", "message": "Students fetched successfully", "data": None}
    

        
    
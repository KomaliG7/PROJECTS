import os
import sqlite3
import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import io

app = FastAPI()
DB_PATH = "students.db"
os.makedirs("uploaded_files", exist_ok=True)  # Ensure upload folder exists

# ✅ Data Models
class RegisterRequest(BaseModel):
    user_id: str
    user_name: str
    password: str
    preferences: str

class LoginRequest(BaseModel):
    user_id: str
    password: str

# ✅ Register Endpoint
@app.post("/register")
def register_user(data: RegisterRequest):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            user_name TEXT,
            password TEXT,
            preferences TEXT
        )
    """)

    try:
        cursor.execute("""
            INSERT INTO users (user_id, user_name, password, preferences)
            VALUES (?, ?, ?, ?)
        """, (data.user_id, data.user_name, data.password, data.preferences))
        conn.commit()
        return {"message": f"User '{data.user_id}' registered successfully!"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="User ID already exists")
    finally:
        conn.close()

# ✅ Login Endpoint
@app.post("/login")
def login_user(data: LoginRequest):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ? AND password = ?", (data.user_id, data.password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return {"message": f"Welcome back, {user[1]}!"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# ✅ CSV Upload (stores CSV file locally and inserts into DB)
@app.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        filepath = f"uploaded_files/{file.filename}"
        with open(filepath, "wb") as f:
            f.write(contents)

        df = pd.read_csv(io.BytesIO(contents))
        table_name = file.filename.replace(".csv", "").replace(" ", "_").lower()
        conn = sqlite3.connect(DB_PATH)
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        conn.close()

        return {"message": f"File '{file.filename}' uploaded and saved as table '{table_name}'"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Enhanced View Data Endpoint
@app.get("/search_table/{table_name}")
def search_table(table_name: str, query: str = "", columns: str = ""):
    try:
        filepath = f"uploaded_files/{table_name}.csv"
        df = pd.read_csv(filepath)

        if query:
            df = df.query(query)

        if columns:
            selected_cols = [col.strip() for col in columns.split(",")]
            df = df[selected_cols]

        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
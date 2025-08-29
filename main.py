from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI()

def get_db_connection():
    conn = sqlite3.connect("simple_fitness.db")
    conn.row_factory = sqlite3.Row  
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            height REAL NOT NULL,
            weight REAL NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            activity TEXT NOT NULL,
            duration INTEGER NOT NULL,
            calories INTEGER NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS steps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            steps INTEGER NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    
    conn.commit()
    conn.close()

init_db()



@app.get("/users")
def get_users():
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return {"users": [dict(user) for user in users]}

@app.post("/users")
def add_user(name: str, age: int, height: float, weight: float):
    conn = get_db_connection()
    conn.execute("INSERT INTO users (name, age, height, weight) VALUES (?, ?, ?, ?)",
                 (name, age, height, weight))
    conn.commit()
    conn.close()
    return {"message": f"User {name} added successfully!"}


@app.get("/workouts/{user_id}")
def get_workouts(user_id: int):
    conn = get_db_connection()
    workouts = conn.execute("SELECT * FROM workouts WHERE user_id = ?", (user_id,)).fetchall()
    conn.close()
    if not workouts:
        raise HTTPException(status_code=404, detail="No workouts found")
    return {"workouts": [dict(workout) for workout in workouts]}

@app.post("/workouts")
def add_workout(user_id: int, activity: str, duration: int, calories: int, date: str):
    conn = get_db_connection()
    conn.execute("INSERT INTO workouts (user_id, activity, duration, calories, date) VALUES (?, ?, ?, ?, ?)",
                 (user_id, activity, duration, calories, date))
    conn.commit()
    conn.close()
    return {"message": "Workout added successfully!"}


@app.get("/steps/{user_id}")
def get_steps(user_id: int):
    conn = get_db_connection()
    steps = conn.execute("SELECT * FROM steps WHERE user_id = ?", (user_id,)).fetchall()
    conn.close()
    if not steps:
        raise HTTPException(status_code=404, detail="No steps found")
    return {"steps": [dict(step) for step in steps]}

@app.post("/steps")
def add_steps(user_id: int, steps: int, date: str):
    conn = get_db_connection()
    conn.execute("INSERT INTO steps (user_id, steps, date) VALUES (?, ?, ?)",
                 (user_id, steps, date))
    conn.commit()
    conn.close()
    return {"message": "Steps added successfully!"}

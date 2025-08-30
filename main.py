from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI()

# ------------------ Database ------------------

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
    return {"users": [dict(u) for u in users]}

@app.post("/users") 
def add_user(name: str, age: int, height: float, weight: float):
    conn = get_db_connection()
    conn.execute("INSERT INTO users (name, age, height, weight) VALUES (?, ?, ?, ?)",
                 (name, age, height, weight))
    conn.commit()
    conn.close()
    return {"message": f"User '{name}' added successfully."}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(user)

@app.put("/users/{user_id}")
def update_user(user_id: int, name: str = None, age: int = None, height: float = None, weight: float = None):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")

    name = name if name is not None else user["name"]
    age = age if age is not None else user["age"]
    height = height if height is not None else user["height"]
    weight = weight if weight is not None else user["weight"]

    conn.execute("""
        UPDATE users SET name = ?, age = ?, height = ?, weight = ? WHERE id = ?
    """, (name, age, height, weight, user_id))
    conn.commit()
    conn.close()
    return {"message": "User updated successfully."}

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    conn = get_db_connection()
    result = conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully."}


@app.get("/workouts/{user_id}")
def get_workouts(user_id: int):
    conn = get_db_connection()
    workouts = conn.execute("SELECT * FROM workouts WHERE user_id = ?", (user_id,)).fetchall()
    conn.close()
    if not workouts:
        raise HTTPException(status_code=404, detail="No workouts found")
    return {"workouts": [dict(w) for w in workouts]}

@app.post("/workouts")
def add_workout(user_id: int, activity: str, duration: int, calories: int, date: str):
    conn = get_db_connection()
    conn.execute("""
        INSERT INTO workouts (user_id, activity, duration, calories, date)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, activity, duration, calories, date))
    conn.commit()
    conn.close()
    return {"message": "Workout added successfully."}

@app.put("/workouts/{workout_id}")
def update_workout(workout_id: int, activity: str = None, duration: int = None, calories: int = None, date: str = None):
    conn = get_db_connection()
    workout = conn.execute("SELECT * FROM workouts WHERE id = ?", (workout_id,)).fetchone()
    if not workout:
        conn.close()
        raise HTTPException(status_code=404, detail="Workout not found")

    activity = activity if activity is not None else workout["activity"]
    duration = duration if duration is not None else workout["duration"]
    calories = calories if calories is not None else workout["calories"]
    date = date if date is not None else workout["date"]

    conn.execute("""
        UPDATE workouts SET activity = ?, duration = ?, calories = ?, date = ? WHERE id = ?
    """, (activity, duration, calories, date, workout_id))
    conn.commit()
    conn.close()
    return {"message": "Workout updated successfully."}

@app.delete("/workouts/{workout_id}")
def delete_workout(workout_id: int):
    conn = get_db_connection()
    result = conn.execute("DELETE FROM workouts WHERE id = ?", (workout_id,))
    conn.commit()
    conn.close()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Workout not found")
    return {"message": "Workout deleted successfully."}


@app.get("/steps/{user_id}")
def get_steps(user_id: int):
    conn = get_db_connection()
    steps = conn.execute("SELECT * FROM steps WHERE user_id = ?", (user_id,)).fetchall()
    conn.close()
    if not steps:
        raise HTTPException(status_code=404, detail="No steps found")
    return {"steps": [dict(s) for s in steps]}

@app.post("/steps")
def add_steps(user_id: int, steps: int, date: str):
    conn = get_db_connection()
    conn.execute("INSERT INTO steps (user_id, steps, date) VALUES (?, ?, ?)",
                 (user_id, steps, date))
    conn.commit()
    conn.close()
    return {"message": "Steps added successfully."}

@app.put("/steps/{step_id}")
def update_steps(step_id: int, steps: int = None, date: str = None):
    conn = get_db_connection()
    current = conn.execute("SELECT * FROM steps WHERE id = ?", (step_id,)).fetchone()
    if not current:
        conn.close()
        raise HTTPException(status_code=404, detail="Steps record not found")

    steps = steps if steps is not None else current["steps"]
    date = date if date is not None else current["date"]

    conn.execute("UPDATE steps SET steps = ?, date = ? WHERE id = ?",
                 (steps, date, step_id))
    conn.commit()
    conn.close()
    return {"message": "Steps updated successfully."}

@app.delete("/steps/{step_id}")
def delete_steps(step_id: int):
    conn = get_db_connection()
    result = conn.execute("DELETE FROM steps WHERE id = ?", (step_id,))
    conn.commit()
    conn.close()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Steps record not found")
    return {"message": "Steps record deleted successfully."}


<div align="center">
  <h1 style="font-size: 3em;">💪 Simple Fitness Tracker API</h1>
  <p>A simple and efficient RESTful API for tracking users, workouts, and daily steps, built with Python and FastAPI.</p>
  <p>
    <img src="https://img.shields.io/badge/Python-3.8%2B-blue.svg?logo=python&logoColor=white" alt="Python 3.8+">
    <img src="https://img.shields.io/badge/FastAPI-005571.svg?logo=fastapi&logoColor=white" alt="FastAPI">
    <img src="https://img.shields.io/badge/SQLite-003B57.svg?logo=sqlite&logoColor=white" alt="SQLite">
    <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT">
  </p>
</div>

---

### ✨ Features

- **Fitness Tracking:** Create users and log their workouts and daily step counts.
- **High-Performance Framework:** Built using the modern, fast, and robust **FastAPI**.
- **Lightweight Database:** Data is stored persistently in a simple, file-based **SQLite** database.
- **Automatic Validation:** FastAPI handles incoming data validation to ensure type correctness.
- **Clear Error Handling:** Provides user-friendly error messages with appropriate HTTP status codes (e.g., `404 Not Found`).
- **Automatic Interactive Docs:** Get started instantly with auto-generated API documentation via Swagger UI and ReDoc.

---

### 🛠️ Technology Stack

- **Python 3.8+**: The core programming language.
- **FastAPI**: The web framework used to build the API.
- **Uvicorn**: An ultra-fast ASGI server for running the application.
- **SQLite**: The serverless, self-contained SQL database engine.

---

### 🚀 Getting Started

Follow these simple steps to get the API up and running on your local machine.

#### Prerequisites

- Ensure you have **Python 3.8+** installed on your system.
- The **SQLite3** command-line tool (usually included with Python).

#### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
    cd YOUR_REPOSITORY_NAME
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    # On macOS and Linux
    python3 -m venv venv
    source venv/bin/activate

    # On Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required packages:**
    The `requirements.txt` file contains all the necessary dependencies.
    ```bash
    pip install -r requirements.txt
    ```
    
4. **Initialize the database:**
   Run the `sqlite3` command to create the database file and then paste the SQL schema to create the tables.
   ```bash
   sqlite3 simple_fitness.db


Now, paste this entire block into the SQLite prompt and press Enter:

```sql
 CREATE TABLE users (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     name TEXT NOT NULL,
     age INTEGER NOT NULL,
     height REAL NOT NULL,
     weight REAL NOT NULL
 );

 CREATE TABLE workouts (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     user_id INTEGER NOT NULL,
     activity TEXT NOT NULL,
     duration INTEGER NOT NULL,
     calories INTEGER NOT NULL,
     date TEXT NOT NULL,
     FOREIGN KEY (user_id) REFERENCES users (id)
 );

 CREATE TABLE steps (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     user_id INTEGER NOT NULL,
     steps INTEGER NOT NULL,
     date TEXT NOT NULL,
     FOREIGN KEY (user_id) REFERENCES users (id)
 );
```

Finally, exit SQLite by typing `.quit`.

5.  **Run the API server:**
    ```bash
    uvicorn main:app --reload
    ```
    The `--reload` flag enables automatic server restarts on code changes. The API will now be live at `http://127.0.0.1:8000`.

-----

### 📖 API Documentation

This API provides a complete set of endpoints to manage your fitness data. For a rich, interactive experience, navigate to the auto-generated documentation pages:

  - **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
  - **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

#### Endpoint Details

| Endpoint                  | Method | Description                                    | Notes                                        |
| ------------------------- | :----: | ---------------------------------------------- | -------------------------------------------- |
| `/users`                  | `GET`  | Retrieves a list of all users.                 |                                              |
| `/users`                  | `POST` | Adds a new user profile.                       | Requires `name`, `age`, `height`, `weight`.  |
| `/workouts/{user_id}`     | `GET`  | Retrieves all workouts for a specific user.    | Returns `404` if no workouts are found.      |
| `/workouts`               | `POST` | Adds a new workout session for a user.         | Requires `user_id`, `activity`, `duration`, etc. |
| `/steps/{user_id}`        | `GET`  | Retrieves all step records for a specific user.| Returns `404` if no steps are found.         |
| `/steps`                  | `POST` | Adds a new daily step count for a user.        | Requires `user_id`, `steps`, `date`.         |

-----

### 📂 Project Structure

```
.
├── main.py               # The main FastAPI application code
├── requirements.txt      # Python package dependencies
├── simple_fitness.db     # The SQLite database file
└── README.md             # This documentation file
```

```
```

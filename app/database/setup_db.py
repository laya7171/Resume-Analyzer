import sqlite3
import os

os.makedirs("data", exist_ok=True)
conn = sqlite3.connect("data/resume_project.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    role            TEXT NOT NULL,
    requirements    TEXT NOT NULL,
    responsibility  TEXT NOT NULL,
    type            TEXT NOT NULL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")


conn.commit()
conn.close()
print("Databse setup completed successfullyp")

import json
import sqlite3

json_file = "questions.json"

db_file = "questions.db"

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        level TEXT NOT NULL,
        question TEXT NOT NULL,
        answers TEXT NOT NULL,
        correct INTEGER NOT NULL,
        solved INTEGER DEFAULT 0
    )
""")

try:
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    print("✅ JSON-файл загружен!")
except Exception as e:
    print(f"❌ Ошибка чтения JSON-файла: {e}")
    exit()

for level, questions in data.items():
    for question in questions:
        cursor.execute("""
            INSERT INTO quiz_questions (level, question, answers, correct, solved) 
            VALUES (?, ?, ?, ?, ?)
        """, (level, question["question"], json.dumps(question["answers"]), question["correct"], 0))

conn.commit()
conn.close()

print("✅ Данные успешно сохранены в SQLite!")

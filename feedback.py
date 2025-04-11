import json
import sqlite3

json_file = "feedback.json"

db_file = "questions.db"

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY,
            count INTEGER NOT NULL
        )
    """)

try:
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    print("✅ JSON-файл загружен!")
except Exception as e:
    print(f"❌ Ошибка чтения JSON-файла: {e}")
    exit()

for el in data:
    id = el.get("id", 0)
    count = el.get("count", 0)

    cursor.execute("""INSERT INTO feedback (id, count) VALUES (?, ?)""", (id, count))

conn.commit()
conn.close()

print("✅ Данные успешно сохранены в SQLite!")

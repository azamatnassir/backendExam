import json
import sqlite3

json_file = "teams.json"

db_file = "questions.db"

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        total INTEGER NOT NULL,
        ironMan INTEGER NOT NULL,
        spiderMan INTEGER NOT NULL,
        drStrange INTEGER NOT NULL
    )      
""")

try:
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    print("✅ JSON-файл загружен!")
except Exception as e:
    print(f"❌ Ошибка чтения JSON-файла: {e}")
    exit()

for group in data:
    name = group.get("name", "Unknown Group")
    ironMan = group.get("ironMan", 0)
    spiderMan = group.get("spiderMan", 0)
    drStrange = group.get("drStrange", 0)
    total = ironMan + spiderMan + drStrange

    cursor.execute("""
        INSERT INTO groups (name, total, ironMan, spiderMan, drStrange) 
        VALUES (?, ?, ?, ?, ?)
    """, (name, total, ironMan, spiderMan, drStrange))

conn.commit()
conn.close()

print("✅ Данные успешно сохранены в SQLite!")

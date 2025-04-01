from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3, json

app = Flask(__name__, static_folder="public", static_url_path="/")
CORS(app)

def init_db():
    conn = sqlite3.connect("questions.db")
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
    conn.commit()
    conn.close()

init_db()

@app.route("/update-question", methods=["POST"])
def update_question():
    data = request.json  
    question_id = data.get("id")

    if question_id is None:
        return jsonify({"success": False, "error": "Нет ID"}), 400

    try:
        conn = sqlite3.connect("questions.db")
        cursor = conn.cursor()
        
        cursor.execute("UPDATE quiz_questions SET solved = 1 WHERE id = ?", (question_id,))
        conn.commit()
        conn.close()

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    

@app.route("/get-questions", methods=["GET"])
def get_questions():
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quiz_questions")
    rows = cursor.fetchall()
    conn.close()

    data = {}
    for id_, level, question, answers, correct, solved in rows:
        if level not in data:
            data[level] = []
        data[level].append({
            "id": id_,
            "question": question,
            "answers": json.loads(answers),
            "correct": correct,
            "solved": solved
        })

    return jsonify(data)

@app.route("/get_groups")
def get_groups():
    conn = sqlite3.connect("questions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM groups")
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    conn.close()

    groups = [dict(zip(columns, row)) for row in rows]
    return jsonify(groups)

@app.route("/")
def home():
    return app.send_static_file("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)

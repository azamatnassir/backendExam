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

        cursor.execute("UPDATE quiz_questions SET solved = 1 WHERE id = ?",
                       (question_id, ))
        conn.commit()
        conn.close()

        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/update-group", methods=["POST"])
def update_group():
    data = request.json
    group_name = data.get("name")
    level_name = data.get("level")

    if level_name is None:
        return jsonify({"success": False, "error": "Нет level_name"}), 400

    if group_name is None:
        return jsonify({"success": False, "error": "Нет group_name"}), 400

    if level_name == "level1":
        query = "UPDATE groups SET ironMan = ironMan + 1, total = total + 1 WHERE name = ?"
    elif level_name == "level2":
        query = "UPDATE groups SET spiderMan = spiderMan + 2, total = total + 2 WHERE name = ?"
    else:
        query = "UPDATE groups SET drStrange = drStrange + 3, total = total + 3 WHERE name = ?"

    try:
        conn = sqlite3.connect("questions.db")
        cursor = conn.cursor()

        cursor.execute(query, (group_name, ))
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


@app.route("/leaderboard")
def leaderboard():
    return app.send_static_file("leaderboard.html")


@app.route("/")
def home():
    return app.send_static_file("index.html")


if __name__ == "__main__":
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=8080)
    app.run(debug=True, port=5000)

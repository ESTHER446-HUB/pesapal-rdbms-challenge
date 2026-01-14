from flask import Flask, render_template, request, redirect, url_for, jsonify
from rdbms import Database, SQLParser, Column
import os

app = Flask(__name__)

DB_FILE = 'webapp.db'

if os.path.exists(DB_FILE):
    db = Database.load(DB_FILE)
else:
    db = Database("webapp")
    parser = SQLParser(db)
    parser.parse_and_execute("""
        CREATE TABLE users (
            id INT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE
        )
    """)
    parser.parse_and_execute("""
        CREATE TABLE tasks (
            id INT PRIMARY KEY,
            user_id INT NOT NULL,
            title VARCHAR(200) NOT NULL,
            completed BOOLEAN
        )
    """)
    db.save(DB_FILE)

parser = SQLParser(db)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users', methods=['GET'])
def get_users():
    result = parser.parse_and_execute("SELECT * FROM users")
    return jsonify(result)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    try:
        parser.parse_and_execute(
            f"INSERT INTO users (id, name, email) VALUES ({data['id']}, '{data['name']}', '{data['email']}')"
        )
        db.save(DB_FILE)
        return jsonify({"message": "User created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    try:
        parser.parse_and_execute(
            f"UPDATE users SET name='{data['name']}', email='{data['email']}' WHERE id={user_id}"
        )
        db.save(DB_FILE)
        return jsonify({"message": "User updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        parser.parse_and_execute(f"DELETE FROM tasks WHERE user_id={user_id}")
        parser.parse_and_execute(f"DELETE FROM users WHERE id={user_id}")
        db.save(DB_FILE)
        return jsonify({"message": "User deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/tasks', methods=['GET'])
def get_tasks():
    user_id = request.args.get('user_id')
    if user_id:
        result = parser.parse_and_execute(f"SELECT * FROM tasks WHERE user_id={user_id}")
    else:
        result = parser.parse_and_execute("SELECT * FROM tasks")
    return jsonify(result)

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    try:
        completed = 'true' if data.get('completed', False) else 'false'
        parser.parse_and_execute(
            f"INSERT INTO tasks (id, user_id, title, completed) VALUES ({data['id']}, {data['user_id']}, '{data['title']}', {completed})"
        )
        db.save(DB_FILE)
        return jsonify({"message": "Task created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    try:
        completed = 'true' if data.get('completed', False) else 'false'
        parser.parse_and_execute(
            f"UPDATE tasks SET title='{data['title']}', completed={completed} WHERE id={task_id}"
        )
        db.save(DB_FILE)
        return jsonify({"message": "Task updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        parser.parse_and_execute(f"DELETE FROM tasks WHERE id={task_id}")
        db.save(DB_FILE)
        return jsonify({"message": "Task deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/users-with-tasks', methods=['GET'])
def get_users_with_tasks():
    result = parser.parse_and_execute(
        "SELECT users.id, users.name, tasks.title FROM users JOIN tasks ON users.id=tasks.user_id"
    )
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

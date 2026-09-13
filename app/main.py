from flask import Flask, jsonify, request

app = Flask(__name__)

todos = [
    {
        "id": 1,
        "title": "Learn CI/CD",
        "done": False
    },
    {
        "id": 2,
        "title": "Practice Jenkins",
        "done": False
    }
]


@app.get("/health")
def health():
    return jsonify({
        "status": "ok"
    })


@app.get("/todos")
def get_todos():
    return jsonify(todos)


@app.get("/todos/<int:todo_id>")
def get_todo(todo_id):
    todo = next(
        (todo for todo in todos if todo["id"] == todo_id),
        None
    )

    if todo is None:
        return jsonify({
            "error": "Todo not found"
        }), 404

    return jsonify(todo)


@app.post("/todos")
def create_todo():
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({
            "error": "title is required"
        }), 400

    new_id = max([todo["id"] for todo in todos], default=0) + 1

    todo = {
        "id": new_id,
        "title": data["title"],
        "done": False
    }

    todos.append(todo)

    return jsonify(todo), 201


@app.put("/todos/<int:todo_id>")
def update_todo(todo_id):
    todo = next(
        (todo for todo in todos if todo["id"] == todo_id),
        None
    )

    if todo is None:
        return jsonify({
            "error": "Todo not found"
        }), 404

    data = request.get_json()

    if "title" in data:
        todo["title"] = data["title"]

    if "done" in data:
        todo["done"] = data["done"]

    return jsonify(todo)


@app.delete("/todos/<int:todo_id>")
def delete_todo(todo_id):
    global todos

    todo = next(
        (todo for todo in todos if todo["id"] == todo_id),
        None
    )

    if todo is None:
        return jsonify({
            "error": "Todo not found"
        }), 404

    todos = [
        todo for todo in todos
        if todo["id"] != todo_id
    ]

    return jsonify({
        "message": "Todo deleted"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )

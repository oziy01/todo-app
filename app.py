from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# File to store tasks
TASKS_FILE = "tasks.json"

def load_tasks():
    """Load tasks from the JSON file."""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    """Save tasks to the JSON file."""
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f)

@app.route("/")
def index():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    task_text = request.form.get("task", "").strip()
    if task_text:
        tasks = load_tasks()
        tasks.append({"id": len(tasks) + 1, "text": task_text, "done": False})
        save_tasks(tasks)
    return redirect(url_for("index"))

@app.route("/complete/<int:task_id>")
def complete(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]  # Toggle done/undone
            break
    save_tasks(tasks)
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

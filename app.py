from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Store tasks in memory
tasks = []
next_id = 1

@app.route("/")
def index():
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    global next_id
    task_text = request.form.get("task", "").strip()
    if task_text:
        tasks.append({"id": next_id, "text": task_text, "done": False})
        next_id += 1
    return redirect(url_for("index"))

@app.route("/complete/<int:task_id>")
def complete(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            break
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

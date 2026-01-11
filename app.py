from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from manager import TableManager
import os

app = FastAPI()
db = TableManager()

# Simple HTML templates
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>PesaDB Dashboard</title>
    <style>
        body { font-family: sans-serif; margin: 40px; }
        table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2 f2 f2; }
        form { margin-bottom: 20px; padding: 15px; border: 1px solid #eee; }
        .container { display: flex; gap: 40px; }
        .section { flex: 1; }
    </style>
</head>
<body>
    <h1>PesaDB Dashboard</h1>
    
    <div class="container">
        <div class="section">
            <h2>Students</h2>
            <table>
                <tr><th>ID</th><th>Grade</th></tr>
                {% for row in students %}
                <tr><td>{{ row.id }}</td><td>{{ row.grade }}</td></tr>
                {% endfor %}
            </table>
            
            <h3>Add Student</h3>
            <form action="/add_student" method="post">
                ID: <input type="number" name="id" required>
                Grade: <input type="number" name="grade" required>
                <button type="submit">Add</button>
            </form>
        </div>

        <div class="section">
            <h2>Courses</h2>
            <table>
                <tr><th>ID</th><th>Course Name</th></tr>
                {% for row in courses %}
                <tr><td>{{ row.id }}</td><td>{{ row.course_name }}</td></tr>
                {% endfor %}
            </table>

            <h3>Add Course</h3>
            <form action="/add_course" method="post">
                ID: <input type="number" name="id" required>
                Name: <input type="text" name="course_name" required>
                <button type="submit">Add</button>
            </form>
        </div>
    </div>

    <h2>Joined Data (Students & Courses)</h2>
    <table>
        <tr><th>ID</th><th>Grade</th><th>Course Name</th></tr>
        {% for row in joined %}
        <tr><td>{{ row.id }}</td><td>{{ row.grade }}</td><td>{{ row.course_name }}</td></tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def index():
    students = db.execute("SELECT * FROM students")
    courses = db.execute("SELECT * FROM courses")
    joined = db.execute("SELECT * FROM students JOIN courses")
    
    # Simple manual template rendering
    from jinja2 import Template
    template = Template(HTML_TEMPLATE)
    return template.render(students=students, courses=courses, joined=joined)

@app.post("/add_student")
async def add_student(id: int = Form(...), grade: int = Form(...)):
    db.execute(f"INSERT INTO students VALUES ({id}, {grade})")
    return RedirectResponse(url="/", status_code=303)

@app.post("/add_course")
async def add_course(id: int = Form(...), course_name: str = Form(...)):
    db.execute(f"INSERT INTO courses VALUES ({id}, '{course_name}')")
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

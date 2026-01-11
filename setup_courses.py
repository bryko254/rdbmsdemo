from manager import TableManager

db = TableManager()
# Create the courses table with initial schema
db.save_table("courses", {"id": "int", "course_name": "string"}, [])
print("Created 'courses' table.")

from manager import TableManager
import json

def test_join():
    db = TableManager()

    print("\n--- Current Students ---")
    print(json.dumps(db.execute("SELECT * FROM students"), indent=4))

    print("\n--- Inserting into Courses ---")
    # Inserting courses for IDs that exist in students
    print(db.execute("INSERT INTO courses VALUES (1, 'Computer Science')"))
    print(db.execute("INSERT INTO courses VALUES (2, 'Mathematics')"))
    print(db.execute("INSERT INTO courses VALUES (3, 'Physics')"))

    print("\n--- Current Courses ---")
    print(json.dumps(db.execute("SELECT * FROM courses"), indent=4))

    print("\n--- Testing JOIN: SELECT * FROM students JOIN courses ---")
    result = db.execute("SELECT * FROM students JOIN courses")
    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    test_join()

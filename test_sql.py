from manager import TableManager
import json

def test_sql_parser():
    db = TableManager()

    print("\n--- Testing SELECT * FROM students ---")
    result = db.execute("SELECT * FROM students")
    print(json.dumps(result, indent=4))

    print("\n--- Testing INSERT INTO students VALUES (3, 95) ---")
    result = db.execute("INSERT INTO students VALUES (3, 95)")
    print(result)

    print("\n--- Testing SELECT * FROM students (after insert) ---")
    result = db.execute("SELECT * FROM students")
    print(json.dumps(result, indent=4))

    print("\n--- Testing DUPLICATE INSERT (id 1) ---")
    result = db.execute("INSERT INTO students VALUES (1, 100)")
    print(result)

    print("\n--- Testing INVALID SYNTAX ---")
    result = db.execute("DROP TABLE students")
    print(result)

if __name__ == "__main__":
    test_sql_parser()

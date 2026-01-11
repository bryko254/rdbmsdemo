from manager import TableManager

def test():
    db = TableManager()

    print("\n--- Current data in 'students' ---")
    print(db.load_table("students"))

    # Try to insert a DIFFERENT student (ID 2)
    print("\n--- Inserting ID 2 ---")
    db.insert_row("students", {"id": 2, "grade": 90})

    # Try to insert a DUPLICATE student (ID 1) - This should FAIL
    print("\n--- Inserting ID 1 (Duplicate) ---")
    db.insert_row("students", {"id": 1, "grade": 100})

    print("\n--- Final data in 'students' ---")
    print(db.load_table("students"))

if __name__ == "__main__":
    test()

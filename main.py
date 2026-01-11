from manager import TableManager

db = TableManager()

print("--- Welcome to PesaDB v1.0 ---")
print("Type 'exit' to quit.")

while True:
    try:
        user_input = input("pesa_db> ")
        
        if user_input.lower() == "exit":
            break
            
        result = db.execute(user_input)
        print(result)
    except EOFError:
        break
    except Exception as e:
        print(f"Error: {e}")

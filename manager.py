import json
import os
import re

class TableManager:
    def __init__(self, data_directory="data"):
        # Get the absolute path to ensure we are in the right place
        self.data_directory = os.path.abspath(data_directory)
        
        # Create the folder if it doesn't exist
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)

    def _get_path(self, table_name):
        # Create the filename with .json extension
        filename = f"{table_name}.json"
        # Join the folder path and the filename correctly
        return os.path.join(self.data_directory, filename)

    def save_table(self, name, columns, rows):
        file_path = self._get_path(name)
        
        # DEBUG PRINT: This will tell us exactly what is wrong
        print(f"DEBUG: Attempting to write to: {file_path}")
        
        full_storage_object = {
            "table_name": name,
            "columns": columns,
            "rows": rows
        }
        
        # The fix: Ensure we are writing to the file_path, not self.data_directory
        with open(file_path, 'w') as f:
            json.dump(full_storage_object, f, indent=4)
        print(f"Successfully saved table: {name}")

    def load_table(self, name):
        file_path = self._get_path(name)
        if not os.path.exists(file_path):
            return None
        with open(file_path, 'r') as f:
            return json.load(f)

    def insert_row(self, table_name, new_row):
        # 1. Load the existing data
        table = self.load_table(table_name)
        if not table:
            print(f"Error: Table '{table_name}' does not exist. Create it first.")
            return

        # 2. Primary Key Check (Assuming 'id' is the primary key)
        new_id = new_row.get("id")
        for existing_row in table["rows"]:
            if existing_row.get("id") == new_id:
                print(f"Constraint Error: Duplicate Primary Key 'id'={new_id}")
                return # Stop here! Don't save.

        # 3. Add the new data
        table["rows"].append(new_row)

        # 4. Save the updated table back to disk
        self.save_table(table_name, table["columns"], table["rows"])
        print(f"Row inserted successfully into {table_name}")

    def execute(self, query):
        query = query.strip()

        # 1. Match JOIN: SELECT * FROM students JOIN courses
        # Check this BEFORE simple SELECT because the SELECT regex might match the prefix
        join_match = re.match(r"SELECT \* FROM (\w+) JOIN (\w+)", query, re.IGNORECASE)
        if join_match:
            t1_name, t2_name = join_match.groups()
            table1 = self.load_table(t1_name)
            table2 = self.load_table(t2_name)
            
            if not table1 or not table2:
                return "One or both tables not found."

            joined_results = []
            # Simple Nested Loop Join
            for r1 in table1["rows"]:
                for r2 in table2["rows"]:
                    if r1["id"] == r2["id"]: # Joining on ID
                        # Merge the two dictionaries
                        combined = {**r1, **r2}
                        joined_results.append(combined)
            return joined_results

        # 2. Match SELECT: SELECT * FROM table_name
        select_match = re.match(r"SELECT \* FROM (\w+)", query, re.IGNORECASE)
        if select_match:
            table_name = select_match.group(1)
            table = self.load_table(table_name)
            return table["rows"] if table else "Table not found."

        # 3. Match INSERT: INSERT INTO table_name VALUES (id, value)
        # Improved regex to handle both numbers and quoted strings
        insert_match = re.match(r"INSERT INTO (\w+) VALUES \((\d+), (?:'([^']*)'|(\d+))\)", query, re.IGNORECASE)
        if insert_match:
            table_name = insert_match.group(1)
            new_id = int(insert_match.group(2))
            
            # Get the second value (could be a string or a number)
            value = insert_match.group(3) if insert_match.group(3) is not None else int(insert_match.group(4))
            
            # Determine the second column name from the table's schema
            table = self.load_table(table_name)
            if not table:
                return f"Error: Table '{table_name}' does not exist."
            
            # Find the first column that isn't 'id'
            second_col = next((col for col in table["columns"] if col != "id"), "value")
            
            self.insert_row(table_name, {"id": new_id, second_col: value})
            return f"Processed INSERT for {table_name}"

        # 3. Match JOIN: SELECT * FROM students JOIN courses
        join_match = re.match(r"SELECT \* FROM (\w+) JOIN (\w+)", query, re.IGNORECASE)
        if join_match:
            t1_name, t2_name = join_match.groups()
            table1 = self.load_table(t1_name)
            table2 = self.load_table(t2_name)
            
            if not table1 or not table2:
                return "One or both tables not found."

            joined_results = []
            # Simple Nested Loop Join
            for r1 in table1["rows"]:
                for r2 in table2["rows"]:
                    if r1["id"] == r2["id"]: # Joining on ID
                        # Merge the two dictionaries
                        combined = {**r1, **r2}
                        joined_results.append(combined)
            return joined_results

        return "Syntax Error: Command not recognized."

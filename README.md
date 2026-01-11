# PesaDB: A Simple Relational Database Management System (RDBMS)

PesaDB is a lightweight, file-based relational database management system designed for the **Pesapal Junior Developer Challenge '26**. It features a custom SQL-ish parser, data integrity via primary keys, relationship support through JOINs, and a web-based dashboard for CRUD operations.

## Features

- **JSON Storage Engine**: Data is persisted in human-readable JSON files.
- **Data Integrity**: Enforces **Primary Key** constraints to prevent duplicate records.
- **SQL-ish Interface**: Supports a subset of SQL commands for managing data.
- **Relationship Support**: Implements **Inner Joins** to link multiple tables by ID.
- **Interactive REPL**: A command-line interface for direct database interaction.
- **Web Dashboard**: A FastAPI-powered web application for visual data management.

## Project Structure

```text
pesapal_rdbms/
├── data/               # Persistent JSON storage for tables
├── manager.py          # Core RDBMS logic & SQL Parser
├── main.py             # Interactive CLI (REPL)
├── app.py              # FastAPI Web Dashboard
├── requirements.txt    # Project dependencies
└── venv/               # Virtual environment
```

## Setup & Installation

1. **Clone the repository** (or navigate to the project folder).
2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Interactive CLI (REPL)
Run the CLI to execute commands directly against the database:
```bash
python3 main.py
```
**Supported Commands:**
- `SELECT * FROM table_name`
- `INSERT INTO table_name VALUES (id, value)` (Supports numbers and quoted strings like `'Text'`)
- `SELECT * FROM table1 JOIN table2` (Joins on `id`)
- `exit` (To quit)

### 2. Web Dashboard
Start the web server to manage data through a browser:
```bash
python3 app.py
```
Open [http://localhost:8000](http://localhost:8000) in your browser. You can view existing records and add new students or courses through the provided forms.

## Technical Details

- **Integrity**: The `TableManager` validates every `INSERT` by checking the `id` against existing rows in the target table.
- **Joins**: Implements a Nested Loop Join algorithm that merges dictionaries from two tables where the `id` field matches.
- **Parsing**: Uses Python's `re` (Regular Expressions) to interpret and route SQL-like strings to the internal management methods.

## Credits & AI Disclosure
This project was developed by Davis for the Pesapal Junior Dev Challenge. 
- **AI Assistance**: An AI assistant (Gemini/Cursor) was used to help design the project architecture, refine the regex parser, and generate the web dashboard boilerplate. 
- **Libraries**: Built using `FastAPI`, `Uvicorn`, `Jinja2`, and Python's standard libraries.

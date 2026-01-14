# Simple RDBMS - Pesapal Junior Dev Challenge '26

A lightweight relational database management system (RDBMS) built from scratch in Python, featuring SQL-like query support, indexing, and a web application demo.

## Features

### Core RDBMS Capabilities
- **SQL Parser**: Supports CREATE TABLE, INSERT, SELECT, UPDATE, DELETE, DROP TABLE
- **Data Types**: INT, FLOAT, VARCHAR(n), BOOLEAN
- **Constraints**: PRIMARY KEY, UNIQUE, NOT NULL
- **Indexing**: B-tree indexing for primary and unique keys
- **Joins**: INNER JOIN support
- **REPL**: Interactive command-line interface
- **Persistence**: Save/load database to disk using pickle

### Web Application Demo
- Task management system with users and tasks
- Full CRUD operations via REST API
- JOIN query demonstration
- Clean, responsive UI

## Architecture

### Components

1. **Column**: Defines table columns with data types and constraints
2. **BTreeIndex**: Simple B-tree implementation for fast lookups
3. **Table**: Manages rows, enforces constraints, handles CRUD operations
4. **Database**: Container for multiple tables
5. **SQLParser**: Parses and executes SQL-like statements
6. **REPL**: Interactive shell for database operations

### Design Decisions

- **In-memory storage** with disk persistence for simplicity
- **B-tree indexing** on primary/unique keys for O(log n) lookups
- **Row-based storage** suitable for OLTP workloads
- **Regex-based SQL parsing** for lightweight implementation
- **Pickle serialization** for easy persistence

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd PESAPAL

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Interactive REPL

```bash
python rdbms.py
```

Example session:
```sql
rdbms> CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100) UNIQUE)
Table users created

rdbms> INSERT INTO users (id, name, email) VALUES (1, 'John Doe', 'john@example.com')
1 row inserted

rdbms> SELECT * FROM users
1 row(s) returned:
{'id': 1, 'name': 'John Doe', 'email': 'john@example.com'}

rdbms> UPDATE users SET name='Jane Doe' WHERE id=1
1 row(s) updated

rdbms> DELETE FROM users WHERE id=1
1 row(s) deleted

rdbms> .save mydb.db
Database saved to mydb.db

rdbms> .exit
```

### REPL Commands
- `.exit` - Exit the REPL
- `.save <filename>` - Save database to file
- `.load <filename>` - Load database from file
- `.tables` - List all tables

### Web Application

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

The web app demonstrates:
- Creating users with unique emails
- Creating tasks assigned to users
- Updating task completion status
- Deleting users and tasks
- JOIN queries showing users with their tasks

## SQL Syntax

### CREATE TABLE
```sql
CREATE TABLE table_name (
    column1 datatype [PRIMARY KEY] [UNIQUE] [NOT NULL],
    column2 datatype [PRIMARY KEY] [UNIQUE] [NOT NULL]
)
```

### INSERT
```sql
INSERT INTO table_name (col1, col2) VALUES (val1, val2)
```

### SELECT
```sql
SELECT * FROM table_name
SELECT col1, col2 FROM table_name WHERE col1=value
SELECT * FROM table1 JOIN table2 ON table1.col=table2.col
```

### UPDATE
```sql
UPDATE table_name SET col1=val1, col2=val2 WHERE condition
```

### DELETE
```sql
DELETE FROM table_name WHERE condition
```

### DROP TABLE
```sql
DROP TABLE table_name
```

## Testing

Manual testing via REPL:

```bash
python rdbms.py
```

```sql
-- Test table creation
CREATE TABLE products (id INT PRIMARY KEY, name VARCHAR(50), price FLOAT)

-- Test insert
INSERT INTO products (id, name, price) VALUES (1, 'Laptop', 999.99)
INSERT INTO products (id, name, price) VALUES (2, 'Mouse', 29.99)

-- Test select
SELECT * FROM products
SELECT name, price FROM products WHERE price > 50

-- Test update
UPDATE products SET price=899.99 WHERE id=1

-- Test delete
DELETE FROM products WHERE id=2

-- Test constraints (should fail)
INSERT INTO products (id, name, price) VALUES (1, 'Keyboard', 79.99)
```

## Limitations & Future Improvements

### Current Limitations
- Single-threaded (no concurrent access)
- No transaction support (ACID properties)
- Limited WHERE clause parsing (no AND/OR)
- No aggregate functions (COUNT, SUM, AVG)
- No ORDER BY, GROUP BY, LIMIT
- No foreign key constraints
- Simple B-tree (not optimized)

### Potential Improvements
- Multi-threading with locks
- Transaction support with rollback
- Query optimizer
- More SQL features (subqueries, views, stored procedures)
- Better indexing (B+ trees, hash indexes)
- Query caching
- Connection pooling for web app
- Comprehensive test suite

## Project Structure

```
PESAPAL/
├── rdbms.py           # Core RDBMS implementation
├── app.py             # Flask web application
├── templates/
│   └── index.html     # Web UI
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

## Technologies Used

- **Python 3**: Core language
- **Flask**: Web framework
- **Pickle**: Serialization
- **Regex**: SQL parsing

## Acknowledgments

This project was created for the Pesapal Junior Dev Challenge '26. All code is original work implementing standard computer science algorithms and database concepts.

## License

MIT License - Feel free to use this for learning purposes.

## Author

Esther Kuria
https://github.com/ESTHER446-HUB
esther.kuria@student.moringaschool.com

---

**Note**: This is an educational project demonstrating RDBMS concepts. It is not production-ready and should not be used for real applications requiring reliability, security, or performance.

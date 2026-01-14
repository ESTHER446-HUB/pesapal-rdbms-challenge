# Simple RDBMS - Pesapal Junior Dev Challenge '26

A relational database management system built from scratch in Python. This project implements core database features including SQL parsing, indexing, constraints, and persistence, plus a web demo to show it all working.

## What It Does

This is a working database system that lets you:
- Create tables with different data types
- Insert, update, delete, and query data
- Use SQL commands (or something very close to SQL)
- Enforce primary keys and unique constraints
- Join tables together
- Save and load your database from disk
- Interact through a command-line REPL or a web interface

## Features

**Core Database:**
- SQL-like commands: CREATE TABLE, INSERT, SELECT, UPDATE, DELETE, DROP TABLE
- Data types: INT, FLOAT, VARCHAR(n), BOOLEAN
- Constraints: PRIMARY KEY, UNIQUE, NOT NULL
- B-tree indexing for fast lookups on primary/unique keys
- INNER JOIN support
- WHERE clause filtering
- Save/load database to disk

**Web Demo:**
- Simple task manager showing users and tasks
- REST API with full CRUD operations
- Clean web interface
- Live demonstration of JOIN queries

## Quick Start

```bash
# Install Flask
pip install -r requirements.txt

# Run the tests
python3 test_rdbms.py

# Try the interactive shell
python3 rdbms.py

# Or start the web app
python3 app.py
# Then visit http://localhost:5000
```

## Using the REPL

The REPL (Read-Eval-Print Loop) is an interactive shell where you can type SQL commands directly.

Start it with:
```bash
python3 rdbms.py
```

Then try some commands:
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

**Special commands:**
- `.exit` - quit the REPL
- `.save <filename>` - save your database to a file
- `.load <filename>` - load a database from a file
- `.tables` - see all your tables

## Using the Web App

The web app is a simple task manager that demonstrates the database in action.

```bash
python3 app.py
```

Open your browser to `http://localhost:5000` and you can:
- Add users (with unique emails)
- Create tasks assigned to users
- Mark tasks as complete
- Delete users and tasks
- See a JOIN query showing which user has which tasks

## SQL Commands

Here's what SQL you can write:

**Create a table:**
```sql
CREATE TABLE table_name (
    column1 datatype [PRIMARY KEY] [UNIQUE] [NOT NULL],
    column2 datatype [PRIMARY KEY] [UNIQUE] [NOT NULL]
)
```

**Add data:**
```sql
INSERT INTO table_name (col1, col2) VALUES (val1, val2)
```

**Query data:**
```sql
SELECT * FROM table_name
SELECT col1, col2 FROM table_name WHERE col1=value
SELECT * FROM table1 JOIN table2 ON table1.col=table2.col
```

**Update data:**
```sql
UPDATE table_name SET col1=val1, col2=val2 WHERE condition
```

**Delete data:**
```sql
DELETE FROM table_name WHERE condition
```

**Remove a table:**
```sql
DROP TABLE table_name
```

## How I Built It

The database is built in layers:

1. **Storage layer** - Rows are stored in memory as Python dictionaries. Each table keeps a list of rows.

2. **Indexing** - Primary keys and unique columns get automatic B-tree indexes (well, Python dicts that act like B-trees) for fast lookups.

3. **Schema enforcement** - The Column class validates data types and checks constraints before any data gets saved.

4. **SQL parsing** - A regex-based parser breaks down SQL commands and calls the right methods. Not fancy, but it works.

5. **Persistence** - The whole database serializes to disk using pickle. Simple and effective for this use case.

## Testing

I wrote a test suite that covers the main features:

```bash
python3 test_rdbms.py
```

You can also test manually in the REPL:

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

## What's Missing

This is a learning project, so there are some things I didn't implement:

- **No concurrent access** - Only one person can use it at a time
- **No transactions** - No COMMIT/ROLLBACK
- **Simple WHERE clauses** - Can't do AND/OR yet
- **No aggregate functions** - No COUNT, SUM, AVG, etc.
- **No ORDER BY or LIMIT**
- **Only INNER JOIN** - No LEFT/RIGHT/OUTER joins

But hey, it works for what it is!

## What I'd Add Next

If I keep working on this:
- AND/OR in WHERE clauses
- ORDER BY and LIMIT
- Aggregate functions
- Better error messages
- Transaction support
- More join types
- Query optimization

## Project Files

```
PESAPAL/
├── rdbms.py           # The main database engine
├── app.py             # Flask web app
├── test_rdbms.py      # Test suite
├── templates/
│   └── index.html     # Web interface
├── requirements.txt   # Just Flask, really
└── README.md          # You're reading it
```

## Tech Stack

- Python 3 (the whole thing)
- Flask (for the web demo)
- Pickle (for saving to disk)
- Regex (for parsing SQL)
- No external database libraries - that would defeat the point!

## Acknowledgments

This project was created for the Pesapal Junior Dev Challenge '26. All code is original work implementing standard computer science algorithms and database concepts.

## License

MIT License - Feel free to use this for learning purposes.

## Author

Esther Kuria
https://github.com/ESTHER446-HUB
esther.kuria@student.moringaschool.com

---

**Note**: This is an educational project. Don't use it for anything important - it's meant to demonstrate concepts, not to be production-ready.

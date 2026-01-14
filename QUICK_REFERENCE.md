# Quick Reference Guide

## Installation & Setup

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run tests
python3 test_rdbms.py

# Start REPL
python3 rdbms.py

# Start web app
python3 app.py
```

## REPL Commands

| Command | Description |
|---------|-------------|
| `CREATE TABLE ...` | Create a new table |
| `INSERT INTO ...` | Add a row |
| `SELECT ...` | Query data |
| `UPDATE ...` | Modify rows |
| `DELETE FROM ...` | Remove rows |
| `DROP TABLE ...` | Delete table |
| `.save <file>` | Save database |
| `.load <file>` | Load database |
| `.tables` | List tables |
| `.exit` | Quit REPL |

## SQL Syntax Quick Reference

### CREATE TABLE
```sql
CREATE TABLE table_name (
    col1 INT PRIMARY KEY,
    col2 VARCHAR(100) UNIQUE NOT NULL,
    col3 FLOAT,
    col4 BOOLEAN
)
```

### INSERT
```sql
INSERT INTO table_name (col1, col2) VALUES (val1, val2)
```

### SELECT
```sql
SELECT * FROM table_name
SELECT col1, col2 FROM table_name WHERE col1 > 10
SELECT t1.col1, t2.col2 FROM t1 JOIN t2 ON t1.id=t2.id
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

## Data Types

| Type | Description | Example |
|------|-------------|---------|
| `INT` | Integer | `42` |
| `FLOAT` | Decimal | `3.14` |
| `VARCHAR(n)` | String (max n chars) | `'Hello'` |
| `BOOLEAN` | True/False | `true` or `false` |

## Constraints

| Constraint | Description |
|------------|-------------|
| `PRIMARY KEY` | Unique identifier, auto-indexed |
| `UNIQUE` | Unique values, auto-indexed |
| `NOT NULL` | Required value |

## Web API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web UI |
| GET | `/users` | List all users |
| POST | `/users` | Create user |
| PUT | `/users/<id>` | Update user |
| DELETE | `/users/<id>` | Delete user |
| GET | `/tasks` | List all tasks |
| POST | `/tasks` | Create task |
| PUT | `/tasks/<id>` | Update task |
| DELETE | `/tasks/<id>` | Delete task |
| GET | `/users-with-tasks` | JOIN demo |

## File Structure

```
PESAPAL/
├── rdbms.py              # Core RDBMS (400+ lines)
├── app.py                # Web app (150+ lines)
├── test_rdbms.py         # Tests (150+ lines)
├── templates/index.html  # Web UI
├── README.md             # Main documentation
├── ARCHITECTURE.md       # Technical details
├── EXAMPLES.md           # SQL examples
├── DIAGRAMS.md           # Visual diagrams
├── SUBMISSION.md         # Submission checklist
├── PROJECT_SUMMARY.md    # Project overview
├── QUICK_REFERENCE.md    # This file
├── requirements.txt      # Dependencies
├── .gitignore           # Git ignore
└── quickstart.sh        # Setup script
```

## Common Operations

### Create and populate a table
```sql
CREATE TABLE products (id INT PRIMARY KEY, name VARCHAR(100), price FLOAT)
INSERT INTO products (id, name, price) VALUES (1, 'Laptop', 999.99)
INSERT INTO products (id, name, price) VALUES (2, 'Mouse', 29.99)
SELECT * FROM products
```

### Query with filter
```sql
SELECT name, price FROM products WHERE price > 50
```

### Update and delete
```sql
UPDATE products SET price=899.99 WHERE id=1
DELETE FROM products WHERE id=2
```

### Save and load
```
.save mydata.db
.load mydata.db
```

## Testing

```bash
# Run all tests
python3 test_rdbms.py

# Expected output: "All tests passed! ✓"
```

## Troubleshooting

### Import Error
```bash
pip3 install Flask
```

### Permission Denied (quickstart.sh)
```bash
chmod +x quickstart.sh
```

### Port Already in Use (web app)
Edit `app.py` and change port:
```python
app.run(debug=True, port=5001)  # Change 5000 to 5001
```

## Performance Tips

1. Use PRIMARY KEY or UNIQUE on frequently queried columns
2. Save database periodically with `.save`
3. Use specific column names in SELECT instead of `*`
4. Keep WHERE clauses simple (single condition)

## Limitations

- Single-threaded (no concurrent access)
- No transactions
- WHERE clauses: single condition only (no AND/OR)
- JOIN: INNER JOIN only
- No aggregate functions (COUNT, SUM, etc.)
- No ORDER BY, GROUP BY, LIMIT

## Documentation Files

| File | Purpose |
|------|---------|
| README.md | User guide and getting started |
| ARCHITECTURE.md | Technical design details |
| EXAMPLES.md | SQL command examples |
| DIAGRAMS.md | Visual system diagrams |
| SUBMISSION.md | Submission checklist |
| PROJECT_SUMMARY.md | Project overview |
| QUICK_REFERENCE.md | This quick reference |

## Support

For questions or issues:
- Check EXAMPLES.md for SQL syntax
- Check ARCHITECTURE.md for technical details
- Check SUBMISSION.md for submission help

## License

MIT License - Free for educational use

# Example SQL Commands for REPL

## Basic Table Creation and Operations

### Create a simple users table
```sql
CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(100) NOT NULL, email VARCHAR(100) UNIQUE, age INT)
```

### Insert some users
```sql
INSERT INTO users (id, name, email, age) VALUES (1, 'Alice Johnson', 'alice@example.com', 28)
INSERT INTO users (id, name, email, age) VALUES (2, 'Bob Smith', 'bob@example.com', 35)
INSERT INTO users (id, name, email, age) VALUES (3, 'Charlie Brown', 'charlie@example.com', 42)
INSERT INTO users (id, name, email, age) VALUES (4, 'Diana Prince', 'diana@example.com', 30)
```

### Query all users
```sql
SELECT * FROM users
```

### Query specific columns
```sql
SELECT name, email FROM users
```

### Query with WHERE clause
```sql
SELECT name, age FROM users WHERE age > 30
```

### Update a user
```sql
UPDATE users SET age=29 WHERE id=1
```

### Delete a user
```sql
DELETE FROM users WHERE id=4
```

## Advanced: Multiple Tables with JOIN

### Create posts table
```sql
CREATE TABLE posts (id INT PRIMARY KEY, user_id INT NOT NULL, title VARCHAR(200) NOT NULL, views INT)
```

### Insert posts
```sql
INSERT INTO posts (id, user_id, title, views) VALUES (1, 1, 'My First Blog Post', 150)
INSERT INTO posts (id, user_id, title, views) VALUES (2, 1, 'Python Tips and Tricks', 320)
INSERT INTO posts (id, user_id, title, views) VALUES (3, 2, 'Database Design 101', 890)
INSERT INTO posts (id, user_id, title, views) VALUES (4, 3, 'Web Development Guide', 450)
```

### JOIN query
```sql
SELECT users.name, posts.title FROM users JOIN posts ON users.id=posts.user_id
```

### Query posts
```sql
SELECT * FROM posts WHERE views > 300
```

### Update post views
```sql
UPDATE posts SET views=1000 WHERE id=3
```

## E-commerce Example

### Create products table
```sql
CREATE TABLE products (id INT PRIMARY KEY, name VARCHAR(100) NOT NULL, price FLOAT, in_stock BOOLEAN)
```

### Insert products
```sql
INSERT INTO products (id, name, price, in_stock) VALUES (1, 'Laptop', 999.99, true)
INSERT INTO products (id, name, price, in_stock) VALUES (2, 'Mouse', 29.99, true)
INSERT INTO products (id, name, price, in_stock) VALUES (3, 'Keyboard', 79.99, false)
INSERT INTO products (id, name, price, in_stock) VALUES (4, 'Monitor', 299.99, true)
```

### Query available products
```sql
SELECT name, price FROM products WHERE in_stock=true
```

### Update stock status
```sql
UPDATE products SET in_stock=true WHERE id=3
```

## REPL Commands

### Save database
```
.save mydata.db
```

### Load database
```
.load mydata.db
```

### List all tables
```
.tables
```

### Exit REPL
```
.exit
```

## Testing Constraints

### Try to insert duplicate primary key (should fail)
```sql
INSERT INTO users (id, name, email, age) VALUES (1, 'Test User', 'test@example.com', 25)
```
Expected: Error: Duplicate value for id

### Try to insert duplicate unique value (should fail)
```sql
INSERT INTO users (id, name, email, age) VALUES (5, 'Test User', 'alice@example.com', 25)
```
Expected: Error: Duplicate value for email

### Try to insert NULL into NOT NULL column (should fail)
```sql
INSERT INTO users (id, email, age) VALUES (5, 'test@example.com', 25)
```
Expected: Error: Column name cannot be NULL

## Complete Example Session

```
$ python3 rdbms.py
==================================================
Simple RDBMS - Interactive REPL
==================================================
Commands: SQL statements, .exit, .save <file>, .load <file>, .tables

rdbms> CREATE TABLE employees (id INT PRIMARY KEY, name VARCHAR(100), salary FLOAT, department VARCHAR(50))
Table employees created

rdbms> INSERT INTO employees (id, name, salary, department) VALUES (1, 'John Doe', 75000.00, 'Engineering')
1 row inserted

rdbms> INSERT INTO employees (id, name, salary, department) VALUES (2, 'Jane Smith', 85000.00, 'Engineering')
1 row inserted

rdbms> INSERT INTO employees (id, name, salary, department) VALUES (3, 'Bob Johnson', 65000.00, 'Sales')
1 row inserted

rdbms> SELECT * FROM employees
3 row(s) returned:
{'id': 1, 'name': 'John Doe', 'salary': 75000.0, 'department': 'Engineering'}
{'id': 2, 'name': 'Jane Smith', 'salary': 85000.0, 'department': 'Engineering'}
{'id': 3, 'name': 'Bob Johnson', 'salary': 65000.0, 'department': 'Sales'}

rdbms> SELECT name, salary FROM employees WHERE salary > 70000
2 row(s) returned:
{'name': 'John Doe', 'salary': 75000.0}
{'name': 'Jane Smith', 'salary': 85000.0}

rdbms> UPDATE employees SET salary=80000 WHERE id=1
1 row(s) updated

rdbms> .save company.db
Database saved to company.db

rdbms> .tables
Tables: employees

rdbms> .exit
Goodbye!
```

## Tips

1. **SQL is case-insensitive**: `SELECT` and `select` both work
2. **Semicolons are optional**: Both `SELECT * FROM users` and `SELECT * FROM users;` work
3. **String values need quotes**: Use single or double quotes for VARCHAR values
4. **Boolean values**: Use `true`/`false` or `1`/`0`
5. **Save frequently**: Use `.save` to persist your data
6. **Check tables**: Use `.tables` to see what tables exist

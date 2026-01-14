# RDBMS Architecture Documentation

## Overview

This document explains the design and implementation of the Simple RDBMS built for the Pesapal Junior Dev Challenge '26.

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Application Layer                     │
│  ┌──────────────┐              ┌──────────────────────┐ │
│  │  REPL Shell  │              │   Flask Web App      │ │
│  └──────┬───────┘              └──────────┬───────────┘ │
│         │                                  │             │
└─────────┼──────────────────────────────────┼─────────────┘
          │                                  │
┌─────────┴──────────────────────────────────┴─────────────┐
│                    SQL Parser Layer                       │
│  ┌────────────────────────────────────────────────────┐  │
│  │  SQLParser: Regex-based SQL statement parsing     │  │
│  │  - CREATE, INSERT, SELECT, UPDATE, DELETE, DROP   │  │
│  │  - WHERE clause parsing                           │  │
│  │  - JOIN support                                   │  │
│  └────────────────────────────────────────────────────┘  │
└───────────────────────────┬───────────────────────────────┘
                            │
┌───────────────────────────┴───────────────────────────────┐
│                    Database Engine                        │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Database: Container for tables                   │  │
│  │  - Table management                               │  │
│  │  - Persistence (pickle)                           │  │
│  └────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Table: Row storage and operations                │  │
│  │  - CRUD operations                                │  │
│  │  - Constraint enforcement                         │  │
│  │  - Index management                               │  │
│  └────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Column: Schema definition                        │  │
│  │  - Data type validation                           │  │
│  │  - Constraint definitions                         │  │
│  └────────────────────────────────────────────────────┘  │
└───────────────────────────┬───────────────────────────────┘
                            │
┌───────────────────────────┴───────────────────────────────┐
│                    Storage Layer                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │  BTreeIndex: Fast lookups for indexed columns     │  │
│  │  - O(log n) search complexity                     │  │
│  │  - Automatic index maintenance                    │  │
│  └────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────┐  │
│  │  In-Memory Row Storage                            │  │
│  │  - List-based row storage                         │  │
│  │  - Dictionary-based row structure                 │  │
│  └────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Disk Persistence (Pickle)                        │  │
│  │  - Serialize entire database                      │  │
│  │  - Load/Save operations                           │  │
│  └────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Column Class

**Purpose**: Defines table schema with data types and constraints.

**Key Features**:
- Data type validation (INT, FLOAT, VARCHAR, BOOLEAN)
- Constraint support (PRIMARY KEY, UNIQUE, NOT NULL)
- Type coercion and validation

**Implementation Details**:
```python
Column(name, dtype, primary_key, unique, nullable)
```

**Validation Logic**:
- INT: Converts to integer
- FLOAT: Converts to float
- BOOLEAN: Accepts true/false/1/0
- VARCHAR(n): Enforces max length

### 2. BTreeIndex Class

**Purpose**: Provides fast lookups for indexed columns.

**Key Features**:
- Dictionary-based B-tree simulation
- O(log n) average search time
- Automatic maintenance on insert/update/delete

**Structure**:
```python
{
    value1: [row_id1, row_id2, ...],
    value2: [row_id3, ...],
    ...
}
```

**Operations**:
- `insert(key, row_id)`: Add entry to index
- `search(key)`: Find all rows with key
- `delete(key, row_id)`: Remove entry from index

### 3. Table Class

**Purpose**: Manages rows and enforces schema constraints.

**Key Features**:
- Row storage as list of dictionaries
- Automatic index management
- Constraint enforcement
- CRUD operations

**Row Structure**:
```python
{
    '_id': internal_row_id,
    'column1': value1,
    'column2': value2,
    ...
}
```

**Operations**:
- `insert(values)`: Add new row with validation
- `select(columns, where)`: Query rows
- `update(values, where)`: Modify rows
- `delete(where)`: Remove rows

**Constraint Enforcement**:
1. PRIMARY KEY: Checked via index before insert
2. UNIQUE: Checked via index before insert/update
3. NOT NULL: Validated during insert/update

### 4. Database Class

**Purpose**: Container for multiple tables with persistence.

**Key Features**:
- Table registry
- Save/load to disk
- Table lifecycle management

**Operations**:
- `create_table(name, columns)`: Create new table
- `drop_table(name)`: Remove table
- `get_table(name)`: Retrieve table
- `save(filepath)`: Persist to disk
- `load(filepath)`: Load from disk

### 5. SQLParser Class

**Purpose**: Parse and execute SQL-like statements.

**Supported SQL**:
```sql
CREATE TABLE table_name (col1 TYPE [constraints], ...)
INSERT INTO table_name (cols) VALUES (vals)
SELECT cols FROM table WHERE condition
SELECT cols FROM t1 JOIN t2 ON t1.col=t2.col
UPDATE table SET col=val WHERE condition
DELETE FROM table WHERE condition
DROP TABLE table_name
```

**Parsing Strategy**:
- Regex-based pattern matching
- Recursive descent for complex queries
- WHERE clause evaluation via lambda functions

**WHERE Clause Parsing**:
Supports operators: `=`, `!=`, `>`, `<`, `>=`, `<=`

Example:
```sql
WHERE age > 25
```
Becomes:
```python
lambda row: row.get('age') > 25
```

### 6. JOIN Implementation

**Type**: INNER JOIN only

**Algorithm**:
```python
for row1 in table1.rows:
    for row2 in table2.rows:
        if row1[join_col1] == row2[join_col2]:
            yield merged_row
```

**Complexity**: O(n * m) where n, m are table sizes

**Output Format**:
```python
{
    'table1.col1': value1,
    'table1.col2': value2,
    'table2.col1': value3,
    ...
}
```

## Data Flow Examples

### INSERT Operation

```
1. SQL: "INSERT INTO users (id, name) VALUES (1, 'Alice')"
2. SQLParser._insert() parses statement
3. Table.insert() called with {'id': 1, 'name': 'Alice'}
4. Column.validate() validates each value
5. Check PRIMARY KEY/UNIQUE via indexes
6. Add row to table.rows
7. Update indexes for indexed columns
8. Return success
```

### SELECT with WHERE

```
1. SQL: "SELECT name FROM users WHERE age > 25"
2. SQLParser._select() parses statement
3. SQLParser._parse_where() creates lambda function
4. Table.select() iterates rows
5. Apply WHERE lambda to each row
6. Filter columns to requested set
7. Return result list
```

### UPDATE Operation

```
1. SQL: "UPDATE users SET age=30 WHERE id=1"
2. SQLParser._update() parses statement
3. Create updates dict and WHERE lambda
4. Table.update() finds matching rows
5. For each match:
   - Validate new values
   - Update indexes if indexed column
   - Modify row in place
6. Return count of updated rows
```

## Performance Characteristics

### Time Complexity

| Operation | Without Index | With Index |
|-----------|--------------|------------|
| INSERT    | O(n)         | O(log n)   |
| SELECT *  | O(n)         | O(n)       |
| SELECT WHERE indexed | O(n) | O(log n) |
| UPDATE    | O(n)         | O(n)       |
| DELETE    | O(n)         | O(n)       |
| JOIN      | O(n*m)       | O(n*m)     |

### Space Complexity

- Row storage: O(n) where n = number of rows
- Index storage: O(k) where k = number of unique values
- Total: O(n + k)

## Design Decisions

### 1. In-Memory Storage

**Rationale**: Simplicity and speed for small datasets

**Trade-offs**:
- ✓ Fast access
- ✓ Simple implementation
- ✗ Limited by RAM
- ✗ Data loss on crash (mitigated by save/load)

### 2. Pickle for Persistence

**Rationale**: Built-in Python serialization

**Trade-offs**:
- ✓ Easy to implement
- ✓ Preserves Python objects
- ✗ Not human-readable
- ✗ Python-specific format
- ✗ Security concerns (untrusted data)

### 3. Regex-Based SQL Parsing

**Rationale**: Lightweight, no external dependencies

**Trade-offs**:
- ✓ Simple implementation
- ✓ No parser library needed
- ✗ Limited SQL support
- ✗ Error messages less helpful
- ✗ Hard to extend

### 4. Dictionary-Based B-Tree

**Rationale**: Python dict provides O(1) average lookup

**Trade-offs**:
- ✓ Fast lookups
- ✓ Simple implementation
- ✗ Not a true B-tree
- ✗ No range queries
- ✗ Memory overhead

### 5. Row-Based Storage

**Rationale**: Natural for OLTP workloads

**Trade-offs**:
- ✓ Fast row operations
- ✓ Simple to implement
- ✗ Slower for column scans
- ✗ More memory per row

## Limitations

### Current Limitations

1. **Concurrency**: Single-threaded, no concurrent access
2. **Transactions**: No ACID guarantees
3. **SQL Support**: Limited to basic operations
4. **Indexing**: Only on PRIMARY KEY and UNIQUE columns
5. **Joins**: Only INNER JOIN, no optimization
6. **WHERE Clauses**: No AND/OR/NOT operators
7. **Aggregations**: No COUNT, SUM, AVG, etc.
8. **Sorting**: No ORDER BY
9. **Grouping**: No GROUP BY
10. **Subqueries**: Not supported

### Security Considerations

1. **SQL Injection**: Vulnerable (no parameterized queries)
2. **Pickle Deserialization**: Unsafe for untrusted data
3. **Access Control**: No authentication/authorization
4. **Encryption**: No data encryption

## Future Improvements

### Short-term (Easy)

1. Add AND/OR support in WHERE clauses
2. Implement ORDER BY and LIMIT
3. Add aggregate functions (COUNT, SUM, AVG)
4. Better error messages
5. Input validation and sanitization

### Medium-term (Moderate)

1. Write-ahead logging (WAL) for durability
2. B+ tree implementation for range queries
3. Query optimizer
4. LEFT/RIGHT/OUTER JOIN support
5. Subquery support
6. CREATE INDEX statement

### Long-term (Complex)

1. Multi-threading with row-level locking
2. ACID transaction support
3. Query planner and optimizer
4. Buffer pool manager
5. Custom binary storage format
6. Network protocol (client-server)
7. Replication and sharding

## Testing Strategy

### Unit Tests (test_rdbms.py)

Tests cover:
1. Table creation
2. Data insertion
3. Data selection (with/without WHERE)
4. Data updates
5. Data deletion
6. JOIN operations
7. Constraint enforcement
8. Indexing functionality
9. Persistence (save/load)

### Integration Tests (Web App)

The Flask application serves as an integration test:
- Real-world CRUD operations
- Multiple tables with relationships
- JOIN queries
- User interface interaction

### Manual Testing (REPL)

Interactive shell allows:
- Ad-hoc query testing
- Edge case exploration
- Performance observation

## Conclusion

This RDBMS implementation demonstrates fundamental database concepts:
- Schema management
- Query parsing and execution
- Indexing for performance
- Constraint enforcement
- Data persistence

While not production-ready, it showcases understanding of:
- Data structures (B-trees, hash tables)
- Algorithms (parsing, searching, joining)
- Software design (modularity, abstraction)
- System architecture (layered design)

The implementation prioritizes clarity and correctness over performance, making it suitable for educational purposes and demonstrating core RDBMS concepts.

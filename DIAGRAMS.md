# System Diagrams

## Component Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACES                          │
├─────────────────────────────┬───────────────────────────────────┤
│      REPL (Terminal)        │      Web App (Browser)            │
│  - Interactive shell        │  - HTML/CSS/JavaScript UI         │
│  - .exit, .save, .load      │  - REST API calls                 │
│  - Direct SQL input         │  - Real-time updates              │
└──────────────┬──────────────┴──────────────┬────────────────────┘
               │                              │
               │         SQL Queries          │
               │                              │
┌──────────────┴──────────────────────────────┴────────────────────┐
│                        SQL PARSER                                 │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Regex-based Pattern Matching                             │  │
│  │  - CREATE TABLE → _create_table()                         │  │
│  │  - INSERT INTO  → _insert()                               │  │
│  │  - SELECT       → _select() / _select_join()              │  │
│  │  - UPDATE       → _update()                               │  │
│  │  - DELETE FROM  → _delete()                               │  │
│  │  - DROP TABLE   → _drop_table()                           │  │
│  └────────────────────────────────────────────────────────────┘  │
└───────────────────────────────┬───────────────────────────────────┘
                                │
                    Parsed Operations
                                │
┌───────────────────────────────┴───────────────────────────────────┐
│                        DATABASE ENGINE                            │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Database                                                  │  │
│  │  - tables: Dict[str, Table]                               │  │
│  │  - save(filepath)                                         │  │
│  │  - load(filepath)                                         │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Table                                                     │  │
│  │  - columns: Dict[str, Column]                             │  │
│  │  - rows: List[Dict]                                       │  │
│  │  - indexes: Dict[str, BTreeIndex]                         │  │
│  │  - insert(values) → validate → check constraints → add    │  │
│  │  - select(cols, where) → filter → project                 │  │
│  │  - update(values, where) → find → validate → modify       │  │
│  │  - delete(where) → find → remove                          │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Column                                                    │  │
│  │  - name, dtype, primary_key, unique, nullable             │  │
│  │  - validate(value) → type checking → constraints          │  │
│  └────────────────────────────────────────────────────────────┘  │
└───────────────────────────────┬───────────────────────────────────┘
                                │
                        Storage Operations
                                │
┌───────────────────────────────┴───────────────────────────────────┐
│                        STORAGE LAYER                              │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  BTreeIndex (Dictionary-based)                            │  │
│  │  {                                                        │  │
│  │    value1: [row_id1, row_id2],                           │  │
│  │    value2: [row_id3],                                    │  │
│  │    ...                                                   │  │
│  │  }                                                       │  │
│  │  - insert(key, row_id)                                  │  │
│  │  - search(key) → [row_ids]                              │  │
│  │  - delete(key, row_id)                                  │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  In-Memory Row Storage                                    │  │
│  │  [                                                        │  │
│  │    {'_id': 0, 'col1': val1, 'col2': val2},              │  │
│  │    {'_id': 1, 'col1': val3, 'col2': val4},              │  │
│  │    ...                                                   │  │
│  │  ]                                                       │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Disk Persistence (Pickle)                                │  │
│  │  - Serialize entire Database object                       │  │
│  │  - Save to .db file                                       │  │
│  │  - Load from .db file                                     │  │
│  └────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────┘
```

## Data Flow: INSERT Operation

```
User Input: INSERT INTO users (id, name) VALUES (1, 'Alice')
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│ SQLParser._insert()                                     │
│ - Regex match: table='users', cols=['id','name'],      │
│                vals=[1, 'Alice']                        │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│ Database.get_table('users')                             │
│ - Returns Table object                                  │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│ Table.insert({'id': 1, 'name': 'Alice'})                │
│ Step 1: Create row with _id                             │
│         row = {'_id': 0, 'id': None, 'name': None}      │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│ For each column:                                        │
│   Column.validate(value)                                │
│   - 'id': INT → int(1) = 1 ✓                           │
│   - 'name': VARCHAR(100) → 'Alice' ✓                   │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│ Check constraints (if PRIMARY KEY or UNIQUE):           │
│   BTreeIndex.search(value)                              │
│   - 'id' is PRIMARY KEY                                 │
│   - Search index for value 1                            │
│   - Not found → OK to insert ✓                          │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│ Add row to table:                                       │
│   table.rows.append({'_id': 0, 'id': 1, 'name': 'Alice'})│
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│ Update indexes:                                         │
│   BTreeIndex.insert(1, 0)  # value=1, row_id=0          │
│   index['id'] = {1: [0]}                                │
└────────────────────┬────────────────────────────────────┘
                     ▼
                  Success!
```

## Data Flow: SELECT with WHERE

```
User Input: SELECT name FROM users WHERE id=1
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│ SQLParser._select()                                     │
│ - cols = ['name']                                       │
│ - table = 'users'                                       │
│ - where = 'id=1'                                        │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│ SQLParser._parse_where('id=1')                          │
│ - Regex match: col='id', op='=', val='1'               │
│ - Create lambda: lambda row: row.get('id') == 1         │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│ Table.select(['name'], where_func)                      │
│ For each row in table.rows:                             │
│   if where_func(row):  # Check id == 1                  │
│     results.append({'name': row['name']})               │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│ Return results:                                         │
│ [{'name': 'Alice'}]                                     │
└─────────────────────────────────────────────────────────┘
```

## Data Flow: JOIN Operation

```
User Input: SELECT users.name, posts.title 
            FROM users JOIN posts ON users.id=posts.user_id
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│ SQLParser._select_join()                                │
│ - table1 = 'users', table2 = 'posts'                    │
│ - join_col1 = 'id', join_col2 = 'user_id'              │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│ Nested Loop Join:                                       │
│ for row1 in users.rows:                                 │
│   for row2 in posts.rows:                               │
│     if row1['id'] == row2['user_id']:                   │
│       joined = {                                        │
│         'users.id': row1['id'],                         │
│         'users.name': row1['name'],                     │
│         'posts.id': row2['id'],                         │
│         'posts.user_id': row2['user_id'],               │
│         'posts.title': row2['title']                    │
│       }                                                 │
│       results.append(joined)                            │
└────────────────────┬────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────┐
│ Project requested columns:                              │
│ [{'users.name': 'Alice', 'posts.title': 'First Post'}] │
└─────────────────────────────────────────────────────────┘
```

## Web Application Flow

```
Browser                Flask App              RDBMS
   │                       │                     │
   │  GET /users           │                     │
   ├──────────────────────>│                     │
   │                       │  SELECT * FROM users│
   │                       ├────────────────────>│
   │                       │                     │
   │                       │  [user1, user2, ...] │
   │                       │<────────────────────┤
   │  JSON response        │                     │
   │<──────────────────────┤                     │
   │                       │                     │
   │  POST /users          │                     │
   │  {id:1, name:'Alice'} │                     │
   ├──────────────────────>│                     │
   │                       │  INSERT INTO users  │
   │                       ├────────────────────>│
   │                       │                     │
   │                       │  Success            │
   │                       │<────────────────────┤
   │                       │  db.save()          │
   │                       ├────────────────────>│
   │  {message: 'created'} │                     │
   │<──────────────────────┤                     │
   │                       │                     │
```

## Index Structure Example

```
Table: users
Columns: id (PRIMARY KEY), name, email (UNIQUE)

Rows:
[
  {'_id': 0, 'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
  {'_id': 1, 'id': 2, 'name': 'Bob', 'email': 'bob@example.com'},
  {'_id': 2, 'id': 3, 'name': 'Charlie', 'email': 'charlie@example.com'}
]

Indexes:
{
  'id': {
    1: [0],  # value 1 → row_id 0
    2: [1],  # value 2 → row_id 1
    3: [2]   # value 3 → row_id 2
  },
  'email': {
    'alice@example.com': [0],
    'bob@example.com': [1],
    'charlie@example.com': [2]
  }
}

Lookup: WHERE id=2
  1. Check index['id'][2] → [1]
  2. Get rows[1] → {'_id': 1, 'id': 2, 'name': 'Bob', ...}
  3. Return result
  
Time: O(1) average (dictionary lookup)
```

## File Persistence

```
In-Memory Database Object
         │
         │ db.save('mydata.db')
         ▼
┌─────────────────────────┐
│   Pickle Serialization  │
│   - Convert to bytes    │
│   - Preserve structure  │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│   Write to Disk         │
│   mydata.db (binary)    │
└────────┬────────────────┘
         │
         │ Database.load('mydata.db')
         ▼
┌─────────────────────────┐
│   Pickle Deserialization│
│   - Read bytes          │
│   - Reconstruct objects │
└────────┬────────────────┘
         │
         ▼
In-Memory Database Object
```

## Testing Flow

```
test_rdbms.py
     │
     ├─> TEST 1: Create tables
     │   └─> CREATE TABLE users (...)
     │       └─> ✓ Table created
     │
     ├─> TEST 2: Insert data
     │   └─> INSERT INTO users VALUES (...)
     │       └─> ✓ 3 rows inserted
     │
     ├─> TEST 3: Select data
     │   ├─> SELECT * FROM users
     │   └─> SELECT ... WHERE age > 26
     │       └─> ✓ Correct results
     │
     ├─> TEST 4: Update data
     │   └─> UPDATE users SET age=26 WHERE id=1
     │       └─> ✓ Row updated
     │
     ├─> TEST 5: JOIN
     │   └─> SELECT ... FROM users JOIN posts ...
     │       └─> ✓ Joined correctly
     │
     ├─> TEST 6: Delete data
     │   └─> DELETE FROM posts WHERE views < 100
     │       └─> ✓ Rows deleted
     │
     ├─> TEST 7: Constraints
     │   ├─> Try duplicate PRIMARY KEY
     │   └─> Try duplicate UNIQUE
     │       └─> ✓ Both rejected
     │
     ├─> TEST 8: Indexing
     │   └─> Check index structures
     │       └─> ✓ Indexes correct
     │
     └─> TEST 9: Persistence
         ├─> db.save('test.db')
         └─> db = Database.load('test.db')
             └─> ✓ Data preserved

All tests passed! ✓
```

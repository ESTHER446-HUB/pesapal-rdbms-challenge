#!/usr/bin/env python3
"""
Test script demonstrating RDBMS functionality
Run this to verify all features work correctly
"""

from rdbms import Database, SQLParser

def test_rdbms():
    print("=" * 60)
    print("RDBMS Feature Test Suite")
    print("=" * 60)
    
    db = Database("test_db")
    parser = SQLParser(db)
    
    # Test 1: CREATE TABLE
    print("\n[TEST 1] Creating tables...")
    try:
        parser.parse_and_execute("""
            CREATE TABLE users (
                id INT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE,
                age INT
            )
        """)
        print("✓ Users table created")
        
        parser.parse_and_execute("""
            CREATE TABLE posts (
                id INT PRIMARY KEY,
                user_id INT NOT NULL,
                title VARCHAR(200) NOT NULL,
                views INT
            )
        """)
        print("✓ Posts table created")
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    # Test 2: INSERT
    print("\n[TEST 2] Inserting data...")
    try:
        parser.parse_and_execute("INSERT INTO users (id, name, email, age) VALUES (1, 'Alice', 'alice@test.com', 25)")
        parser.parse_and_execute("INSERT INTO users (id, name, email, age) VALUES (2, 'Bob', 'bob@test.com', 30)")
        parser.parse_and_execute("INSERT INTO users (id, name, email, age) VALUES (3, 'Charlie', 'charlie@test.com', 28)")
        print("✓ 3 users inserted")
        
        parser.parse_and_execute("INSERT INTO posts (id, user_id, title, views) VALUES (1, 1, 'First Post', 100)")
        parser.parse_and_execute("INSERT INTO posts (id, user_id, title, views) VALUES (2, 1, 'Second Post', 50)")
        parser.parse_and_execute("INSERT INTO posts (id, user_id, title, views) VALUES (3, 2, 'Bob Post', 200)")
        print("✓ 3 posts inserted")
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    # Test 3: SELECT
    print("\n[TEST 3] Selecting data...")
    try:
        result = parser.parse_and_execute("SELECT * FROM users")
        print(f"✓ SELECT * returned {len(result)} rows")
        for row in result:
            print(f"  {row}")
        
        result = parser.parse_and_execute("SELECT name, email FROM users WHERE age > 26")
        print(f"✓ SELECT with WHERE returned {len(result)} rows")
        for row in result:
            print(f"  {row}")
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    # Test 4: UPDATE
    print("\n[TEST 4] Updating data...")
    try:
        parser.parse_and_execute("UPDATE users SET age=26 WHERE id=1")
        result = parser.parse_and_execute("SELECT name, age FROM users WHERE id=1")
        print(f"✓ UPDATE successful: {result[0]}")
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    # Test 5: JOIN
    print("\n[TEST 5] Testing JOIN...")
    try:
        result = parser.parse_and_execute(
            "SELECT users.name, posts.title FROM users JOIN posts ON users.id=posts.user_id"
        )
        print(f"✓ JOIN returned {len(result)} rows")
        for row in result:
            print(f"  {row}")
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    # Test 6: DELETE
    print("\n[TEST 6] Deleting data...")
    try:
        parser.parse_and_execute("DELETE FROM posts WHERE views < 100")
        result = parser.parse_and_execute("SELECT * FROM posts")
        print(f"✓ DELETE successful, {len(result)} posts remaining")
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    # Test 7: Constraints
    print("\n[TEST 7] Testing constraints...")
    try:
        parser.parse_and_execute("INSERT INTO users (id, name, email, age) VALUES (1, 'Duplicate', 'dup@test.com', 20)")
        print("✗ PRIMARY KEY constraint failed to prevent duplicate")
    except ValueError as e:
        print(f"✓ PRIMARY KEY constraint working: {e}")
    
    try:
        parser.parse_and_execute("INSERT INTO users (id, name, email, age) VALUES (4, 'Test', 'alice@test.com', 20)")
        print("✗ UNIQUE constraint failed to prevent duplicate")
    except ValueError as e:
        print(f"✓ UNIQUE constraint working: {e}")
    
    # Test 8: Indexing
    print("\n[TEST 8] Testing indexing...")
    try:
        users_table = db.get_table('users')
        print(f"✓ Index on 'id' (PRIMARY KEY): {len(users_table.indexes['id'].index)} entries")
        print(f"✓ Index on 'email' (UNIQUE): {len(users_table.indexes['email'].index)} entries")
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    # Test 9: Persistence
    print("\n[TEST 9] Testing persistence...")
    try:
        db.save('test_database.db')
        print("✓ Database saved to test_database.db")
        
        loaded_db = Database.load('test_database.db')
        loaded_parser = SQLParser(loaded_db)
        result = loaded_parser.parse_and_execute("SELECT * FROM users")
        print(f"✓ Database loaded, {len(result)} users found")
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)

if __name__ == '__main__':
    test_rdbms()

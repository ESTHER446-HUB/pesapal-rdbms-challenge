#!/usr/bin/env python3
"""
Test script to demonstrate all web API functionality
Run this while the Flask app is running (python3 app.py)
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def test_api():
    print("🚀 Testing RDBMS Web API Functionality")
    print("=" * 50)
    
    # Test 1: Create users
    print("\n1. Creating users...")
    users = [
        {"id": 1, "name": "Alice Johnson", "email": "alice@example.com"},
        {"id": 2, "name": "Bob Smith", "email": "bob@example.com"},
        {"id": 3, "name": "Carol Davis", "email": "carol@example.com"}
    ]
    
    for user in users:
        try:
            response = requests.post(f"{BASE_URL}/users", json=user)
            if response.status_code == 201:
                print(f"✓ Created user: {user['name']}")
            else:
                print(f"⚠ User might already exist: {user['name']}")
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to Flask app. Make sure it's running with: python3 app.py")
            return
    
    # Test 2: Get all users
    print("\n2. Getting all users...")
    try:
        response = requests.get(f"{BASE_URL}/users")
        users_data = response.json()
        print(f"✓ Found {len(users_data)} users:")
        for user in users_data:
            print(f"   - {user['name']} ({user['email']})")
    except Exception as e:
        print(f"❌ Error getting users: {e}")
    
    # Test 3: Create tasks
    print("\n3. Creating tasks...")
    tasks = [
        {"id": 1, "user_id": 1, "title": "Complete project documentation", "completed": False},
        {"id": 2, "user_id": 1, "title": "Review code changes", "completed": True},
        {"id": 3, "user_id": 2, "title": "Fix database bug", "completed": False},
        {"id": 4, "user_id": 3, "title": "Write unit tests", "completed": False}
    ]
    
    for task in tasks:
        try:
            response = requests.post(f"{BASE_URL}/tasks", json=task)
            if response.status_code == 201:
                status = "✅" if task['completed'] else "⏳"
                print(f"✓ Created task: {task['title']} {status}")
            else:
                print(f"⚠ Task might already exist: {task['title']}")
        except Exception as e:
            print(f"❌ Error creating task: {e}")
    
    # Test 4: Get all tasks
    print("\n4. Getting all tasks...")
    try:
        response = requests.get(f"{BASE_URL}/tasks")
        tasks_data = response.json()
        print(f"✓ Found {len(tasks_data)} tasks:")
        for task in tasks_data:
            status = "✅" if task['completed'] else "⏳"
            print(f"   - {task['title']} {status}")
    except Exception as e:
        print(f"❌ Error getting tasks: {e}")
    
    # Test 5: Test JOIN query (users with their tasks)
    print("\n5. Testing JOIN query (users with their tasks)...")
    try:
        response = requests.get(f"{BASE_URL}/users-with-tasks")
        join_data = response.json()
        print(f"✓ JOIN query returned {len(join_data)} results:")
        for item in join_data:
            print(f"   - {item['users.name']}: {item['tasks.title']}")
    except Exception as e:
        print(f"❌ Error with JOIN query: {e}")
    
    # Test 6: Update a task
    print("\n6. Updating a task...")
    try:
        update_data = {"title": "Complete project documentation (UPDATED)", "completed": True}
        response = requests.put(f"{BASE_URL}/tasks/1", json=update_data)
        if response.status_code == 200:
            print("✓ Task updated successfully")
        else:
            print(f"⚠ Update response: {response.status_code}")
    except Exception as e:
        print(f"❌ Error updating task: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API Test Complete!")
    print(f"📱 Visit the web interface at: {BASE_URL}")
    print("💡 Try the REPL with: python3 rdbms.py")

if __name__ == "__main__":
    test_api()
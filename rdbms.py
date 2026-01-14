import re
import pickle
import os
from typing import Any, Dict, List, Optional, Tuple
from collections import defaultdict

class Column:
    def __init__(self, name: str, dtype: str, primary_key: bool = False, unique: bool = False, nullable: bool = True):
        self.name = name
        self.dtype = dtype.upper()
        self.primary_key = primary_key
        self.unique = unique
        self.nullable = nullable if not primary_key else False
    
    def validate(self, value):
        if value is None:
            if not self.nullable:
                raise ValueError(f"Column {self.name} cannot be NULL")
            return None
        
        if self.dtype == 'INT':
            return int(value)
        elif self.dtype == 'FLOAT':
            return float(value)
        elif self.dtype == 'BOOLEAN':
            if isinstance(value, bool):
                return value
            return str(value).upper() in ('TRUE', '1', 'YES')
        elif self.dtype.startswith('VARCHAR'):
            max_len = int(re.search(r'\d+', self.dtype).group()) if re.search(r'\d+', self.dtype) else 255
            s = str(value)
            if len(s) > max_len:
                raise ValueError(f"String too long for {self.name} (max {max_len})")
            return s
        return value

class BTreeIndex:
    def __init__(self):
        self.index = {}
    
    def insert(self, key, row_id):
        if key not in self.index:
            self.index[key] = []
        self.index[key].append(row_id)
    
    def search(self, key):
        return self.index.get(key, [])
    
    def delete(self, key, row_id):
        if key in self.index:
            self.index[key].remove(row_id)
            if not self.index[key]:
                del self.index[key]

class Table:
    def __init__(self, name: str, columns: List[Column]):
        self.name = name
        self.columns = {col.name: col for col in columns}
        self.rows = []
        self.next_id = 0
        self.indexes = {}
        self.primary_key_col = None
        self.unique_cols = []
        
        for col in columns:
            if col.primary_key:
                self.primary_key_col = col.name
                self.indexes[col.name] = BTreeIndex()
            if col.unique:
                self.unique_cols.append(col.name)
                self.indexes[col.name] = BTreeIndex()
    
    def insert(self, values: Dict[str, Any]) -> int:
        row = {'_id': self.next_id}
        
        for col_name, col in self.columns.items():
            value = values.get(col_name)
            validated = col.validate(value)
            
            if col.primary_key or col.unique:
                if validated is not None and self.indexes[col_name].search(validated):
                    raise ValueError(f"Duplicate value for {col_name}")
            
            row[col_name] = validated
        
        self.rows.append(row)
        
        for col_name in self.indexes:
            if row[col_name] is not None:
                self.indexes[col_name].insert(row[col_name], self.next_id)
        
        self.next_id += 1
        return self.next_id - 1
    
    def select(self, columns: List[str] = None, where: callable = None) -> List[Dict]:
        results = []
        for row in self.rows:
            if where is None or where(row):
                if columns:
                    results.append({k: row[k] for k in columns if k in row})
                else:
                    results.append({k: v for k, v in row.items() if k != '_id'})
        return results
    
    def update(self, values: Dict[str, Any], where: callable) -> int:
        count = 0
        for row in self.rows:
            if where(row):
                for col_name, value in values.items():
                    if col_name in self.columns:
                        old_val = row[col_name]
                        new_val = self.columns[col_name].validate(value)
                        
                        if col_name in self.indexes:
                            if old_val is not None:
                                self.indexes[col_name].delete(old_val, row['_id'])
                            if new_val is not None:
                                if self.indexes[col_name].search(new_val):
                                    raise ValueError(f"Duplicate value for {col_name}")
                                self.indexes[col_name].insert(new_val, row['_id'])
                        
                        row[col_name] = new_val
                count += 1
        return count
    
    def delete(self, where: callable) -> int:
        to_delete = [row for row in self.rows if where(row)]
        for row in to_delete:
            for col_name in self.indexes:
                if row[col_name] is not None:
                    self.indexes[col_name].delete(row[col_name], row['_id'])
            self.rows.remove(row)
        return len(to_delete)

class Database:
    def __init__(self, name: str = "mydb"):
        self.name = name
        self.tables = {}
    
    def create_table(self, table_name: str, columns: List[Column]):
        if table_name in self.tables:
            raise ValueError(f"Table {table_name} already exists")
        self.tables[table_name] = Table(table_name, columns)
    
    def drop_table(self, table_name: str):
        if table_name not in self.tables:
            raise ValueError(f"Table {table_name} does not exist")
        del self.tables[table_name]
    
    def get_table(self, table_name: str) -> Table:
        if table_name not in self.tables:
            raise ValueError(f"Table {table_name} does not exist")
        return self.tables[table_name]
    
    def save(self, filepath: str):
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)
    
    @staticmethod
    def load(filepath: str):
        with open(filepath, 'rb') as f:
            return pickle.load(f)

class SQLParser:
    def __init__(self, db: Database):
        self.db = db
    
    def parse_and_execute(self, sql: str):
        sql = sql.strip().rstrip(';')
        
        if sql.upper().startswith('CREATE TABLE'):
            return self._create_table(sql)
        elif sql.upper().startswith('INSERT INTO'):
            return self._insert(sql)
        elif sql.upper().startswith('SELECT'):
            return self._select(sql)
        elif sql.upper().startswith('UPDATE'):
            return self._update(sql)
        elif sql.upper().startswith('DELETE FROM'):
            return self._delete(sql)
        elif sql.upper().startswith('DROP TABLE'):
            return self._drop_table(sql)
        else:
            raise ValueError("Unsupported SQL statement")
    
    def _create_table(self, sql: str):
        match = re.match(r'CREATE TABLE (\w+)\s*\((.*)\)', sql, re.IGNORECASE | re.DOTALL)
        if not match:
            raise ValueError("Invalid CREATE TABLE syntax")
        
        table_name = match.group(1)
        cols_def = match.group(2)
        
        columns = []
        for col_def in cols_def.split(','):
            col_def = col_def.strip()
            parts = col_def.split()
            col_name = parts[0]
            col_type = parts[1]
            
            primary_key = 'PRIMARY KEY' in col_def.upper()
            unique = 'UNIQUE' in col_def.upper()
            nullable = 'NOT NULL' not in col_def.upper()
            
            columns.append(Column(col_name, col_type, primary_key, unique, nullable))
        
        self.db.create_table(table_name, columns)
        return f"Table {table_name} created"
    
    def _insert(self, sql: str):
        match = re.match(r'INSERT INTO (\w+)\s*\((.*?)\)\s*VALUES\s*\((.*?)\)', sql, re.IGNORECASE)
        if not match:
            raise ValueError("Invalid INSERT syntax")
        
        table_name = match.group(1)
        columns = [c.strip() for c in match.group(2).split(',')]
        values = [v.strip().strip("'\"") for v in match.group(3).split(',')]
        
        table = self.db.get_table(table_name)
        row_data = dict(zip(columns, values))
        table.insert(row_data)
        return "1 row inserted"
    
    def _select(self, sql: str):
        join_match = re.search(r'JOIN\s+(\w+)\s+ON\s+([\w.]+)\s*=\s*([\w.]+)', sql, re.IGNORECASE)
        
        if join_match:
            return self._select_join(sql, join_match)
        
        match = re.match(r'SELECT (.*?) FROM (\w+)(?:\s+WHERE\s+(.*))?', sql, re.IGNORECASE)
        if not match:
            raise ValueError("Invalid SELECT syntax")
        
        cols = match.group(1).strip()
        table_name = match.group(2)
        where_clause = match.group(3)
        
        table = self.db.get_table(table_name)
        columns = None if cols == '*' else [c.strip() for c in cols.split(',')]
        
        where_func = self._parse_where(where_clause) if where_clause else None
        return table.select(columns, where_func)
    
    def _select_join(self, sql: str, join_match):
        main_match = re.match(r'SELECT (.*?) FROM (\w+)\s+JOIN', sql, re.IGNORECASE)
        cols = main_match.group(1).strip()
        table1_name = main_match.group(2)
        table2_name = join_match.group(1)
        join_col1 = join_match.group(2)
        join_col2 = join_match.group(3)
        
        t1_col = join_col1.split('.')[1] if '.' in join_col1 else join_col1
        t2_col = join_col2.split('.')[1] if '.' in join_col2 else join_col2
        
        table1 = self.db.get_table(table1_name)
        table2 = self.db.get_table(table2_name)
        
        results = []
        for row1 in table1.rows:
            for row2 in table2.rows:
                if row1.get(t1_col) == row2.get(t2_col):
                    joined = {}
                    for k, v in row1.items():
                        if k != '_id':
                            joined[f"{table1_name}.{k}"] = v
                    for k, v in row2.items():
                        if k != '_id':
                            joined[f"{table2_name}.{k}"] = v
                    results.append(joined)
        
        if cols != '*':
            col_list = [c.strip() for c in cols.split(',')]
            results = [{k: row[k] for k in col_list if k in row} for row in results]
        
        return results
    
    def _update(self, sql: str):
        match = re.match(r'UPDATE (\w+) SET (.*?)(?:\s+WHERE\s+(.*))?$', sql, re.IGNORECASE)
        if not match:
            raise ValueError("Invalid UPDATE syntax")
        
        table_name = match.group(1)
        set_clause = match.group(2)
        where_clause = match.group(3)
        
        table = self.db.get_table(table_name)
        
        updates = {}
        for assignment in set_clause.split(','):
            parts = assignment.split('=', 1)
            if len(parts) != 2:
                raise ValueError(f"Invalid SET clause: {assignment}")
            col, val = parts
            updates[col.strip()] = val.strip().strip("'\"")
        
        where_func = self._parse_where(where_clause) if where_clause else lambda x: True
        count = table.update(updates, where_func)
        return f"{count} row(s) updated"
    
    def _delete(self, sql: str):
        match = re.match(r'DELETE FROM (\w+)(?:\s+WHERE\s+(.*))?', sql, re.IGNORECASE)
        if not match:
            raise ValueError("Invalid DELETE syntax")
        
        table_name = match.group(1)
        where_clause = match.group(2)
        
        table = self.db.get_table(table_name)
        where_func = self._parse_where(where_clause) if where_clause else lambda x: True
        count = table.delete(where_func)
        return f"{count} row(s) deleted"
    
    def _drop_table(self, sql: str):
        match = re.match(r'DROP TABLE (\w+)', sql, re.IGNORECASE)
        if not match:
            raise ValueError("Invalid DROP TABLE syntax")
        
        table_name = match.group(1)
        self.db.drop_table(table_name)
        return f"Table {table_name} dropped"
    
    def _parse_where(self, where_clause: str):
        where_clause = where_clause.strip()
        
        match = re.match(r"(\w+)\s*(=|!=|>|<|>=|<=)\s*(.+)", where_clause)
        if match:
            col = match.group(1)
            op = match.group(2)
            val = match.group(3).strip().strip("'\"")
            
            def where_func(row):
                row_val = row.get(col)
                if row_val is None:
                    return False
                try:
                    if isinstance(row_val, (int, float)):
                        try:
                            val_typed = type(row_val)(val)
                        except:
                            val_typed = val
                    else:
                        val_typed = val
                    
                    if op == '=': return row_val == val_typed
                    elif op == '!=': return row_val != val_typed
                    elif op == '>': return row_val > val_typed
                    elif op == '<': return row_val < val_typed
                    elif op == '>=': return row_val >= val_typed
                    elif op == '<=': return row_val <= val_typed
                except:
                    return False
            
            return where_func
        
        return lambda x: True

def repl(db: Database):
    parser = SQLParser(db)
    print("=" * 50)
    print("Simple RDBMS - Interactive REPL")
    print("=" * 50)
    print("Commands: SQL statements, .exit, .save <file>, .load <file>, .tables")
    print()
    
    while True:
        try:
            query = input("rdbms> ").strip()
            
            if not query:
                continue
            
            if query == '.exit':
                print("Goodbye!")
                break
            elif query.startswith('.save'):
                filepath = query.split()[1] if len(query.split()) > 1 else 'database.db'
                db.save(filepath)
                print(f"Database saved to {filepath}")
            elif query.startswith('.load'):
                filepath = query.split()[1] if len(query.split()) > 1 else 'database.db'
                if os.path.exists(filepath):
                    db = Database.load(filepath)
                    parser = SQLParser(db)
                    print(f"Database loaded from {filepath}")
                else:
                    print(f"File {filepath} not found")
            elif query == '.tables':
                if db.tables:
                    print("Tables:", ', '.join(db.tables.keys()))
                else:
                    print("No tables")
            else:
                result = parser.parse_and_execute(query)
                if isinstance(result, list):
                    if result:
                        print(f"\n{len(result)} row(s) returned:")
                        for row in result:
                            print(row)
                    else:
                        print("0 rows returned")
                else:
                    print(result)
        
        except KeyboardInterrupt:
            print("\nUse .exit to quit")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    db = Database()
    repl(db)

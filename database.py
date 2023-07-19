import sqlite3
import os

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.create_db_if_not_exists()

    def create_db_if_not_exists(self):
        if not os.path.exists(self.db_name):
            with sqlite3.connect(self.db_name) as conn:
                with open('initialise_db.sql', 'r') as sql_file:
                    create_table_query = sql_file.read()
                    conn.executescript(create_table_query)

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.conn.execute("PRAGMA foreign_keys = ON")

    def close(self):
        if self.conn:
            self.conn.close()

    def select(self, table_name, condition=None):
        with self.conn:
            cursor = self.conn.cursor()
            query = f"SELECT * FROM {table_name}"
            if condition:
                query += f" WHERE {condition}"
            cursor.execute(query)
            return cursor.fetchall()

    def insert(self, table_name, data):
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary with column names as keys and values to be inserted.")

        if not data:
            raise ValueError("Data dictionary is empty.")

        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data.values()])

        with self.conn:
            cursor = self.conn.cursor()
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(query, tuple(data.values()))

    def update(self, table_name, data, condition=None):
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary with column names as keys and values to be updated.")

        if not data:
            raise ValueError("Data dictionary is empty.")

        with self.conn:
            cursor = self.conn.cursor()
            set_values = ', '.join([f"{column} = ?" for column in data.keys()])
            query = f"UPDATE {table_name} SET {set_values}"
            if condition:
                query += f" WHERE {condition}"
            cursor.execute(query, tuple(data.values()))

    def delete(self, table_name, condition=None):
        with self.conn:
            cursor = self.conn.cursor()
            query = f"DELETE FROM {table_name}"
            if condition:
                query += f" WHERE {condition}"
            cursor.execute(query)


import sqlite3
from flask import g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('sqlite:///database/database.db')
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db():
    db = get_db()
    with open('database/schema.sql', 'r') as f:
        db.executescript(f.read())
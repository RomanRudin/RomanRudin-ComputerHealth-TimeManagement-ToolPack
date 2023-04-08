import sqlite3 as sql

class db():
    def __init__(self) -> None:
        conn = sql.connect() #TODO  
        cursoer = sql.Cursor()
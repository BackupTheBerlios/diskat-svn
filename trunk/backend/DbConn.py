import sqlite
import DbCursor
import warnings

# Disable annoying warning
warnings.filterwarnings("ignore", ".*lastrowid used.*", UserWarning, "sqlite")

class DbConn:

    def __init__(self, db_name):
        self.conn = sqlite.connect(db = db_name)

    def getCursor(self):
        return DbCursor.DbCursor(self.conn.cursor())

    def commit(self):
        self.conn.commit()

def quote(str):
    return sqlite.main._quote(str)

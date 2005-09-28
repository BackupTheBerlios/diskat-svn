import sqlite

class DbCursor:
    "Logging wrapper around DB API cursor object"

    def __init__(self, cursor):
        self.cursor = cursor

    def __getattr__(self, attr_name):
        return self.cursor.__getattr__(attr_name)
        if attr_name == "rowcount":
            return self.cursor.rowcount
        else:
            raise AttributeError

    def execute(self, sql):
#        f = open("sql.log", "a")
#        f.write(sql + "\n\n")
#        f.close()
        return self.cursor.execute(sql)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()


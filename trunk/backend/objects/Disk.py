import diskat_config
import DbConn


class Disk:

    def __init__(self, connection):
        self.connection = connection

    def findByTag(self, diskTag):
        cursor = self.connection.getCursor()
        cursor.execute("SELECT * FROM disk WHERE tag=%s" % (DbConn.quote(diskTag)))
        if cursor.rowcount != 1: return None
        return cursor.fetchone()


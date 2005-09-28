import diskat_config
import DbConn

class File:

    def __init__(self, connection):
        self.connection = connection

    def findByDiskIdAndName(self, diskId, name):
        cursor = self.connection.getCursor()
        cursor.execute("SELECT * FROM directory WHERE snapshot=%d AND name=%s" % (diskId, DbConn.quote(name)))
        return cursor.fetchall()

import diskat_config
import DbConn
import time


class Category:

    FILE = 1
    DISK = 2
    
    def __init__(self, connection):
        self.connection = connection

    def findByTypeAndName(self, type, name):
        cursor = self.connection.getCursor()
        cursor.execute("SELECT * FROM category WHERE type=%d AND name=%s" % (type, DbConn.quote(name)))
        if cursor.rowcount != 1: return None
        return cursor.fetchone()

    def addFileCategory(self, fileId, categoryId, timeStamp = None):
        if timeStamp == None: 
            timeStamp = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        cursor = self.connection.getCursor()
        cursor.execute("""\
            INSERT INTO category_map(cat_id, obj_id, tstamp) 
            VALUES (%d, %d, '%s')
        """ % (categoryId, fileId, timeStamp))
        self.connection.commit()

    def deleteFileCategory(self, fileId, categoryId):
        cursor = self.connection.getCursor()
        cursor.execute("""\
            DELETE FROM category_map
            WHERE cat_id=%d AND obj_id=%d
        """ % (categoryId, fileId))
        self.connection.commit()


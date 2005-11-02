import time
import string
import diskat_config
import DbConn


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

    def addFileCategory(self, fileId, categoryId, value = None, timeStamp = None):
        if timeStamp == None: 
            timeStamp = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        cursor = self.connection.getCursor()
        cursor.execute("""\
            INSERT INTO category_map(cat_id, obj_id, value, tstamp) 
            VALUES (%d, %d, %s, '%s')
        """ % (categoryId, fileId, DbConn.quote(value), timeStamp))
        self.connection.commit()

    def deleteFileCategory(self, fileId, categoryId):
        cursor = self.connection.getCursor()
        cursor.execute("""\
            DELETE FROM category_map
            WHERE cat_id=%d AND obj_id=%d
        """ % (categoryId, fileId))
        self.connection.commit()

    def isCategoriesAssignedToFiles(self, fileIds):
        cursor = self.connection.getCursor()
        fileIds = map(lambda x: str(x), fileIds)
        cursor.execute("SELECT * FROM category_map WHERE obj_id IN (%s) LIMIT 1" % (string.join(fileIds, ",")))
        if cursor.rowcount != 0: return True
        return False

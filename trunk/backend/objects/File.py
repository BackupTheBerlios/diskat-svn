import diskat_config
import DbConn
import Disk

ARC_NONE	= 0
ARC_IS_ARCHIVE	= 1
ARC_IN_ARCHIVE	= 2

class File:

    def __init__(self, connection):
        self.connection = connection

    def findByDiskIdAndName(self, diskId, name):
        cursor = self.connection.getCursor()
        cursor.execute("SELECT * FROM directory WHERE snapshot=%d AND name=%s" % (diskId, DbConn.quote(name)))
        return cursor.fetchall()

    def findByParentIdAndName(self, diskId, parentId, name):
        cursor = self.connection.getCursor()
        cursor.execute("SELECT * FROM directory WHERE snapshot=%d AND parent=%d AND name=%s" % (diskId, parentId, DbConn.quote(name)))
        return cursor.fetchall()

    def findByDiskId(self, diskId):
        cursor = self.connection.getCursor()
        cursor.execute("SELECT * FROM directory WHERE snapshot=%d" % (diskId))
        return cursor.fetchall()

class DirectoryResolver:

    def __init__(self, connection):
        self.connection = connection
        self.cache = {}

    def getPathElementById(self, id):
        if self.cache.has_key(id):
            return self.cache[id]
        else:
            cursor = self.connection.getCursor()
            cursor.execute("SELECT * FROM directory WHERE id=%d" % id)
            rec = cursor.fetchone()
            self.cache[id] = rec
            return rec

    def getFilePath(self, id):
        result = ""
        while id != 0:
            pathElement = self.getPathElementById(id)
            parentId = pathElement['parent']
            if pathElement['arc_status'] != ARC_IN_ARCHIVE:
                parent = pathElement['name']
                result = parent + "/" + result
            id = parentId
        return result[1:-1]

    def getDirectoryPath(self, id):
        result = ""
        while id != 0:
            pathElement = self.getPathElementById(id)
            parentId = pathElement['parent']
            if pathElement['arc_status'] != ARC_IN_ARCHIVE and pathElement['is_dir']:
                parent = pathElement['name']
                result = parent + "/" + result
            id = parentId
        return result[1:-1]

    def getIdByPath(self, diskId, path):
        assert path[0] == "/"
        fileApi = File(self.connection)
        root = fileApi.findByParentIdAndName(diskId, 0, "/")
        if path == "/": return root

        components = path[1:].split("/")
        for c in components:
            root = fileApi.findByParentIdAndName(diskId, root[0]['id'], c)
        return root

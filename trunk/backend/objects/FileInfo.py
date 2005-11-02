import stat
import time


class FileInfo:
    
    MATCH_TYPE  = 1
    MATCH_NAME  = 2
    MATCH_SIZE  = 4
    MATCH_MTIME = 8
    MATCH_ALL   = MATCH_TYPE|MATCH_NAME|MATCH_SIZE|MATCH_MTIME

    def __init__(self, fromDb = None, fromStat = None, name = None):
        if fromDb:
            self._createFromDb(fromDb)
        else:
            self._createFromStat(name, fromStat)

    def _createFromStat(self, name, statInfo):
        self.name = name
        self.size = statInfo[stat.ST_SIZE]
        self.mtime = time.strftime("%Y%m%d%H%M%S", time.localtime(statInfo[stat.ST_MTIME]))
        if stat.S_ISDIR(statInfo[stat.ST_MODE]):
            self.isDir = True
        else:
            self.isDir = False

    def _createFromDb(self, dbRow):
        self.name = dbRow["name"]
        self.size = dbRow["size"]
        self.mtime = dbRow["mdate"]
        if dbRow["is_dir"]:
            self.isDir = True
        else:
            self.isDir = False

    def compare(self, another):
        result = 0
        if self.isDir == another.isDir: result |= FileInfo.MATCH_TYPE
        if self.name  == another.name:  result |= FileInfo.MATCH_NAME
        if self.size  == another.size:  result |= FileInfo.MATCH_SIZE
        if self.mtime == another.mtime: result |= FileInfo.MATCH_MTIME
        return result

    def __repr__(self):
        return "<FileInfo %s%s %d %s>" % (self.name, ["", "/"][self.isDir], self.size, self.mtime)

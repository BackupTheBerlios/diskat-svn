import diskat_config
import DbConn
import time
import stat
import string
import sys
import IFileInfoAcceptor
import Const

class DbDumper(IFileInfoAcceptor.IFileInfoAcceptor): 

    c = None
    file_no = 0
    numFiles = 0
    numDirectories = 0
    numArcFiles = 0
    numArcDirectories = 0
    numArchives = 0

    def __init__(self, cursor, disk_id, feedbackObject):
        self.c = cursor
        self.feedbackObject = feedbackObject
        self.disk_id = disk_id
        self.file_no = 0

    def accept(self, parent_id, name, stat_info, arc_flag):
        is_dir = 0
        if stat.S_ISDIR(stat_info[stat.ST_MODE]):
            is_dir = 1
        ext = ''
        i = string.rfind(name, ".")
        if i != -1: ext = name[i+1:]
        self.file_no = self.file_no + 1
        self.c.execute("""
            INSERT INTO directory(snapshot, no, parent, name, extension, size, is_dir, arc_status, mdate)
            VALUES (%d, %d, %s, %s, %s, %d, %d, %d, '%s')
        """ % (self.disk_id, self.file_no, parent_id, DbConn.quote(name), DbConn.quote(ext), 
               stat_info[stat.ST_SIZE], is_dir, arc_flag, time.strftime("%Y%m%d%H%M%S", time.localtime(stat_info[stat.ST_MTIME])))
        )
        id = self.c.lastrowid

        # Update UI with status
        self.feedbackObject.feedback(self.file_no);

        # Bookkeeping
        if arc_flag == Const.ARC_IN_ARCHIVE:
            if stat.S_ISDIR(stat_info[stat.ST_MODE]): 
                self.numArcDirectories = self.numArcDirectories + 1
            else: 
                self.numArcFiles = self.numArcFiles + 1
        else:
            if stat.S_ISDIR(stat_info[stat.ST_MODE]): 
                self.numDirectories = self.numDirectories + 1
            else: 
                self.numFiles = self.numFiles + 1
                if arc_flag == Const.ARC_IS_ARCHIVE:
                    self.numArchives += 1

        return int(id)

    def updateArchiveFlag(self, id, arc_flag):
        self.c.execute("""
            UPDATE directory
            SET arc_status=%d
            WHERE id=%d
        """ % (arc_flag, id))

    def finish(self):
        self.feedbackObject.feedback(None);

    def getStats(self):
        s = [self.numFiles, self.numDirectories, self.numArcFiles, self.numArcDirectories, self.numArchives]
        return s

class App:

    def __init__(self):
        self.conn = DbConn.DbConn(diskat_config.dbname)

    def feedback(self, num):
        if num == None:
            sys.stderr.write("done    \r                       \r")
        else:
            sys.stderr.write("% 7d\b\b\b\b\b\b\b" % num)

    def _findDisk(self, criteria):
        c = self.conn.getCursor()
        c.execute("""\
            SELECT *
            FROM disk
            WHERE %s
        """ % criteria)
        if c.rowcount != 1: return None
        return c.fetchone()

    def findDiskBySerialAndLabel(self, serial, label):
	return self._findDisk("serial='%s' AND label='%s'" % (serial, label))

    def findDiskByTag(self, tag):
	return self._findDisk("tag='%s'" % (tag))

    def addDisk(self, volume, tag, title):
        c = self.conn.getCursor()
        c.execute("""
            INSERT INTO disk(last_update, root, serial, label, tag, title)
            VALUES (%d, '%s', '%s', '%s', '%s' , '%s')
        """ % (time.time(), volume.getRoot(), volume.getSerialNumber(), volume.getLabel(), tag, title))
        id = c.lastrowid
        return int(id)
        
    def catalogDisk(self, volume, id):
        dumper = DbDumper(self.conn.getCursor(), id, self)
        volume.enumerateFiles(dumper)
        return dumper.getStats()

    def checkDiskTag(self, tag):
        if not self._findDisk("tag='%s'" % tag):
            return 1
        return 0

    def clearDiskContents(self, diskId):
        c = self.conn.getCursor()
        c.execute("""
            DELETE FROM directory
            WHERE snapshot = %d
        """ % diskId)

    def deleteDisk(self, diskId):
        self.clearDiskContents(diskId)
        c = self.conn.getCursor()
        c.execute("""
            DELETE FROM disk
            WHERE id = %d
        """ % diskId)

    def commit(self):
        self.conn.commit()

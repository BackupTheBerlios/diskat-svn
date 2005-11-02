import diskat_config
import DbConn
import time
import stat
import string
import sys
import os
import IFileInfoAcceptor
import Const
import objects.File
import objects.FileInfo
import objects.Category
from objects.FileInfo import FileInfo

class DbDumper(IFileInfoAcceptor.IFileInfoAcceptor): 

    c = None
    file_no = 0
    numFiles = 0
    numDirectories = 0
    numArcFiles = 0
    numArcDirectories = 0
    numArchives = 0

    def __init__(self, connection, disk_id, feedbackObject):
        self.connection = connection
        self.c = self.connection.getCursor()
        self.feedbackObject = feedbackObject
        self.disk_id = disk_id
        self.file_no = 0

    def setVolume(self, volume):
        self.volume = volume

    def getExt(self, name):
        ext = ''
        i = string.rfind(name, ".")
        if i != -1: ext = name[i+1:]
        return ext
    
    def accept(self, parent_id, name, stat_info, arc_flag, fullPath = None):
        is_dir = 0
        if stat.S_ISDIR(stat_info[stat.ST_MODE]):
            is_dir = 1
        ext = self.getExt(name)
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

class DbUpdateDumper(DbDumper): 

    DEBUG_SQL = 1
    DEBUG_STAGE_1 = 2
    DEBUG_STAGE_2 = 4
    DEBUG_STAGE_3 = 8
    
    def __init__(self, connection, disk_id, feedbackObject, debugLevel = 0):
        DbDumper.__init__(self, connection, disk_id, feedbackObject)
        self.debugLevel = debugLevel
        self.fileApi = objects.File.File(connection)
        self.resolverApi = objects.File.DirectoryResolver(self.connection)
        self.oldFiles = self.fileApi.findByDiskId(disk_id)
        self.filenameMap = {}
        self.sizeMap = {}
        self.idMap = {}
        for f in self.oldFiles:
            self.idMap[f['id']] = f
        self.i = 0
        self.newFiles = []
        print
        print "Stage 1: Scanning volume"

    def accept(self, parent_id, name, stat_info, arc_flag, fullPath = None):
#        print fullPath, name
        fileInfo = FileInfo(name = name, fromStat = stat_info)
        if type(parent_id) == type(()):
            oldParentId = parent_id[1]
        else:
            oldParentId = parent_id

        match = self.fileApi.findByParentIdAndName(self.disk_id, oldParentId, name)
        if len(match) > 0:
            fi = FileInfo(fromDb = match[0])
            cmpr = fileInfo.compare(fi) 
            
            if not (cmpr & FileInfo.MATCH_TYPE):
                print "Type changed!"
                # If file type was changed, that's horrible
                self.newFiles.append((parent_id, name, stat_info, arc_flag, fullPath))
                self.i += 1
                return (int(self.i), -1)

            if cmpr == FileInfo.MATCH_ALL:
#                print match, " - perfect match"
                pass
            else:
                if self.debugLevel & DbUpdateDumper.DEBUG_STAGE_1:
                    print "!", `fileInfo`, `fi`, " - match:", cmpr
                sql = "UPDATE directory SET size=%d, mdate='%s' WHERE id=%d" % (fileInfo.size, fileInfo.mtime, match[0]['id'])
                if self.debugLevel & DbUpdateDumper.DEBUG_SQL:
                    print sql
                self.c.execute(sql)
            self.i += 1
            del self.idMap[match[0][0]]
            return (int(self.i), match[0][0])
        else:
            if self.debugLevel & DbUpdateDumper.DEBUG_STAGE_1:
                print "+", `fileInfo`
            self.newFiles.append((parent_id, name, stat_info, arc_flag, fullPath))
            self.i += 1
            return (int(self.i), -1)

    def finish(self):
        print
        print "Stage 2: Results of volume/DB scan"
        for f in self.newFiles:
            if self.debugLevel & DbUpdateDumper.DEBUG_STAGE_2:
                print "+", self.getInVoumePath(f[4])
        missingDirs = []
        for f in self.idMap.values():
            if self.debugLevel & DbUpdateDumper.DEBUG_STAGE_2:
                print "-", self.resolverApi.getFilePath(f["id"])
            recs = self.filenameMap.get(f['name'], [])
            recs.append(f)
            self.filenameMap[f['name']] = recs
            recs = self.sizeMap.get(f['size'], [])
            recs.append(f)
            self.sizeMap[f['size']] = recs
            if f['is_dir']:
                missingDirs.append(f)
        if self.debugLevel & DbUpdateDumper.DEBUG_STAGE_2:
            print "New files:", self.newFiles
            print "Missing by id:", self.idMap
            print "Missing by name:", self.filenameMap
            print "Missing by size:", self.sizeMap
            print "Missing directories:", missingDirs

        self.deletions = []
        self.additions = []
        self.updates = []
        
        
        print
        print "Stage 3: Matching files"
        for f in self.newFiles:
            if self.debugLevel & DbUpdateDumper.DEBUG_STAGE_3:
                print "Processing new:", f
            newFile = FileInfo(name = f[1], fromStat = f[2])

            # match for new file is found (i.e. the file was updated)
            matchFound = False

            if self.filenameMap.has_key(newFile.name):
                assert len(self.filenameMap[newFile.name]) == 1, "Only 1 match is supported"
                for match in self.filenameMap[newFile.name]: 
                    cmpr = newFile.compare(FileInfo(fromDb = match))
                    if self.debugLevel & DbUpdateDumper.DEBUG_STAGE_3:
                        print hex(cmpr), ":", match
                    assert cmpr & FileInfo.MATCH_TYPE, "Changing type is not supported"
                    if cmpr == FileInfo.MATCH_ALL:
                        self.reparent(f[4], newFile, match)
                        self.unsetByDbRec(match)
                        matchFound = True
                    elif cmpr & FileInfo.MATCH_SIZE == 0:
                        pass # if sizes don't match, it's not match at all
                    else:
                        assert False, "This match type is not supported"

            if not matchFound and not newFile.isDir and self.sizeMap.has_key(newFile.size):
                if self.debugLevel & DbUpdateDumper.DEBUG_STAGE_3:
                    print "Matches by size: ", self.sizeMap[newFile.size]
                perfectMatches = []
                imperfectMatches = []
                for match in self.sizeMap[newFile.size]: 
                    cmpr = newFile.compare(FileInfo(fromDb = match))
                    if self.debugLevel & DbUpdateDumper.DEBUG_STAGE_3:
                        print "match", hex(cmpr), ":", match
                    if cmpr & (FileInfo.MATCH_TYPE|FileInfo.MATCH_SIZE|FileInfo.MATCH_MTIME):
                        perfectMatches.append((cmpr, match))
                    elif cmpr & (FileInfo.MATCH_TYPE|FileInfo.MATCH_SIZE):
                        imperfectMatches.append((cmpr, match))
                    else:
                        assert False
                if self.debugLevel & DbUpdateDumper.DEBUG_STAGE_3:
                    print "Perfect matches:", perfectMatches
                    print "Imperfect matches:", imperfectMatches
                if len(perfectMatches) == 0 and len(imperfectMatches) == 0:
                    pass # no match at all
                if len(perfectMatches) == 1 and len(imperfectMatches) == 0:
                    match = perfectMatches[0][1]
                    self.reparent(f[4], newFile, match)
                    self.unsetByDbRec(match)
                    matchFound = True

                    if self.debugLevel & DbUpdateDumper.DEBUG_STAGE_3:
                        print "Missing by id:", self.idMap
                        print "Missing by name:", self.filenameMap
                        print "Missing by size:", self.sizeMap
                        print "Missing directories:", missingDirs
                else:
                    assert False, "More than one match not supported"

            if not matchFound:
                self.insertNew(f[4], newFile)
                    
        # idMap now has unclaimed files - this means, delete them
        fileIds = map(lambda f: f["id"], self.idMap.values())
	categoryApi = objects.Category.Category(self.connection)
        assert not categoryApi.isCategoriesAssignedToFiles(fileIds), "Files to delete have categories assigned"
        for f in self.idMap.values():
            self.deleteOld(f)

        print
        print "Stage 4: Final changes"
        for r in self.updates:
            print "! %s -> %s" % (r[0], r[1])
        for r in self.deletions:
            print "- %s" % (r)
        for r in self.additions:
            print "+ %s" % (r)


#        self.connection.rollback()
        DbDumper.finish(self)
    
    def unsetByDbRec(self, match):
        del self.idMap[match["id"]]
        l = self.filenameMap[match["name"]]
        l.remove(match)
        if len(l) > 0:
            self.filenameMap[match["name"]] = l
        else:
            del self.filenameMap[match["name"]]
        l = self.sizeMap[match["size"]]
        l.remove(match)
        if len(l) > 0:
            self.sizeMap[match["size"]] = l
        else:
            del self.sizeMap[match["size"]]
    
    def getInVoumePath(self, fsPath):
        volumePath = self.volume.volume_path
        if volumePath[-1] == "/": volumePath = volumePath[:-1]
        return fsPath[len(volumePath):]
    
    def reparent(self, fullPath, fileInfo, match):
        path = self.getInVoumePath(fullPath)

#        if fileRec["is_dir"]: path += "/"
        self.updates.append((
            self.resolverApi.getFilePath(match["id"]) + ["", "/"][match["is_dir"]], 
            path + ["", "/"][fileInfo.isDir]
        ))

        dir = self.resolverApi.getIdByPath(self.disk_id, os.path.dirname(path))
        sql = "UPDATE directory SET parent=%d, name=%s, size=%d, mdate='%s' WHERE id=%d" % (dir[0]['id'], DbConn.quote(fileInfo.name), fileInfo.size, fileInfo.mtime, match['id'])
        if self.debugLevel & DbUpdateDumper.DEBUG_SQL:
            print sql
        self.c.execute(sql)
        
    def insertNew(self, fullPath, fileInfo):
        path = self.getInVoumePath(fullPath)
        self.additions.append(path)
        dir = self.resolverApi.getIdByPath(self.disk_id, os.path.dirname(path))
        sql = """
            INSERT INTO directory(snapshot, no, parent, name, extension, size, is_dir, arc_status, mdate)
            VALUES (%d, %d, %s, %s, %s, %d, %d, %d, '%s')
        """ % (self.disk_id, 0, dir[0]["id"], DbConn.quote(fileInfo.name), DbConn.quote(self.getExt(fileInfo.name)), 
               fileInfo.size, fileInfo.isDir, 0, fileInfo.mtime)
        if self.debugLevel & DbUpdateDumper.DEBUG_SQL:
            print sql
        self.c.execute(sql)
        
    def deleteOld(self, fileRec):
        path = self.resolverApi.getFilePath(fileRec["id"])
        if fileRec["is_dir"]: path += "/"
        self.deletions.append(path)
        sql = "DELETE FROM directory WHERE id=%d" % fileRec["id"]
        if self.debugLevel & DbUpdateDumper.DEBUG_SQL:
            print sql
        self.c.execute(sql)
    

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
        dumper = DbDumper(self.conn, id, self)
        volume.enumerateFiles(dumper)
        return dumper.getStats()

    def updateDisk(self, volume, id, debugLevel):
        dumper = DbUpdateDumper(self.conn, id, self, debugLevel)
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

    def rollback(self):
        self.conn.rollback()

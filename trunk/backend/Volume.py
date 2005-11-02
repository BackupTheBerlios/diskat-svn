import string
import os
import stat
import VolumeInfo
import Archivers
import Const
import IFileInfoAcceptor
import IVolumeEnumerator
import GenericCommandLineArchiver

def _path_join(a, b):
    if a[-1] == "/": a = a[:-1]
    if b[0] == "/":  b = b[1:]
    return a + "/" + b

class Volume(IVolumeEnumerator.IVolumeEnumerator):

    volume_path = ""
    drive_letter = ''
    recurseArchives = 1

    def __init__(self, volume_path):
        assert len(volume_path) >= 2
        assert volume_path[1] == ':'
        volume_path = volume_path.replace("\\", "/")
        self.volume_path = volume_path
        if self.volume_path[-1] == "/": self.volume_path = self.volume_path[:-1]
        self.drive_letter = volume_path[0]
        self.vol_info = VolumeInfo.VolumeInfo(self.drive_letter + ":\\")
        self.recurseArchives = 1
#        os.path.join = _path_join

    def __repr__(self):
        return "<Volume root=%s>" % self.getRoot()
    
    def getSerialNumber(self):
        return self.vol_info.getSerialNum()

    def getLabel(self):
        return self.vol_info.getLabel()

    def getRoot(self):
        return self.volume_path

    def setRecurseArchives(self, flag):
        self.recurseArchives = flag
    
    def enumerateFiles(self, accept_object):
        accept_object.setVolume(self)
        root_stat = [0] * 10
        root_stat[stat.ST_MODE] = stat.S_IFDIR
        root_id = accept_object.accept(0, "/", root_stat, Const.ARC_NONE)
#        self._enumerateFiles(accept_object, self.drive_letter + ":", "/", root_id)
        self._enumerateFiles(accept_object, self.volume_path, "/", root_id)
        accept_object.finish()
        accept_object.setVolume(None)

    def _enumerateFiles(self, accept_object, vol_path, root_path, root_id):
        names = os.listdir(_path_join(vol_path, root_path))
        names.sort()
        for name in names:
            full_path = _path_join(vol_path, _path_join(root_path, name))
            try:
                st = os.stat(full_path)
            except OSError:
                print "Warning: Cannot stat " + full_path + " - will appear as empty file"
                st = Const.VIRTUAL_FILE_STAT
            arc_flag = Const.ARC_NONE
            is_sfx = 0

            if self.recurseArchives and not stat.S_ISDIR(st[stat.ST_MODE]):
                if Archivers.getArchiver(name): 
                    arc_flag = Const.ARC_IS_ARCHIVE
                elif Archivers.isSFX(name, st): 
                    arc_flag = Const.ARC_IS_ARCHIVE
                    is_sfx = 1

            current_id = accept_object.accept(root_id, name, st, arc_flag, fullPath = full_path)

            if stat.S_ISDIR(st[stat.ST_MODE]):
                self._enumerateFiles(accept_object, vol_path, _path_join(root_path, name), current_id)
            elif arc_flag != Const.ARC_NONE:
                if is_sfx: arc_flag = Const._ARC_IS_SFX
                archive_enum = GenericCommandLineArchiver.GenericCommandLineArchiver(string.replace(root_path, "\\", "/") + "/" + name, full_path, current_id, arc_flag)
                if archive_enum.enumerateFiles(accept_object) == 0:
                    accept_object.updateArchiveFlag(current_id, Const.ARC_NONE)
                archive_enum.close()

if __name__ == '__main__':
    class FooAcceptor(IFileInfoAcceptor.IFileInfoAcceptor):
        def accept(self, path, name, st, arc_flag):
            print path, name, st, arc_flag
    a = Volume("d:")
    a.enumerateFiles(FooAcceptor())
    a.close()

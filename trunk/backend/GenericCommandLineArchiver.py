import os
import re
import string
import stat
import IVolumeEnumerator
import Const
import Archivers
import diskat_config

class GenericCommandLineArchiver(IVolumeEnumerator.IVolumeEnumerator):

    repr_name = ""
    filename = ""
    root_id = 0
    dir_map = {}
    arc_flag = 0

    def __init__(self, repr_name, filename, root_id, arc_flag):
        self.repr_name = repr_name
        self.filename = filename
        self.root_id = root_id
        self.arc_flag = arc_flag
        self.dir_map = {}

    def open(self, filename):
        self.archive_name = filename

    def close(self):
        pass

    def enumerateFiles(self, accept_object):
        if self.arc_flag == Const._ARC_IS_SFX:
            numFiles = 0
            for archiverType in diskat_config.archive_sfx_use_archivers:
                archiver = diskat_config.archiver_type[archiverType]
                f = os.popen(archiver["command"] % self.filename, "r")
                numFiles = self.parseListing(f, accept_object, archiver)
                if numFiles > 0: break
            return numFiles
        else:
            archiver = Archivers.getArchiver(self.filename)
            f = os.popen(archiver["command"] % self.filename, "r")
            return self.parseListing(f, accept_object, archiver)

    def parseListing(self, file, accept_object, archiver):
        do_parse = 0
        numFiles = 0
        while 1:
            l = file.readline()
            if not l: break
            l = l[:-1]
            if do_parse:
                if re.match(archiver["end_pattern"], l): 
                    do_parse = 0
                else:
                    m = re.match(archiver["parse_pattern"], l)
                    if m:
                        props = m.groupdict()
                        name = string.strip(props["name"])
		        name = string.replace(name, "\\", "/")
		        # Convert cp866=>cp1251 (OEM=>ANSI)
		        try:
		            name = unicode(name, "cp866").encode("cp1251")
		        except UnicodeError:
		            # Their may be other encoding or plain garbage,
		            # leave name as is
		            pass

                        st = [0] * 10
                        try:
                            st[stat.ST_SIZE] = int(props["size"])
                        except:
                            print props
                            raise
                        if props.has_key("attr"):
                            if props["attr"][0] == 'D': st[stat.ST_MODE] = stat.S_IFDIR

                        self.acceptHelper(accept_object, name, st, Const.ARC_IN_ARCHIVE)
                        numFiles = numFiles + 1
            else:
                if re.match(archiver["start_pattern"], l): do_parse = 1

        return numFiles

    def acceptHelper(self, accept_object, name, st, flags):
        path_parts = string.split(name, "/")

        cur_parent = self.root_id
        cur_dir    = self.dir_map

        # Traverse our directory structure cache to find out what will be the parent of
        # current item, creating intermediate directories if needed.
        for path_el in path_parts[:-1]:
            if not cur_dir.has_key(path_el):
                id = accept_object.accept(cur_parent, path_el, Const.VIRTUAL_DIR_STAT, flags)
                cur_dir[path_el] = (id, {})
                cur_parent = id
            else:
                cur_parent = cur_dir[path_el][0]
            cur_dir = cur_dir[path_el][1]

        # Finally, add the item
        id = accept_object.accept(cur_parent, path_parts[-1], st, flags)

        # Finally, if it was a directory, add it to the map - or
        # else we will want to create it in the loop above next time
        if (stat.S_ISDIR(st[stat.ST_MODE])):
            if not cur_dir.has_key(path_parts[-1]):
                cur_dir[path_parts[-1]] = (id, {})


if __name__ == '__main__':
    class FooAcceptor:
        i = 100
        def accept(self, parent_is, name, st, arc_flag):
            print parent_is, name, st, arc_flag
            self.i = self.i + 1
            return self.i
    a = GenericCommandLineArchiver("xmldbm.zip", "C:/projects/xmldbm.zip ", 1)
    a.enumerateFiles(FooAcceptor())
    a.close()

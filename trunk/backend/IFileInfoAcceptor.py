class IFileInfoAcceptor:
    "Acceptor interface for receiving file information during volume enumeration"

    def accept(self, parentId, name, statInfo, arcFlag, fullPath = None):
        """
        Record next file.
        @param parentId ID of parent of this file (previously returned by very this method, or 0 for root)
        @param name Name of file
        @param statInfo Info for the file, in format of stat.stat()
        @param arcFlag Archive flag for the file, ARC_*
        @param fullPath Full path of file, optional (enumerator should pass this if it can)
        @return File ID
        """
        pass

    def updateArchiveFlag(self, id, arcFlag):
        """
        Update archive flag for previously recorded file.
        @param id ID of file (previously returned by accept())
        @param arcFlag Archive flag for the file, ARC_*
        """
        pass

    def finish(self):
        """
        Called when all files have been enumerated.
        """
        pass

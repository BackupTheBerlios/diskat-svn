class IVolumeEnumerator:
    "Inteface for enumerating a volume"

    def open(url):
        "Open volume identified by url"
        pass

    def enumerateFiles(self, accept_object):
        """
        Enumerate files in volume, by passing them to accept_object
        @type accept_object IFileInfoAcceptor
        """
        pass

    def close(filename):
        "Close volume identified by url"
        pass

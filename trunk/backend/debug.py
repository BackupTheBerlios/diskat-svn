class InfoDumper(IFileInfoAcceptor.IFileInfoAcceptor): 
    def accept(self, path, name, stat_info):
        print path, name, hex(stat_info[stat.ST_MODE])

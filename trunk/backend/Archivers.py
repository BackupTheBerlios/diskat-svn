import diskat_config
import stat
import re

def getArchiver(filename):
    for pat in diskat_config.archivers.keys():
        if re.match(pat, filename, re.IGNORECASE): 
            return diskat_config.archiver_type[diskat_config.archivers[pat]]
    return None

def isSFX(filename, statInfo):
    if re.match(diskat_config.archive_sfx_pattern, filename, re.IGNORECASE): 
        if (statInfo[stat.ST_SIZE] > diskat_config.archive_sfx_size_threshold):
            return 1
    return 0


if __name__ == '__main__':
    import sys, os
    print isArchive(sys.argv[1])
    print isSFX(sys.argv[1], os.stat(sys.argv[1]))

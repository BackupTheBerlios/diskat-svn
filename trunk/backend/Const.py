import stat

# Archive type flags
ARC_NONE	= 0
ARC_IS_ARCHIVE	= 1
ARC_IN_ARCHIVE	= 2
_ARC_IS_SFX	= 3 # Internal only, ARC_IS_ARCHIVE stored in DB

# Stat structure for a directory
VIRTUAL_DIR_STAT = [0] * 10
VIRTUAL_DIR_STAT[stat.ST_MODE] = stat.S_IFDIR
VIRTUAL_FILE_STAT = [0] * 10

dbname = "C:/projects/diskat/diskat.db"

archiver_type = {}

archiver_type["InfoZIP"] = {
  "command": 'unzip -l "%s"',
  "start_pattern": r'^ ----',
  "parse_pattern": r'^\s+(?P<size>.+?)\s+(?P<date>.+?)\s+(?P<time>.+?)\s+(?P<name>.+?)\s*$',
  "end_pattern": r'^ ----',
}

archiver_type["7-Zip"] = {
  "command": 'C:/misc/arc/7-Zip/7z.exe l "%s"',
  "start_pattern": r'^----',
  "parse_pattern": r'^(?P<date>.+?)\s+(?P<time>.+?)\s+(?P<attr>.+?)\s+(?P<size>.+?)\s+(?P<compr_size>.+?)\s+(?P<name>.+)$',
  "end_pattern": r'^----',
}

archivers = {
    r'.+\.(zip|rar)$': "7-Zip"
}


archive_sfx_pattern = r'.+\.(exe)$'
archive_sfx_size_threshold = 100000
archive_sfx_use_archivers = ["InfoZIP"]

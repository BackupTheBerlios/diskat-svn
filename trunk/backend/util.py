def oem2ansi(s):
    return unicode(s, "cp866").encode("cp1251")

import string
from ctypes import *

GetVolumeInformation = windll.kernel32.GetVolumeInformationA

class VolumeInfo:

    def __init__(self, path):
        self.name_buf = c_buffer(32)
        self.ser_num = c_int()
        max_comp_len = c_int()
        fs_flags = c_int()
        self.fs_name_buf = c_buffer(32)

        GetVolumeInformation(path, byref(self.name_buf), 32, byref(self.ser_num), byref(max_comp_len), byref(fs_flags), byref(self.fs_name_buf), len(self.fs_name_buf))

    def getLabel(self):
        return string.strip(string.replace(self.name_buf.raw, "\0", ""))

    def getSerialNum(self):
        return "%08X" % self.ser_num.value





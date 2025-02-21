import typing
from littlefs import LittleFS, UserContext
from gba_mpy_tools.errors import ROMInvalidError, LFSNotFormatedError

if typing.TYPE_CHECKING:
    from os import PathLike
# ref: https://github.com/devkitPro/gba-tools/blob/master/src/gbafix.c
MAGIC_BLOCK_SIZE                                = 0x67452301
MAGIC_BLOCK_COUNT                               = 0xEFCDAB89

class GBAMicroPythonRom():
    def __init__(self):
        self.__rom = b""
        self.__romfs_offset = -1
        self.__romfs_capacity = -1
        self.__romfs_bsize = -1
        self.__romfs_bcount = -1
        self.__uctx = UserContext(0)
        self.__lfs = LittleFS()
    
    @property
    def fs(self):
        return self.__lfs
    
    @property
    def is_valid(self):
        return self.__romfs_capacity > 0
    
    @property
    def fs_block_size(self):
        return self.__romfs_bsize if (self.__romfs_bsize > 0 and self.__romfs_bsize != MAGIC_BLOCK_SIZE) else -1
    
    @property
    def fs_block_count(self):
        return self.__romfs_bcount if (self.__romfs_bcount > 0 and self.__romfs_bcount != MAGIC_BLOCK_COUNT) else -1
    
    def mkfs(self, block_size: int, block_count: int = -1):
        if not self.is_valid:
            raise ROMInvalidError()
        if block_count < 0:
            block_count = self.__romfs_capacity // block_size
        self.__romfs_bsize = block_size
        self.__romfs_bcount = block_count
        self.__uctx = UserContext(self.__romfs_capacity)
        self.__lfs = LittleFS(self.__uctx, False, block_size = block_size, block_count = block_count)
        assert self.__lfs.format() == 0
        assert self.__lfs.mount() == 0
    
    @staticmethod
    def load(path: 'PathLike'):
        nrom = GBAMicroPythonRom()
        # load ROM
        with open(path, "rb") as f:
            nrom.__rom = f.read()
        # search for location
        # the pos is aligned to 8, so it is easy
        s_pos = 0
        while s_pos + 8 <= len(nrom.__rom):
            chunk = nrom.__rom[s_pos: s_pos + 8]
            if chunk == b"GBABDEV\0":
                nrom.__romfs_offset = s_pos
                break
            s_pos += 8
        if nrom.__romfs_offset <= 0:
            # not a mpy ROM
            return nrom
        s_pos = nrom.__romfs_offset
        nrom.__romfs_bsize = int.from_bytes(nrom.__rom[s_pos + 8: s_pos + 12], "little")
        nrom.__romfs_bcount = int.from_bytes(nrom.__rom[s_pos + 12: s_pos + 16], "little")
        nrom.__romfs_capacity = int.from_bytes(nrom.__rom[s_pos + 16: s_pos + 20], "little")
        # check last tag
        end = s_pos + 20 + nrom.__romfs_capacity
        chunk = nrom.__rom[end: end + 8]
        if chunk != b"BDEVGBA\0":
            # make it invalid
            nrom = GBAMicroPythonRom()
            return nrom
        return nrom

    def save(self, path: 'PathLike'):
        if not self.is_valid:
            raise ROMInvalidError()
        if len(self.__uctx.buffer) <= 0 or self.fs_block_size < 0 or self.fs_block_count < 0:
            raise LFSNotFormatedError()
        assert self.__romfs_capacity == len(self.__uctx.buffer)
        # modify ROM
        p = self.__romfs_offset
        data = bytearray(self.__rom)
        data[p + 8: p + 12] = self.fs_block_size.to_bytes(4, "little")
        data[p + 12: p + 16] = self.fs_block_count.to_bytes(4, "little")
        fs_end = p + 20 + self.__romfs_capacity
        data[p + 20 : fs_end] = self.__uctx.buffer
        # write ROM
        with open(path, "wb") as f:
            f.write(data)
    
    def __repr__(self):
        return f"<GBAMicropythonRom block_size={self.fs_block_size} block_count={self.fs_block_count} capacity={self.__romfs_capacity}>"
from gba_mpy_tools.config import Config
from gba_mpy_tools.errors import GBAEmulatorNotFoundError, FileNotFoundError
from pathlib import Path
from subprocess import run
from shutil import which

class GBAEmulator():
    def __init__(self, cfg: Config):
        self.__cfg = cfg
        self.__emu = ""
        # check path
        mpath = cfg.gba_emulator
        if mpath.exists() and mpath.is_file():
            self.__emu = str(mpath.resolve())
        else:
            # search for emulator in default PATH
            result = which(str(cfg.gba_emulator))
            if result:
                self.__emu = result
    
    def __ensure_gba_emulator(self):
        if self.__emu == "":
            raise GBAEmulatorNotFoundError()
    
    def run(self, gba_rom: str | Path):
        """Run the GBA ROM with emulator.

        Args:
            gba_rom (str | Path): The GBA ROM file.
        """
        self.__ensure_gba_emulator()
        if not isinstance(gba_rom, Path):
            gba_rom = Path(gba_rom)
        if not gba_rom.exists():
            raise FileNotFoundError()
        cmd = [ self.__emu ]
        cmd.extend(self.__cfg.gba_params)
        cmd.append(gba_rom)
        p = run(cmd)

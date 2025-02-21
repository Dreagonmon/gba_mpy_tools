from gba_mpy_tools.config import Config
from gba_mpy_tools.rom import GBAMicroPythonRom
from gba_mpy_tools.wrap_mpy_cross import MpyCross
from gba_mpy_tools.wrap_gba_emulator import GBAEmulator
from pathlib import Path, PurePosixPath
from typing import NamedTuple

class FileItemPair(NamedTuple):
    source: Path
    target: PurePosixPath
    is_dir: bool
    compile: bool

def __deal_file_with_config(file: Path, cfg: Config):
    target = cfg.to_target_path(file)
    should_compile = False
    if cfg.mpy_cross_compile and target.suffix.lower() == ".py" and (not cfg.should_ignore_mpy_cross_compile(file)):
        target = target.with_suffix(".mpy")
        should_compile = True
    return FileItemPair(file, target, False, should_compile)

def __walk_dir_with_config(dir: Path, cfg: Config) -> list[FileItemPair]:
    if dir.is_dir():
        result = [FileItemPair(dir, cfg.to_target_path(dir), True, False)]
        # list current dir
        for fp in dir.iterdir():
            if cfg.should_ignore_project_file(fp):
                continue
            if fp.is_dir():
                result.extend(__walk_dir_with_config(fp, cfg))
            else:
                result.append(__deal_file_with_config(fp, cfg))
        return result
    else:
        return [ __deal_file_with_config(dir, cfg) ]

def list_files(cfg: Config):
    """List all the files that will be write into the ROM.

    Args:
        cfg (Config): Config info object.
    
    Returns:
        list[FileItemPair]: File list
    """
    return __walk_dir_with_config(cfg.project_source_dir, cfg)

def build(cfg: Config):
    """Build the ROM with files.

    Args:
        cfg (Config): Config info object.
    """
    file_list = list_files(cfg)
    rom = GBAMicroPythonRom.load(cfg.gba_template)
    rom.mkfs(512)
    mpy_cross = MpyCross(cfg)
    for item in file_list:
        if item.is_dir:
            rom.fs.makedirs(str(item.target), exist_ok=True)
        else:
            if item.compile:
                content = mpy_cross.compile(item.source)
            else:
                with open(item.source, "rb") as f:
                    content = f.read()
            with rom.fs.open(str(item.target), "wb") as f:
                f.write(content)
    rom.save(cfg.gba_output)

def run(cfg: Config):
    """Build GBA ROM and run with emulator

    Args:
        cfg (Config): Config info object.
    """
    build(cfg)
    gba_emu = GBAEmulator(cfg)
    gba_emu.run(cfg.gba_output)

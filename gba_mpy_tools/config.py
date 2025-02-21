from pathlib import Path, PurePosixPath
from typing import TypedDict, NotRequired
from tomllib import load as load_toml
from shlex import split as sh_split

DEFAULT_CONFIG_FILENAME = ".gbampy.toml"

ProjectSectionDict = TypedDict("ProjectSection", {
    "source_dir": NotRequired[str],
    "target_dir": NotRequired[str],
    "ignore-pattern": NotRequired[list[str]],
})
MpyCorssSectionDict = TypedDict("MpyCorssSection", {
    "compile": NotRequired[bool],
    "path": NotRequired[str],
    "params": NotRequired[str],
    "ignore-pattern": NotRequired[list[str]],
})
GBASectionDict = TypedDict("ProjectSection", {
    "template": NotRequired[str],
    "output": NotRequired[str],
    "emulator": NotRequired[str],
    "params": NotRequired[str],
})
ConfigDict = TypedDict("ConfigDict",{
    "project": NotRequired[ProjectSectionDict],
    "mpy-cross": NotRequired[MpyCorssSectionDict],
    "gba": NotRequired[GBASectionDict],
})

class Config():
    def __init__(self, config_file_or_dir: str | Path = "."):
        self.__cfg: ConfigDict = dict()
        temp_path = Path(config_file_or_dir)
        if temp_path.exists() and temp_path.is_dir():
            config_path = temp_path.joinpath(DEFAULT_CONFIG_FILENAME)
            self.__cfgdir = temp_path
        else:
            config_path = temp_path
            self.__cfgdir = temp_path.parent
        if config_path.exists() and config_path.is_file():
            # load config
            with open(config_path, "rb") as stream:
                self.__cfg = load_toml(stream)
    
    def replace_config(self, cfg: ConfigDict):
        self.__cfg = cfg

    def to_target_path(self, source_file: str | Path):
        if not isinstance(source_file, Path):
            source_file = Path(source_file)
        rel = source_file.relative_to(self.project_source_dir)
        return self.project_target_dir.joinpath(rel)
    
    def should_ignore_project_file(self, source_file: str | Path | PurePosixPath):
        if isinstance(source_file, (str, Path, )):
            source_file = self.to_target_path(source_file)
        source_file = source_file.relative_to(self.project_target_dir) # use rel path to match
        for pattern in self.project_ignore_pattern:
            if source_file.full_match(pattern):
                return True
        return False

    def should_ignore_mpy_cross_compile(self, source_file: str | Path | PurePosixPath):
        if isinstance(source_file, (str, Path, )):
            source_file = self.to_target_path(source_file)
        source_file = source_file.relative_to(self.project_target_dir) # use rel path to match
        for pattern in self.mpy_cross_ignore_pattern:
            if source_file.full_match(pattern):
                return True
        return False

    @property
    def config_file_dir(self):
        return self.__cfgdir
    
    @property
    def project_source_dir(self):
        prj: ProjectSectionDict = self.__cfg.setdefault("project", dict())
        return Path(prj.setdefault("source_dir", ".")).resolve()
    
    @property
    def project_target_dir(self):
        prj: ProjectSectionDict = self.__cfg.setdefault("project", dict())
        return PurePosixPath("/").joinpath(prj.setdefault("target_dir", "."))
    
    @property
    def project_ignore_pattern(self) -> list[str]:
        prj: ProjectSectionDict = self.__cfg.setdefault("project", dict())
        return prj.setdefault("ignore-pattern", [])
    
    @property
    def mpy_cross_compile(self):
        mpyc: MpyCorssSectionDict = self.__cfg.setdefault("mpy-cross", dict())
        return mpyc.setdefault("compile", False)

    @property
    def mpy_cross_path(self):
        mpyc: MpyCorssSectionDict = self.__cfg.setdefault("mpy-cross", dict())
        return Path(mpyc.setdefault("path", "."))
    
    @property
    def mpy_cross_params(self):
        mpyc: MpyCorssSectionDict = self.__cfg.setdefault("mpy-cross", dict())
        return sh_split(mpyc.setdefault("params", ""))
    
    @property
    def mpy_cross_ignore_pattern(self) -> list[str]:
        mpyc: MpyCorssSectionDict = self.__cfg.setdefault("mpy-cross", dict())
        return mpyc.setdefault("ignore-pattern", [])

    @property
    def gba_template(self):
        gba: GBASectionDict = self.__cfg.setdefault("gba", dict())
        return Path(gba.setdefault("template", "."))

    @property
    def gba_output(self):
        gba: GBASectionDict = self.__cfg.setdefault("gba", dict())
        return Path(gba.setdefault("output", "."))

    @property
    def gba_emulator(self):
        gba: GBASectionDict = self.__cfg.setdefault("gba", dict())
        return Path(gba.setdefault("emulator", "."))

    @property
    def gba_params(self):
        gba: GBASectionDict = self.__cfg.setdefault("gba", dict())
        return sh_split(gba.setdefault("params", ""))

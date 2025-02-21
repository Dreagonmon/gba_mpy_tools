from gba_mpy_tools.config import Config
from gba_mpy_tools.errors import MpyCrossNotFoundError, FileNotFoundError, CompileError
from tempfile import NamedTemporaryFile
from pathlib import Path
from subprocess import run, DEVNULL, PIPE
from shutil import which

class MpyCross():
    def __init__(self, cfg: Config):
        self.__cfg = cfg
        self.__mc = ""
        # check mpy_cross
        mpath = cfg.mpy_cross_path
        if mpath.exists() and mpath.is_file():
            self.__mc = mpath
        if self.__mc == "":
            # search for mpy-cross in default PATH
            result = which("mpy-cross")
            if result:
                self.__mc = result
        if self.__mc == "":
            # get from the mpy_cross module
            from mpy_cross import mpy_cross
            self.__mc = str(Path(mpy_cross).resolve())
    
    def __ensure_mpy_cross(self):
        if self.__mc == "":
            raise MpyCrossNotFoundError()
    
    def compile(self, source: str | Path):
        """Compile a mpy script, return compiled content.

        Args:
            source (str | Path): The source file.

        Returns:
            bytes: .mpy file content.
        """
        self.__ensure_mpy_cross()
        if not isinstance(source, Path):
            source = Path(source)
        if not source.exists():
            raise FileNotFoundError()
        with NamedTemporaryFile(delete_on_close=False, suffix=".mpy") as f:
            fpath = f.name
            # close it allow mpy-cross to write
            f.close()
            cmd = [ self.__mc ]
            cmd.extend(self.__cfg.mpy_cross_params)
            cmd.extend([ "-o", fpath ])
            cmd.extend([ "-s", source.name ])
            cmd.append(source)
            p = run(cmd, stdin=DEVNULL, stdout=PIPE, stderr=PIPE, text=True, encoding="utf-8")
            if p.returncode != 0:
                raise CompileError(source, p.stderr)
            # read file
            with open(fpath, "rb") as compiled_file:
                data = compiled_file.read()
            # return it
            return data

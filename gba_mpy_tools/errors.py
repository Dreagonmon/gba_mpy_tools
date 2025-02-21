from pathlib import Path

class MpyCrossNotFoundError(Exception):
    def __init__(self):
        super().__init__("'mpy-cross' not found, please make sure it is in your PATH.")

class GBAEmulatorNotFoundError(Exception):
    def __init__(self, program: str):
        super().__init__(f"GBA emulator '{program}' not found.")

class FileNotFoundError(Exception):
    def __init__(self, file: str | Path):
        super().__init__(f"File '{str(file)}' is not exist.")

class CompileError(Exception):
    def __init__(self, source: str | Path, message: str):
        super().__init__(f"Failed to compile: {str(source)}\nCompiling output:\n{message}")

class ROMInvalidError(Exception):
    def __init__(self):
        super().__init__("Micropython ROM for GBA is invalid")

class LFSNotFormatedError(Exception):
    def __init__(self):
        super().__init__("The LittleFS file system in the ROM is not formated")

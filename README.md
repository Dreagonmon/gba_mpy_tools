# GBA MicroPython Tools

## install

```bash
# clone this repo
git clone ...
# install with pip, and install it to user dir
pip install -e .
# or if your python can't install the global dependence, using pipx
pipx install -e .
# the "-e" is optional, but since this is the very early version, much more development is needed, "-e" helps a lot.
```

## Useage
1. Create the config file in the project workspace. `.gbampy.toml`
2. Create the config file for local environment (higher priority). `.gbampy.local.toml`
3. Run `gbampy build` to build the ROM.
4. Run `gbampy run` to build and run the ROM, testing your game.

## Config file
```toml
[project]
source_dir = "/path/to/src/dir"                   # source code dir
target_dir = "/"                                  # path in the ROM, normally "/"
ignore_pattern = [
    "**/__pycache__",                             # python cache files
    "**/.*",                                      # hidden files
    "**/*.gba",                                   # gba files
    "**/*.sav",                                   # sav files
    "**/*.sgm",                                   # sgm files
    "**/*.ss?",                                   # ss1, ss2, ss3, ..., ss9 files
]
before_build = ""                                 # python module and function to be execute before build, "build.script.module:func_name"
after_build = ""                                  # python module and function to be execute after build, "build.script.module:func_name"

[mpy-cross]
compile = true                                    # compile code with mpy-cross
path = "/run/media/dreagonmon/Data/Code/Python/gba_mpy_tools/.venv/bin/mpy-cross"
params = "-O2 -X emit=bytecode"                   # params passed to mpy-cross
ignore_pattern = [
    "boot.py",                                    # keep entry file as .py
    "main.py",                                    # keep entry file as .py
]

[gba]
template = "/path/to/template/micropython.gba"    # the micropython.gba template ROM
output = "/path/to/output/game_name.gba"          # the output ROM
emulator = "mgba-qt"                              # mgba emulator
params = "-l 23"                                  # params passed to mgba
```

## Build
```bash
python -m pip install build
python -m build
```

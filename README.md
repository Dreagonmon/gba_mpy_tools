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
2. Run `gbampy build` to build the ROM
3. Run `gbampy run` to build and run the ROM, testing your game.

## Config file
```toml
[project]
source_dir = "/path/to/src/dir"                   # source code dir
target_dir = "/"                                  # path in the ROM, normally "/"
ignore-pattern = [
    "**/__pycache__",                             # python cache files
    "**/.*",                                      # hidden files
]

[mpy-cross]
compile = true                                    # compile code with mpy-cross
path = "/run/media/dreagonmon/Data/Code/Python/gba_mpy_tools/.venv/bin/mpy-cross"
params = "-O2 -X emit=bytecode"                   # params passed to mpy-cross
ignore-pattern = [
    "boot.py",                                    # keep entry file as .py
    "main.py",                                    # keep entry file as .py
]

[gba]
template = "/path/to/template/micropython.gba"    # the micropython.gba template ROM
output = "/path/to/output/game_name.gba"          # the output ROM
emulator = "mgba-qt"                              # mgba emulator
params = "-l 255"                                 # params passed to mgba
```
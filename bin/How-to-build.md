## How to build pyxelTetris.py?

1. Install requirements:
```bash
sudo pip3 install -U nuitka zstandard patchelf orderedset
```
2. exec this:
```bash
nuitka3 --standalone --onefile --windows-disable-console --static-libpython=no --include-data-dir=assets=tetris.pyxres pyxelTetris.py
```

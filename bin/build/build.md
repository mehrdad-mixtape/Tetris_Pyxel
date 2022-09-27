### I built bin-files on Debian, Make venv, install pkgs and build it that reduce the size of pkgs
#### Install python3.10-dev
- I have python3.8 on my system (If you have python3.10 skip 1, 2)
    1. sudo update-alternatives --set python3 /usr/bin/python3.8
    2. sudo apt install --reinstall python3-apt
    3. sudo add-apt-repository ppa:deadsnakes/ppa
    4. sudo apt install python3.10-dbg python3.10-distutils python3.10-dev python3.10-full python3.10-gdbm python3.10-gdbm-dbg python3.10-lib2to3 python3.10-venv ccache

- sudo update-alternatives --set python3 /usr/bin/python3.10
- source env/bin/activate
- (env) pip3 install -U nuitka zstandard pyxel==1.8.5 ordered-set patchelf

#### Building
- (env) nuitka3 --standalone --windows-disable-console --include-data-dir=path/to/Tetris_Pyxel/assets=tetris.pyxres --python-flag=-O pyxelTetris.py

## Don't do it on venv!
### I built bin-files on Debian
```bash
sudo update-alternatives --set python3 /usr/bin/python3.8
sudo apt install --reinstall python3-apt
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.10-dev -y

sudo update-alternatives --set python3 /usr/bin/python3.10
sudo python3.10 -m pip install -U nuitka zstandard pyxel==1.8.5 ordered-set patchelf

nuitka3 --standalone --windows-disable-console --include-data-dir=path/to/Tetris_Pyxel/assets=tetris.pyxres --python-flag=-O pyxelTetris.py
```
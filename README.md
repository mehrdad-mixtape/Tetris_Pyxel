# Tetris Pyxel
- An other Tetris With `Python` + `Pyxel`, Let's Play!
- Programming Language: (Python3.10)
- Retro Game Engine **[Pyxel](https://github.com/kitao/pyxel)**

## Interview:
![image](https://github.com/mehrdad-mixtape/Tetris_Pyxel/blob/master/images/index.gif)

## Platforms:
- Linux (Absolutely worked)
- Windows (I didn't test)
- Mac (I didn't test)

## Python version:
- 3.10 or higher

## How to Play?
### Bin file: (Linux)
- step 1: requierments
	1. 
    ```bash
	sudo apt install g++ build-essential libc6 libc6-dev
	```
1. Go to the `./bin/build/`
2. Run `pyxelTetris`

### Directly:
1. Install [pyxel](https://github.com/kitao/pyxel) version **1.9.7** 
    ```bash
    pip3 install pyxel==1.9.7
    ```
2. Enjoy!
    - Run:
    ```bash
    python3 pyxelTetris.py
    ```
    OR
    ```bash
    python pyxelTetris.py
    ```
### WebAssembly: Help you to play game on every platform.
- Notice!
    1. **Chrome FireFox** Are Best Choice For Phones
    2. **FireFox Chrome Brave** Are Best Choice For LapTop Or PCs
    - PCs:
        1. Go to `./wasm` directory
        2. Connect your system to your local network
            - Find IP-ADDRESS of your system
                - Linux:
                ```bash
                $ ifconfig

                OR

                $ ip addr show
                ```
                - Windows:
                ```bash
                $ ipconfig
                ```
        3. Run ***run-game-server.py*** On Terminal Or Cmd Or PowerShell Or WSL Or etc ...
            ```bash
            $ python3 or python run-game-server.py --addr 192.168.x.x --port 8080
            ```
        4. Open Your Browser & Go to URL --> http://ADDR:8080 & Wait For Seconds
        5. Game Will Be Start On Your Browser!

    - Phones: I Recommend **UserLand** (linux on android):
        1. Enable your ***data-network-connection*** and ***HotSpot*** network.
        2. Install **UserLand** and setup your linux distribution (I recommend install **debian without Gui**)
        3. Install this packages
        ```bash
        sudo apt install curl git vim net-tools python3
        ```
        4. Find your IP-ADDRESS (looking for **wlan** interface)
        ```bash
        ifconfig
        [...]
        wlan1 [...] 192.168.x.x [...]
        [...]

        OR

        ip addr show
        [...]
        wlan1 [...] 192.168.x.x [...]
        [...]
        ```
        5. Clone my repo
        ```bash
        git clone https://github.com/mehrdad-mixtape/Tetris_Pyxel
        ```
        6. Go to `./Tetris_Pyxel/wasm/`
        ```bash
        cd Tetris_Pyxel/wasm/
        ```
        7. Run the source code of **run-game-server.py**
        ```bash
        python3 run-game-server.py --addr 192.168.x.x --port 8080
        ```
        8. Open Your ***Chrome Browser*** & Go to URL --> http://ADDR:8080 & Wait For Seconds
        9. Game Will Be Start On Your Browser!

## Issus:
I fixed many `Critical Bugs`, But maybe ... :)
- I made the first version in ***3 days*** on my free time! Just for Fun with (Pyxel retro game engine)

## TODO:
- [x] **clean code**
- [x] **Cross Platform**
- [ ] **sound effects** aren't complete
- [x] **levels** aren't implemented
- [x] **comments** aren't complete
- ...

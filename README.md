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

### Directly:
1. Install [pyxel](https://github.com/kitao/pyxel)
    ```bash
    python3 -m venv env
    source env/bin/activate
    pip3 install pyxel
    ```
2. Enjoy!
    - Run:
        ```bash
        python3 pyxelTetris.py
        ```

### WebAssembly: Help you to play game on every platform.
- Notice!
    1. **Chrome FireFox** Are Best Choice For Phones
    2. **FireFox Chrome Brave** Are Best Choice For LapTop Or PCs
    3. Make virtualenv
        ```bash
        python3 -m venv env
        source env/bin/activate
        pip3 install pyxel
        ```
    4. Install make tools
        ```bash
        sudo apt install make
        ```    
    5. Go to **path/to/Tetris_Pyxel** repo

    - **PCs**:
        1. Do it
            ```bash
            git clone https://github.com/mehrdad-mixtape/Tetris_Pyxel
            cd Tetris_Pyxel/build
            make all
            cd ../wasm
            ```
        2. Connect your system to your local network
            - Find IP-ADDRESS of your system. LAN or WLAN
                - Linux:
                    ```bash
                    ifconfig

                    OR

                    ip addr show
                    ```
                - Windows:
                    ```bash
                    ipconfig
                    ```
        3. Run **run-game-server.py** On Terminal Or Cmd Or PowerShell Or WSL Or etc ...
            ```bash
            python3 run-game-server.py --addr 192.168.x.x --port 8080
            ```
        4. Open Your Browser & Go to URL --> http://ADDR:8080 & Wait For Seconds
        5. Game Will Be Start On Your Browser!

    - **Phones**: I Recommend **UserLand** (linux on android):
        1. Enable your ***data-network-connection*** and ***HotSpot*** network.
        2. Install **UserLand** and setup your linux distribution (I recommend install **debian without Gui**)
        3. Install this packages
            ```bash
            sudo apt install curl git vim net-tools python3 make
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
        5. Do it
            ```bash
            git clone https://github.com/mehrdad-mixtape/Tetris_Pyxel
            cd Tetris_Pyxel/build
            make all
            cd ../wasm
            ```
        6. Run the source code of **run-game-server.py**
            ```bash
            python3 run-game-server.py --addr 192.168.x.x --port 8080
            ```
        7. Open Your ***Chrome Browser*** & Go to URL --> http://ADDR:8080 & Wait For Seconds
        8. Game Will Be Start On Your Browser!

## Issus:
I fixed many `Critical Bugs`, But maybe ... :)
- I made the first version in ***3 days*** on my free time! Just for Fun with (Pyxel retro game engine)

## TODO:
- [x] **clean code**
- [x] **Cross Platform**
- [x] **sound effects** aren't complete
- [x] **levels** aren't implemented
- [x] **comments** aren't complete
- [] **cache the piece**
- [] **fix piece cover piece** when move it left or right
- [] **score board**
- [] **implement center rotation**

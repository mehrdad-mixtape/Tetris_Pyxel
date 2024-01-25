all:
	cp -r ../env/lib/python3.10/site-packages/pyxel ./
	rm -rf pyxel/examples pyxel/editor
	pyxel package . pyxelTetris.py
	pyxel app2html build.pyxapp
	rm build.pyxapp
	rm -rf pyxel
	mv build.html ../wasm/pyxelTetris.html

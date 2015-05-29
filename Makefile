PYTHON := python3

.PHONY: run clean

run: httpserver.py clientside.html sunlight.js pginterface.py api.py 
	$(PYTHON) $<

%.js: %.coffee
	coffee -c $<

clean:
	-rm sunlight.js
	-rm -rf __pycache__

PYTHON := python3

.PHONY: run

run: httpserver.py clientside.html sunlight.js pginterface.py api.py 
	$(PYTHON) $<

%.js: %.coffee
	coffee -c $<

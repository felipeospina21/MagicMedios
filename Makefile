h ?= true

debug:
	python main.py --debug --headles=$(h)

start:
	python main.py

test:
	python main.py --test

lint:
	ruff check

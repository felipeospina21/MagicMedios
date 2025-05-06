h ?= true
l ?= 3

debug:
	python main.py --debug --headles=$(h)

start:
	python main.py

test:
	python main.py --test

load:
	python main.py --debug --headles=$(h) --load_test=$(l)

lint:
	ruff check

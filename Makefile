h ?= true
l ?= 3

.PHONY: help debug start test load lint

debug:
	python main.py --debug --headless=$(h)

help:
	@echo "Available targets:"
	@echo "  make debug        Debug mode: test output file, debug consecutive path, skips prompts"
	@echo "  make start        Normal mode: asks for client/company/user and uses production consecutive"
	@echo "  make test         Test mode: test output file, skips prompts, keeps normal consecutive path"
	@echo "  make load         Load-test mode: repeats scraping l times without generating PPTX"
	@echo "  make lint         Run ruff check"
	@echo ""
	@echo "Variables:"
	@echo "  h=true|false      Controls headless mode for debug/load"
	@echo "  l=<number>        Number of load test iterations"


start:
	python main.py

test:
	python main.py --test

load:
	python main.py --debug --headless=$(h) --load_test=$(l)

lint:
	ruff check

compile-deps:
	pip-compile requirements.in

install:
	uv pip install -r requirements.txt

serve:
	mkdocs serve

gen-test:
	python scripts/generate-docs.py --test

gen:
	python scripts/generate-docs.py
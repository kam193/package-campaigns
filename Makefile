install:
	uv pip install -r requirements.txt

serve:
	zensical serve

build:
	zensical build --clean

gen-test:
	python scripts/generate-docs.py --test

gen:
	python scripts/generate-docs.py

PIP_COOLDOWN ?= P3D

lock:
	PIP_UPLOADED_PRIOR_TO="$(PIP_COOLDOWN)" pip-compile -q --generate-hashes --output-file requirements.txt $(ARGS) requirements.in

lock-update:
	PIP_UPLOADED_PRIOR_TO="P3D" pip-compile --output-file requirements.txt --generate-hashes --upgrade $(ARGS) requirements.in
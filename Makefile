.PHONY: install run debug clean lint

install:
	pip install -r requirements.txt

run:
	python pac-man.py config.json

debug:
	python -m pdb pac-man.py config.json

clean:
	python -c "import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('__pycache__')]; shutil.rmtree('.mypy_cache', ignore_errors=True); shutil.rmtree('.pytest_cache', ignore_errors=True)"

lint:
	python -m flake8 .
	python -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs


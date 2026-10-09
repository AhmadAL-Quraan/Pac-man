.PHONY: install run debug clean lint check_venv 

PIP=.venv/bin/pip

install: check_venv
	$(PIP) install -r requirements.txt
	@echo
	@echo "Trying to install mazgenerator.whl if exists"
	@if [ ! -f ./mazegenerator-2.1.0-py3-none-any.whl ]; then\
		echo "mazgenerator.whl not found";\
	fi
	@if [ -f ./mazegenerator-2.1.0-py3-none-any.whl ]; then\
			$(PIP) install mazegenerator-2.1.0-py3-none-any.whl;\
	fi
	@echo
	@echo "Requirement libraries installed run: source .venv/bin/activate"

check_venv: 
	@if [ -n "$VIRTUAL_ENV" ]; then\
		python3 -m venv .venv;\
	fi

run:
	python pac-man.py config.json

debug:
	python -m pdb pac-man.py config.json

clean:
	python -c "import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('__pycache__')]; shutil.rmtree('.mypy_cache', ignore_errors=True); shutil.rmtree('.pytest_cache', ignore_errors=True)"

lint:
	@python -m flake8 .
	@python -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs


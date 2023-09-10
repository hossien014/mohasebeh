install: 
	python3 -m pip install --upgrade pip&&\
		python3 -m pip install -r requiremnts.txt

test:
	python3 -m pytest -vv 

format:
	python3 -m black *.py

lint:
	pylint --disable=R,C *.py
all: install lint test format

run_env:
	source .venv/Scripts/activate
	


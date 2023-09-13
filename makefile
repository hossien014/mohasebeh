install: 
	pip install --upgrade pip&&\
		pip install -r requiremnts.txt

install-pg:
	pip install -e .

test:
	coverage run -m pytest -vv&&\
	coverage report 

test-2:
	python3 -m pytest -vv
	

format:
	black mohasebeh_v1

lint:
	python3 -m pylint --disable=R,C mohasebeh_v1

all: install lint test format

run_env:
	source .venv/Scripts/activate

init-db:
	flask --app mohasebeh_v1 init-db
	
run-sql:
	sqlite3 .\instance\mohasbat.sqlite
run-flask:
	flask --app mohasebeh_v1 run --debug



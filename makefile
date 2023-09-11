install: 
	pip install --upgrade pip&&\
		pip install -r requiremnts.txt

test:
	coverage run -m pytest&&\
	coverage report

format:
	black mohasebeh_v1

lint:
	python3 -m pylint --disable=R,C mohasebeh_v1

all: install lint test format

run_env:
	source .venv/Scripts/activate
	
runflask:
	flask --app mohasebeh_v1 run --debug



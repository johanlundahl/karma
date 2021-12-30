MKFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
CURRENT_DIR := $(dir $(MKFILE_PATH))
	
clean:
	find . -name '*.pyc' -delete
	python3 -m karma.cmd delete-db

init:
	pip3 install -r requirements.txt
	python3 -m karma.cmd init

run:
	python3 -m karma.app

test:
	coverage run --source=. -m pytest tests/*_test.py

cov:
	coverage report
	coverage html

lint:
	flake8 --statistics --count
		
update:
	git pull
	pip3 install -r requirements.txt	

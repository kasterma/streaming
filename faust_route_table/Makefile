VENV=. venv/bin/activate

all: venv test format scan

.PHONY: venv
venv:
	python3.8 -m venv venv
	${VENV} ; pip install -i http://localhost:8989/root/pypi/+simple/ --upgrade pip
	${VENV} ; pip install -r requirements.txt

.PHONY: clean
clean:
	rm -rf venv

.PHONY: test
test:
	${VENV} ; pytest

.PHONY: format
format:
	${VENV} ; black *.py

.PHONY: scan
scan:
	${VENV} ; safety check
	${VENV} ; bandit *.py  # Note: will warn for asserts in tests

.PHONY: wheel install test clean

wheel:
	python3 -m pip wheel . --no-deps -w dist

install:
	python3 -m pip install dist/*.whl

test:
	python3 -m pytest -q tests

clean:
	rm -rf dist build src/*.egg-info
	find . -name __pycache__ -type d -prune -exec rm -rf {} +

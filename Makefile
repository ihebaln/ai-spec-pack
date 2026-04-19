.PHONY: test data-check eval-gate install clean

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v --tb=short

data-check:
	pytest tests/test_data_checks.py -v --tb=short

eval-gate:
	python src/eval_gate.py

clean:
	rm -rf __pycache__ .pytest_cache reports/*.json

.PHONY: test perf_test clean build_ais


test:
	py.test

perf_test:
	python tests/perf_test.py

clean:
	rm -Rf build tron-log-* `find . -name '*.pyc'`

build:
	mkdir build

ais: build build_ai.py
	python build_ai.py ai_wanderer.py build/ai_wanderer.py

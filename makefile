.PHONY: test perf_test clean build_ais


test:
	py.test

perf_test:
	python tests/perf_test.py

clean:
	rm -Rf build

build:
	mkdir build

build_ais: build
	python build_ai.py ai_wanderer.py build/ai_wanderer.py

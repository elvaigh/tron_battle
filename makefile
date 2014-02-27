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
	python build_ai.py ai_crosser.py build/ai_crosser.py
	python build_ai.py ai_hugger.py build/ai_hugger.py
	python build_ai.py ai_minimaxer.py build/ai_minimaxer.py
	python build_ai.py ai_gbase.py build/ai_gbase.py

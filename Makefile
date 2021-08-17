mypy:
	@poetry run mypy src/dashy/* tests/*

flake8:
	@poetry run flake8 src/dashy/* tests/*

lint: mypy flake8

test: unit_test

unit_test:
	@poetry run pytest tests/unit -xvvs

shell:
	@poetry run ipython

install_git_hooks:
	@ln -s /Users/axel/Projects/dashy/.hooks/pre-push .git/hooks/pre-push

install:
	poetry install
	poetry run pre-commit install --install-hooks --overwrite
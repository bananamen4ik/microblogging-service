flake8 . (проверка качества кода и покрытия документацией с дополнительными плагинами: flake8-docstrings, wemake-python-styleguide)
mypy . (проверка типов)
pytest (проверка созданных тестов)
pytest --cov-config=.coveragerc --cov=. tests/ (pytest-cov - проверка на покрытие тестами)
Проверка качества кода и покрытия документацией с дополнительными плагинами:

- flake8-docstrings
- wemake-python-styleguide

`flake8 .`

Проверка типов

`mypy .`

Проверка созданных тестов

`pytest`

Проверка на покрытие тестами (pytest-cov)

`pytest --cov-report=term-missing --cov=. tests/`

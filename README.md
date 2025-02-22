# Дипломный проект "Сервис микроблогов"

<p align="center">
  <img src="https://i.imgur.com/rM5fTDx.png" width="48%">
  <img src="https://i.imgur.com/qjAzAWD.png" width="48%">
</p>

## Описание сервиса

Корпоративный сервис микроблогов, очень похожий на Twitter.

## Функциональность

- Пользователь может добавить новый твит.
- Пользователь может удалить свой твит.
- Пользователь может зафоловить другого пользователя.
- Пользователь может отписаться от другого пользователя.
- Пользователь может отмечать твит как понравившийся.
- Пользователь может убрать отметку "Нравится".
- Пользователь может получить ленту из твитов отсортированных в
  порядке убывания по популярности от пользователей, которых он фоловит.
- Твит может содержать картинку.
- Добавление пользователя через API доступно только в dev окружении.

## Общий стек технологий

- Docker - для контейнеризации и управления компонентами системы.
- Nginx - в качестве веб-сервера.
- FastAPI - фреймворк для разработки API на Python.
- PostgreSQL - база данных.

## Установка и запуск

1. Склонируйте репозиторий в удобное место.
2. В зависимости от окружения создайте `.env` файл:
    1. Для окружения `dev` перейдите в директорию
       `./envs/dev`.
    2. Для окружения `prod` перейдите в директорию
       `./envs/prod`.
    3. Скопируйте файл `.env.example` в файл `.env`.
    4. Измените содержимое ранее созданного файла `.env`
       на свои необходимые данные.
3. Запуск:
    1. Для запуска сервиса необходимо приложение
       docker.
    2. Запустите терминал и перейдите в корневую
       директорию сервиса куда он был склонирован.
    3. В зависимости от окружения напишите следующую
       команду:
        1. Для окружения `dev`: `docker compose up`.
        2. Для окружения `prod`: `docker compose -f
           compose.yaml -f compose.prod.yaml up`
4. Откройте браузер и перейдите по адресу
   `http://localhost`.

## API документация

- Swagger документация доступна по адресу:
  `http://localhost/docs`.
- ReDoc документация доступна по адресу:
  `http://localhost/redoc`.

## Проверка кода и тестирование

Код полностью покрыт тестами с помощью `pytest`, проверен
линтером `flake8` (с плагинами `wemake-python-styleguide`
и `flake8-docstrings`) и статической проверкой типов `mypy`.

### Тестирование кода

Тесты необходимо запускать в `dev` окружении!

Для запуска всех тестов выполните команду
`docker exec -ti fastapi pytest`.

Для проверки покрытия кода тестами выполните команду
`docker exec -ti fastapi
pytest --cov-report=term-missing --cov=. tests/`.

### Проверка кода

Для проверки с помощью `flake8` выполните команду:
`docker exec -ti fastapi flake8 .`.

Для проверки с помощью `mypy` выполните команду:
`docker exec -ti fastapi mypy .`.
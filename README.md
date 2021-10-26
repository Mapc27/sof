# sof

## Установка и запуск проекта

- `git clone https://github.com/Mapc27/sof.git` - клонирование репозитория
- `cd sof/`
- `poetry install` - создание виртуального окружения и установка зависимостей
- `установите PostgreSQL`
- `sudo -i -u postgres` - вход в консоль postgres. При необходимости, нужно авторизоваться
- `psql`
- `CREATE DATABASE sof;` - создание базы данных
- `\q` - выход из psql
- `exit` - выход из консоли postgres
- `cd sof/`
- `subl config.py` или `pycharm-professional config.py` - измените файл конфигурации
- `poetry shell` - вход в виртуальное окружение
- `cd sof/`
- `export FLASK_APP='manage.py'` - объявление переменной среды
- `python3 create_db.py` - создание таблиц
- `flask db migrate` - миграции
- `python3 manage.py` - запуск сервера

# virtual-museum-backend-2025s
# инструкция по развёртыванию
1. Установить PostgreSQL 
2. В консоли PostgreSQL: sudo -u postgres psql CREATE USER virtual_museum WITH PASSWORD '123' SUPERUSER; 
3. Установить зависимости: pip install -r requirements.txt

Для MacOS:
1. Запустите PostgreSQL сервис
brew services start postgresql@14

2. Подключитесь к PostgreSQL
psql postgres

3. Создайте пользователя и базу данных внутри psql
После подключения выполните команды:
CREATE USER virtual_museum WITH PASSWORD '123' SUPERUSER;
CREATE DATABASE virtual_museum OWNER virtual_museum;

4. Выйдите из psql
\q

Проверьте подключение:
psql -U virtual_museum -d virtual_museum

Выйдите из psql
\q

# Активируем окружение
source venv/bin/activate

# Запускаем так
PYTHONPATH=$(pwd) python3 app/main.py
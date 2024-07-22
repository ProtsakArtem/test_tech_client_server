# Client-Server Application for Encrypted Data Transfer

## Опис

Цей проект реалізує клієнт-серверну архітектуру для завантаження даних у базу даних. Клієнтська частина відправляє дані у зашифрованій формі на сервер, який, у свою чергу, дешифрує їх і додає до бази даних. Сервер також може відповідати на запити клієнта. Для перегляду даних у базі даних використовується Django-додаток з налаштованою адміністративною панеллю.

## Вимоги

- Python 3.6+
- Django
- cryptography
- asyncio

## Установка

1. Клонуйте репозиторій або завантажте файли проекту.

```bash
git clone <URL of your repository>
cd <repository directory>
```

2. Створіть та активуйте віртуальне середовище.
```bash
python -m venv venv
source venv/bin/activate # для Linux
venv\Scripts\activate # для Windows
```
3. Встановіть необхідні пакети.
```bash
pip install -r requirements.txt
```
4. Налаштуйте базу даних.
```bash
# Відредагуйте DATABASES в settings.py для підключення до вашої бази даних
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser # Створіть адміністративного користувача
```
## Генерація ключів
Запустіть create_keys.py для генерації RSA ключів для шифрування симетричних ключів.
```bash
python create_keys.py
```

## Запуск
1. Запуск серверної частини:
```bash
python server_app.py
```
2. Запуск клієнтської частини:
```bash
python client_app.py
```

## Перегляд даних
1. Запустіть Django сервер:
```bash
python manage.py runserver
```

2. Увійдіть в адміністративну панель за адресою http://127.0.0.1:8000/admin використовуючи створеного суперкористувача.
4. Переглядайте та керуйте записами у базі даних. 

## Користування REST API
Після налаштування REST API ви можете використовувати такі HTTP запити для взаємодії з базою даних:
1. Створення запису (POST):
```bash
curl -X POST http://127.0.0.1:8000/api/datarecords/ -H "Content-Type: application/json" -d '{"name": "user1", "encrypted_data": "data1"}'
```
2. Отримання всіх записів (GET):
```bash
curl -X GET http://127.0.0.1:8000/api/datarecords/
```
3. Оновлення запису (PUT):
```bash
curl -X PUT http://127.0.0.1:8000/api/datarecords/1/ -H "Content-Type: application/json" -d "{\"name\": \"user1\", \"encrypted_data\": \"updated_data1\"}"
```
4. Видалення запису (DELETE):
```bash
curl -X DELETE http://127.0.0.1:8000/api/datarecords/1/
```
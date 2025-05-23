Платформа для обмена вещами

Установка

1. Клонируйте репозиторий

2. Создайте и активируйте виртуальное окружение:

python -m venv venv
venv\Scripts\activate для Windows

3. Установите зависимости:

pip install -r requirements.txt

4. Настройте базу данных PostgreSQL:
Создайте БД с именем barter_db

Обновите настройки в barter_system/settings.py при необходимости

5. Примените миграции:

bash
python manage.py migrate

6. Создайте суперпользователя:

bash
python manage.py createsuperuser

7. Запустите сервер:

bash
python manage.py runserver

8. Использование API
Объявления (Ads)
GET /api/ads/ - список всех объявлений

POST /api/ads/ - создать новое объявление

GET /api/ads/{id}/ - получить объявление по ID

PUT /api/ads/{id}/ - обновить объявление

DELETE /api/ads/{id}/ - удалить объявление

 Параметры фильтрации:

?category=electronics - фильтр по категории

?condition=used - фильтр по состоянию

?search=Python - поиск по заголовку и описанию

9. Предложения обмена (Exchange Proposals)
GET /api/proposals/ - список всех предложений

POST /api/proposals/ - создать новое предложение

GET /api/proposals/{id}/ - получить предложение по ID

POST /api/proposals/{id}/accept/ - принять предложение

POST /api/proposals/{id}/reject/ - отклонить предложение

Параметры фильтрации:

?sent=true - предложения, отправленные текущим пользователем

?received=true - предложения, полученные текущим пользователем

?status=pending - фильтр по статусу

10. Запуск тестов
bash
python manage.py test

11. Административная панель
Доступна по адресу /admin/ после создания суперпользователя.


12. Запуск проекта
bash
python manage.py runserver
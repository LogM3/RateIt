![yamdb workflow](https://github.com/logm3/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
### Описание  

Данный проект предоставляет доступ к сервису YaMDb посредством API.
Вы можете:

- просматривать раличные произведения
- писать отзывы на произведения
- ставить оценку произведениям
- комментировать отзывы других пользователей

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/LogM3/infra_sp2.git
```

```
cd infra_sp2
```

Cоздать и активировать виртуальное окружение:

```
py -3.7 -m venv env
```

```
. venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r api_yamdb/requirements.txt
```

Создать файл .env в директории infra и указать в нём параметры для БД, например:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=12345
DB_HOST=db
DB_PORT=5432
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Примеры взаимодействия:

Вам доступны такие эндпойнты:

- api/v1/auth/signup/ - регистрация в сервисе yamdb
- api/v1/auth/token/ - получение токена авторизации в сервисе yamdb
- api/v1/users/ - просмотр, создание и редактирование пользователей (для администратора)
- api/v1/users/me/ - редактирование данных своего профиля

Пример регистрации (POST запрос к api/v1/auth/signup/):

```
{
    "username":"User1",
    "email":"user1@ya.ru"
}
```

Пример получения токена (POST запрос к api/v1/auth/token/):

```
{
    "username":"User1",
    "confirmation_code":"89cbba4f-2c6b-4650-8f78-347055c193fd"
}
```

Пример добавления пользователя (POST запрос к api/v1/users/):

```
{
    "username":"User2",
    "email":"user2@ya.ru",
    "first_name":"Вася",
    "last_name":"Васильевич"
}
```

Пример редактирования данных своего профиля (POST запрос к api/v1/users/me/):

```
{
    "first_name":"Иван",
    "last_name":"Иванов"
}
```

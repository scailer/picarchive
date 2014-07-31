picarchive
==========

## Установка ##

Копируем к себе

```sh
$ git clone https://github.com/scailer/picarchive.git picarchive_project
$ cd picarchive_project
```

Создаем виртуальное окружение, любым удобным для Вас способом

```sh
$ virtualenv2 env
$ ./env/bin/pip install -r project/pip_req.txt
```

Создаем файл настроек project/local.py где укадываем:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'project/picarchive.db',
    }
}

EMAIL_HOST = 'smtp.host.ru'
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL = SERVER_EMAIL = 'no-reply@host.net'
EMAIL_SUBJECT_PREFIX = '[PicArchive] '
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 25
EMAIL_USE_TLS = False
```

Создаем базу 

```sh
./env/bin/python manage.py syncdb
```


## Запуск ##

В разных консолях, одновременно запускаем

```sh
./env/bin/python manage.py celeryd
```

и

```sh
./env/bin/python manage.py runserver
```


## Использование ##

1. Регистрируемся
2. Логинимся
3. Создаем картинки
4. Редактируем заголовок картинки
5. Удаляем картинки
6. Добавляем заметки (видны только для текущего пользователя)
7. Отправляем на email (тут вот celery работает)
8. Выходим


## Структура проекта ##

project - базовые настройки, список зависимостей и т.п.
utils - всякие самописные и ворованые утилитки
static - js, css файлы
templates - наш единственный шаблон
media - тут храняться файлики пользователей
logs - сюда пишутся логи
apps - собственно уникальная бизнес-логика проекта

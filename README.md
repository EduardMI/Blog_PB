# Python_Band

Для старта проекта
```
python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser
```

### Fixtures

Перед загрузкойц фикстур должен быть создан superuser, тк статьи заводятся на него
```
python manage.py loaddata fixtures/fixtures.json
```
В фикстурах добавляется 4 категории и 12 статей.

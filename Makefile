# Start containers
up:
	docker-compose -f docker-compose.yml up

# Start containers in background
upd:
	docker-compose -f docker-compose.yml up -d

# Stop containers
down:
	docker-compose -f docker-compose.yml down

# Remove containers
remove:
	docker-compose -f docker-compose.yml down -v

# Restart containers
restart:
	docker-compose -f docker-compose.yml restart

# Build containers
build:
	docker-compose -f docker-compose.yml build

# Pipenv
pipenv_install:
	docker-compose -f docker-compose.yml run --rm djangoapp pipenv install

# Bash
bash:
	docker-compose -f docker-compose.yml run --rm djangoapp bash

# Django create new app
start_app:
	docker-compose -f docker-compose.yml run --rm djangoapp pipenv run python ./manage.py startapp $(app_name)

# Django create superuser
createsuperuser:
	docker-compose -f docker-compose.yml run --rm djangoapp pipenv run python ./manage.py createsuperuser

# Django migrate
migrate:
	docker-compose -f docker-compose.yml run --rm djangoapp pipenv run python ./manage.py migrate

# Django makemigrations
makemigrations:
	docker-compose -f docker-compose.yml run --rm djangoapp pipenv run python ./manage.py makemigrations

# Django shell
shell:
	docker-compose -f docker-compose.yml run --rm djangoapp pipenv run python ./manage.py shell

# Run Tests
test:
	docker-compose -f docker-compose.yml run --rm djangoapp pipenv run python ./manage.py test -v 2 --settings=config.settings.test

# Run test module
test_module:
	docker-compose -f docker-compose.yml run --rm djangoapp pipenv run python ./manage.py test -v 2 music_backend.$(module) --settings=config.settings.test

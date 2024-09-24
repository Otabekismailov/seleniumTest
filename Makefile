bulk_update:
	python manage.py bulk_update

populate_dict:
	python manage.py populate_dict

# supervisor:
# 	sudo supervisorctl restart backend
server:
	python manage.py runserver 0.0.0.0:8000

run:
	python manage.py runserver 8000

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate



push:
	git add .
	git commit -m "Updated: $$(date +'%Y-%m-%d %H:%M:%S')"
	git push origin main

pull:
	git pull origin main

merge:
	git checkout main
	git merge main
	git push origin main
	git checkout main

install:
	pip install -r requirements.txt
freeze:
	pip freeze > requirements.txt



app_name := $(word 2, $(MAKECMDGOALS))

.PHONY: app-api

app-api:
	@cd api/$(app_name)
	@touch api/$(app_name)/urls.py
	@touch api/$(app_name)/views.py
	@touch api/$(app_name)/serializers.py



user:
	python manage.py createsuperuser
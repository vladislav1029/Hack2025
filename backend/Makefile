.DEFAULT_GOAL := help

.PHONY: help start 
help:
	@echo Make command:
	@echo 	start-app	 				Run a local project.
	@echo 	revision MESSAGE="your message"			Create an "alembic" revision with your message.
	@echo 	upgrade						Upgrade "alembic" migration to top version.
	@echo 	downgrade					Revert to previous version of "alembic" migration.

start:
	docker-compose up -d


.PHONY: start-app
start-app:
	poetry run python -m uvicorn main:main --factory --reload

.PHONY: revision upgrade downgrade
revision:
ifndef MESSAGE
	$(error MESSAGE is not defined. Usage: make revision MESSAGE="your message")
endif
	poetry run alembic revision --autogenerate -m "$(MESSAGE)"

upgrade:
	poetry run alembic upgrade head

downgrade:
	poetry run alembic downgrade -1
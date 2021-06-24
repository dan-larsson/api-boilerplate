NAME:=api-boilerplate

.PHONY: clean
clean: 
	@docker system prune -a

.PHONY: build-app
build-app:
	@docker-compose build --no-cache app

.PHONY: build-db
build-db:
	@docker-compose build --no-cache db

.PHONY: build
build: build-db build-app

.PHONY: run
run:
	@docker-compose up app

.PHONY: run-bg
run-bg:
	@docker-compose up -d app

.PHONY: logs
logs:
	@docker-compose logs -f

.PHONY: psql
psql:
	@PGPASSWORD=secret NAME=${NAME} docker-compose exec db \
		psql -U api-boilerplate ${NAME} \
			-P linestyle=unicode \
			-P border=2 \
			-P expanded=auto \
			-P footer=on \
			-v COMP_KEYWORD_CASE=upper \
			-v PROMPT1="%[%033[33;1m%]%x%[%033[0m%]%[%033[1m%]%n%[%033[0m%]%R%# "

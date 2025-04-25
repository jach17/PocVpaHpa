DOCKER_COMPOSE = docker compose -f ./docker-compose.yml

up:
	${DOCKER_COMPOSE} up -d

rebuild:
	${DOCKER_COMPOSE} up -d --build

test_coverage:
	pytest --cov=app --cov-report=html --cov-report=xml --cov-config=.coveragerc

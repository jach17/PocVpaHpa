DOCKER_COMPOSE = docker compose -f ./docker-compose.yml

up:
	${DOCKER_COMPOSE} up -d

rebuild:
	${DOCKER_COMPOSE} up --build

test_coverage:
	pytest --cov=app --cov-report=html --cov-report=xml --cov-config=.coveragerc

build_image:
	docker build -t user-service-api:1.0.0 .
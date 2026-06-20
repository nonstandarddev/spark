.PHONY: setup rebuild clean down up scale submit

setup:
	uv sync --locked

rebuild:
	docker compose build

clean:
	docker compose down --volumes --remove-orphans

down:
	docker compose down --remove-orphans

up:
	docker compose up -d spark-master spark-worker spark-history

scale:
	docker compose up -d spark-master spark-worker spark-history --scale spark-worker=$(n)

submit:
	docker compose run --rm spark-driver /opt/spark/apps/submit.sh "$(app)" $(args)

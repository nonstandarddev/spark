.PHONY: clean down up submit

clean:
	docker compose down --volumes --remove-orphans

down:
	docker compose down --remove-orphans

up:
	docker compose up -d spark-master spark-worker spark-history

submit:
	docker compose run --rm spark-driver /opt/spark/apps/submit.sh "$(app)" $(args)

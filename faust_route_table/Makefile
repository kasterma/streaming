VENV=. venv/bin/activate

all: venv test format scan

.PHONY: venv
venv:
	python3.8 -m venv venv
	${VENV} ; pip install --upgrade pip # pip install -i http://localhost:8989/root/pypi/+simple/ --upgrade pip
	${VENV} ; pip install -r requirements.txt

.PHONY: clean
clean:
	rm -rf venv

.PHONY: up
up:
	docker-compose up

.PHONY: topics
topics:
	docker exec -ti faust_route_table_kafka_1 kafka-topics --create --topic hellos-here --zookeeper zookeeper:2181 --partitions 8 --replication-factor 1
	docker exec -ti faust_route_table_kafka_1 kafka-topics --create --topic points-here --zookeeper zookeeper:2181 --partitions 8 --replication-factor 1

show-changelog:
	docker exec -ti faust_route_table_kafka_1 kafka-console-consumer --bootstrap-server localhost:9092 --topic get-hello-hello_counts-changelog --from-beginning


.PHONY: list-topics
list-topics:
	docker exec -ti faust_route_table_kafka_1 kafka-topics --list --zookeeper zookeeper:2181

.PHONY: down
down:
	docker-compose down

.PHONY: test
test:
	${VENV} ; pytest

.PHONY: format
format:
	${VENV} ; black *.py

.PHONY: scan
scan:
	${VENV} ; safety check
	${VENV} ; bandit *.py  # Note: will warn for asserts in tests

run/generator:
	${VENV} ; faust -A send_hellos worker -l info

run-worker-1:
	${VENV} ; faust -A get_hellos worker -l info --web-port 6067 --web-host localhost

run-worker-2:
	${VENV} ; faust -A get_hellos worker -l info --web-port 6068 --web-host localhost

query-worker-1:
	for i in $(shell seq 0 10); do curl localhost:6067/count/?i=hellohello-$$i; echo; done

query-worker-2:
	for i in $(shell seq 0 10); do curl localhost:6068/count/?i=hellohello-$$i; echo; done

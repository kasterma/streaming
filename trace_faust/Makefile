VENV=source venv/bin/activate

venv:
	python3.8 -m venv venv
	${VENV} ; pip install -r requirements.txt

topics:
	docker exec -ti trace_faust_kafka_1 kafka-topics --create --topic raw-events --zookeeper zookeeper:2181 --partitions 8 --replication-factor 1
	docker exec -ti trace_faust_kafka_1 kafka-topics --create --topic counts --zookeeper zookeeper:2181 --partitions 8 --replication-factor 1
	docker exec -ti trace_faust_kafka_1 kafka-topics --create --topic alerts --zookeeper zookeeper:2181 --partitions 8 --replication-factor 1

generator:
	${VENV} ; faust -A send_events worker -l info

counter:
	${VENV} ; faust -A counter worker -l info --web-port 6022 --web-host localhost

counter2:
	${VENV} ; faust -A counter worker -l info --web-port 6023 --web-host localhost

counter3:
	${VENV} ; faust -A counter worker -l info --web-port 6024 --web-host localhost

counter4:
	${VENV} ; faust -A counter worker -l info --web-port 6025 --web-host localhost

checker:
	${VENV} ; faust -A checker worker -l info --web-port 6021 --web-host localhost

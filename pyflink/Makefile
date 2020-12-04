VENV=source venv/bin/activate

venv:
	python3.6 -m venv venv
	${VENV} ; pip install -r requirements.txt

topics:
	docker exec -ti pyflink_kafka_1 kafka-topics --create --topic raw-events --zookeeper zookeeper:2181 --partitions 8 --replication-factor 1

clean:
	rm -rf /tmp/output

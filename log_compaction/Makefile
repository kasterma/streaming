VENV=source venv/bin/activate

venv:
	python3.8 -m venv venv
	${VENV} ; pip install -r requirements.txt

topics:
	docker exec -ti log_compaction_kafka_1 kafka-topics --create --topic raw-events --zookeeper zookeeper:2181 --partitions 8 --replication-factor 1
	docker exec -ti log_compaction_kafka_1 kafka-topics --create --topic count-log-compaction --zookeeper zookeeper:2181 --partitions 8 --replication-factor 1 \
	--config "cleanup.policy=compact" --config "delete.retention.ms=100"  --config "segment.ms=100" --config "min.cleanable.dirty.ratio=0.01"


producer:
	python3 producer.py

counter:
	python3 counter.py 1

counter2:
	python3 counter.py 2

counter3:
	python3 counter.py 3

counter4:
	python3 counter.py 4
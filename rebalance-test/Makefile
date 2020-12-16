VENV=source venv/bin/activate

venv:
	python3.8 -m venv venv
	${VENV} ; pip install -r requirements.txt


up:
	docker-compose up

down:
	docker-compose down

topics:
	docker exec -ti rebalance-test_kafka_1 kafka-topics --create --topic events --zookeeper zookeeper:2181 --partitions 5 --replication-factor 1
	docker exec -ti rebalance-test_kafka_1 kafka-topics --create --topic mem-updater --zookeeper zookeeper:2181 --partitions 5 --replication-factor 1 \
	   --config "cleanup.policy=compact" --config "delete.retention.ms=100"  --config "segment.ms=100" --config "min.cleanable.dirty.ratio=0.01"

generator:
	${VENV} ; python send_events.py

counter1:
	${VENV} ; python counter.py --msg-sleep 2 --group-id-id 1

counter2:
	${VENV} ; python counter.py --msg-sleep 2 --group-id-id 2

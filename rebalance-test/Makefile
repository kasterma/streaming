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
	   --config "cleanup.policy=compact" --config "delete.retention.ms=100"  --config "segment.ms=100" --config "min.cleanable.dirty.ratio=0.01" \
	   --config "max.compaction.lag.ms=100"

clean-topics:
	for i in $$(seq 0 9) ; do echo "key-$$i:" | kafkacat -b localhost:9092 -t mem-updater -Z -K: ; done

generator:
	${VENV} ; python send_events.py --delay-ms 100

counter1:
	${VENV} ; python counter.py --group-id-id 1

counter2:
	${VENV} ; python counter.py --group-id-id 2

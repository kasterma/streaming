VENV=. venv/bin/activate
NUMPART=10
NUM_KEYS?=20
START_KEY?=0

venv:
	python3.8 -m venv venv
	${VENV} ; pip install -r requirements.txt


up:
	docker-compose up

down:
	docker-compose down

topics:
	docker exec -ti rebalance-test_kafka_1 kafka-topics --create --topic events --zookeeper zookeeper:2181 --partitions ${NUMPART} --replication-factor 1
	docker exec -ti rebalance-test_kafka_1 kafka-topics --create --topic event-lists --zookeeper zookeeper:2181 --partitions ${NUMPART} --replication-factor 1
	docker exec -ti rebalance-test_kafka_1 kafka-topics --create --topic mem-updater --zookeeper zookeeper:2181 --partitions ${NUMPART} --replication-factor 1 \
	   --config "cleanup.policy=compact" --config "delete.retention.ms=100"  --config "segment.ms=100" --config "min.cleanable.dirty.ratio=0.01"

list-topics:
	docker exec -ti rebalance-test_kafka_1 kafka-topics --list --zookeeper zookeeper:2181

clean-topics:
	for i in $$(seq 0 9) ; do echo "key-$$i:" | kafkacat -b localhost:9092 -t mem-updater -Z -K: ; done

generator:
	${VENV} ; python red_paint.py --delay-ms 100 --num-keys ${NUM_KEYS} --start-key ${START_KEY} --quiet

counter1:
	${VENV} ; python counter.py --group-id-id 1

counter2:
	${VENV} ; python counter.py --group-id-id 2

counter3:
	${VENV} ; python counter.py --group-id-id 3

counter4:
	${VENV} ; python counter.py --group-id-id 4

counter5:
	${VENV} ; python counter.py --group-id-id 5

counter-explain:
	${VENV} ; python counter_explain.py --source-topic events --sink-topic event-lists

RED_PAINT_KEY?=-1
paint-explain:
	${VENV} ; python red_paint.py --red-paint-key ${RED_PAINT_KEY}

paint:
	${VENV} ; python red_paint.py --red-paint-key -2

format:
	black red_paint.py counter_explain.py


kafkacat-event-lists:
	kafkacat -b localhost -t event-lists -f 'Topic %t[%p], offset: %o, key: %k, payload: %S bytes: %s\n'

kafkacat-events:
	kafkacat -b localhost -t events -f 'Topic %t[%p], offset: %o, key: %k, payload: %S bytes: %s\n'

kafkacat-mem-updater:
	kafkacat -b localhost -t mem-updater -f 'Topic %t[%p], offset: %o, key: %k, payload: %S bytes: %s\n'

from pyflink.common.typeinfo import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer, FlinkKafkaProducer
from pyflink.datastream.functions import SourceFunction
from pyflink.common.serialization import SimpleStringSchema


topics = ["test"]
properties = {
    "bootstrap_servers": "localhost:9092",
    "group_id": "flink_test",
}
kafka_file_loc = "/Users/wouter/kpn/flink/flink/flink-connectors/flink-connector-kafka/target/"
kafka_file_name = "flink-connector-kafka_2.11-1.13-SNAPSHOT.jar"
core_file_loc = "/Users/wouter/kpn/flink/flink/flink-core"
core_file_name = "flink-core-1.13-SNAPSHOT.jar"
ref = "file://" + kafka_file_loc + kafka_file_name
ref2 = "file://" + core_file_loc + core_file_name
producer_config = {

}

def generator():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)
    
    env.add_classpaths(ref)

    # env.add_source(FlinkKafkaConsumer(topics, SimpleStringSchema(), properties))
    ds = env.from_collection(
        collection=[('ava',), ('bab', )],
        type_info=Types.ROW([Types.STRING(),]))
    ds.print()
    ds.add_sink(StreamingFileSink
            .for_row_format('/tmp/output', SimpleStringEncoder())
            .build())
    env.execute("ds_example_job")

if __name__ == '__main__':
    generator()
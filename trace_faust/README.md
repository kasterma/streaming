# tracing in a Faust program

Run a simple Faust example, and collect tracing data about the data flow that results.

0. kafka docker-compose
   copy-paste from other dir + version update

1. make example; Faust flow
     generator different events
     count types of events; asyncio with random sleep, and sometimes an error
     check if N more, then emit a message
        
     G --{a,a,b,b,c,a,b,c,d}--> C --{a:1, a:2, b:1, b:2, c:1}--> A --{there were 10 a's, there were 10 b's}-->
     
2. add tracing instrumentation: opentracing, faust/utils/tracing.py

3. collect somewhere; jeager, collector  (<--- docker-compose completion)
   https://github.com/jaegertracing/jaeger/blob/master/docker-compose/jaeger-docker-compose.yml
   http://localhost:16686  <- UI for jeager, here is where the data should eventually appear

4. Select simple webframework supported by open tracing
   FastAPI: [link](https://fastapi.tiangolo.com/)
   Opentracing support: [link](https://fastapi.tiangolo.com/)

5. Simple webserver with response behavior
   Use the response in the context of the counter

6. Implement distributed traces (between faust and the webserver)

7. Aiohttp request tracing headers with middleware(?)




[2020-11-20 15:54:26,542] [10540] [WARNING] e: 36 X
[2020-11-20 15:54:26,542] [10540] [WARNING] d: 43 X
[2020-11-20 15:54:26,542] [10540] [WARNING] c: 41 X
[2020-11-20 15:54:26,542] [10540] [WARNING] b: 34 
[2020-11-20 15:54:26,542] [10540] [WARNING] f: 35 
[2020-11-20 15:54:26,542] [10540] [WARNING] a: 32 



[WARNING] [^-App]: Missing sensor state for rebalance #1 


[2020-11-27 15:36:46,410] [6284] [WARNING] c: 28 
[2020-11-27 15:36:46,410] [6284] [WARNING] d: 150 
[2020-11-27 15:36:46,410] [6284] [WARNING] e: 155



---------------------------------------------------------

aming/trace_faust/Makefile counter2
source venv/bin/activate ; faust -A counter worker -l info --web-port 6023 --web-host localhost
Initializing Jaeger Tracer with UDP reporter
Using selector: KqueueSelector
Using sampler ConstSampler(True)
opentracing.tracer initialized to <jaeger_client.tracer.Tracer object at 0x1065acfa0>[app_name=counter]
Using selector: KqueueSelector
(0l(BƒaµS† v0.3.0(0qwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqk(B
(0x(B id          (0x(B count-events                                                        (0x(B
(0x(B transport   (0x(B [URL('kafka://localhost:9092')]                                     (0x(B
(0x(B store       (0x(B memory:                                                             (0x(B
(0x(B web         (0x(B http://localhost:6023/                                              (0x(B
(0x(B log         (0x(B -stderr- (info)                                                     (0x(B
(0x(B pid         (0x(B 6912                                                                (0x(B
(0x(B hostname    (0x(B erik.fritz.box                                                      (0x(B
(0x(B platform    (0x(B CPython 3.8.5 (Darwin x86_64)                                       (0x(B
(0x(B        +    (0x(B Cython (Clang 12.0.0 (clang-1200.0.31.1))                           (0x(B
(0x(B drivers     (0x(B                                                                     (0x(B
(0x(B   transport (0x(B aiokafka=0.7.0                                                      (0x(B
(0x(B   web       (0x(B aiohttp=3.7.3                                                       (0x(B
(0x(B datadir     (0x(B /Users/kasterma/projects/streaming/trace_faust/count-events-data    (0x(B
(0x(B appdir      (0x(B /Users/kasterma/projects/streaming/trace_faust/count-events-data/v1 (0x(B
(0mqqqqqqqqqqqqqvqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqj(B
[2020-11-27 16:09:51,825] [6912] [INFO] [^Worker]: Starting... 
[2020-11-27 16:09:51,830] [6912] [INFO] [^-App]: Starting... 
[2020-11-27 16:09:51,830] [6912] [INFO] [^--Monitor]: Starting... 
[2020-11-27 16:09:51,830] [6912] [INFO] [^--Producer]: Starting... 
[2020-11-27 16:09:51,831] [6912] [INFO] [^---ProducerBuffer]: Starting... 
[2020-11-27 16:09:51,865] [6912] [INFO] [^--CacheBackend]: Starting... 
[2020-11-27 16:09:51,865] [6912] [INFO] [^--Web]: Starting... 
[2020-11-27 16:09:51,865] [6912] [INFO] [^---Server]: Starting... 
[2020-11-27 16:09:51,866] [6912] [INFO] [^--Consumer]: Starting... 
[2020-11-27 16:09:51,867] [6912] [INFO] [^---AIOKafkaConsumerThread]: Starting... 
[2020-11-27 16:09:51,888] [6912] [INFO] [^--LeaderAssignor]: Starting... 
[2020-11-27 16:09:51,889] [6912] [INFO] [^--Producer]: Creating topic 'count-events-__assignor-__leader' 
[2020-11-27 16:09:51,903] [6912] [INFO] [^--ReplyConsumer]: Starting... 
[2020-11-27 16:09:51,903] [6912] [INFO] [^--AgentManager]: Starting... 
[2020-11-27 16:09:51,903] [6912] [INFO] [^---Agent: counter.counter]: Starting... 
[2020-11-27 16:09:51,906] [6912] [INFO] [^----OneForOneSupervisor: (1@0x106eec340)]: Starting... 
[2020-11-27 16:09:51,906] [6912] [INFO] [^---Conductor]: Starting... 
[2020-11-27 16:09:51,906] [6912] [INFO] [^--TableManager]: Starting... 
[2020-11-27 16:09:51,907] [6912] [INFO] [^---Conductor]: Waiting for agents to start... 
[2020-11-27 16:09:51,907] [6912] [INFO] [^---Conductor]: Waiting for tables to be registered... 
[2020-11-27 16:09:52,911] [6912] [INFO] [^---GlobalTable: event_counts]: Starting... 
[2020-11-27 16:09:52,912] [6912] [INFO] [^----Store: memory:]: Starting... 
[2020-11-27 16:09:52,912] [6912] [INFO] [^--Producer]: Creating topic 'count-events-event_counts-changelog' 
[2020-11-27 16:09:52,917] [6912] [INFO] [^---Recovery]: Starting... 
[2020-11-27 16:09:52,917] [6912] [INFO] [^--Producer]: Creating topic 'count-events-event_counts-changelog' 
[2020-11-27 16:09:52,922] [6912] [INFO] [^--Producer]: Creating topic 'count-events-__assignor-__leader' 
[2020-11-27 16:09:52,927] [6912] [INFO] Updating subscribed topics to: 
(0l(BRequested Subscription(0qqqqqqqqqqqqqqqk(B
(0x(B topic name                          (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqu(B
(0x(B count-events-__assignor-__leader    (0x(B
(0x(B count-events-event_counts-changelog (0x(B
(0x(B raw-events                          (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqj(B 
[2020-11-27 16:09:52,927] [6912] [INFO] Subscribed to topic(s): 
(0l(BFinal Subscription(0qqqqqqqqqqqqqqqqqqqk(B
(0x(B topic name                          (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqu(B
(0x(B count-events-__assignor-__leader    (0x(B
(0x(B count-events-event_counts-changelog (0x(B
(0x(B raw-events                          (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqj(B 
[2020-11-27 16:09:52,940] [6912] [INFO] Discovered coordinator 1 for group count-events 
[2020-11-27 16:09:52,941] [6912] [INFO] Revoking previously assigned partitions set() for group count-events 
[2020-11-27 16:09:52,942] [6912] [INFO] (Re-)joining group count-events 
[2020-11-27 16:09:52,944] [6912] [INFO] [^---Recovery]: Highwater for active changelog partitions:
(0l(BHighwater - Active(0qwqqqqqqqqqqqk(B
(0x(B topic (0x(B partition (0x(B highwater (0x(B
(0mqqqqqqqvqqqqqqqqqqqvqqqqqqqqqqqj(B 
[2020-11-27 16:09:52,947] [6912] [INFO] [^---Recovery]: Resuming flow... 
[2020-11-27 16:09:52,947] [6912] [INFO] [^---Recovery]: Recovery complete 
[2020-11-27 16:09:52,947] [6912] [INFO] [^---Recovery]: Restore complete! 
[2020-11-27 16:09:52,948] [6912] [INFO] [^---Fetcher]: Starting... 
[2020-11-27 16:09:52,948] [6912] [INFO] [^---Recovery]: Worker ready 
[2020-11-27 16:09:52,948] [6912] [INFO] [^Worker]: Ready 
[2020-11-27 16:09:53,997] [6912] [INFO] Joined group 'count-events' (generation 7) with member_id faust-0.3.0-dd5ce5a3-da6b-47e3-b404-7e3b687f46fd 
[2020-11-27 16:09:54,008] [6912] [INFO] Successfully synced group count-events with generation 7 
[2020-11-27 16:09:54,009] [6912] [INFO] Setting newly assigned partitions 
(0l(BTopic Partition Set(0qqqqqqqqqqqqqqqqqqwqqqqqqqqqqqqk(B
(0x(B topic                               (0x(B partitions (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B {0-7}      (0x(B
(0x(B raw-events                          (0x(B {6-7}      (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqqj(B for group count-events 
[2020-11-27 16:09:54,012] [6912] [WARNING] [^-App]: Missing sensor state for rebalance #1 
[2020-11-27 16:09:54,022] [6912] [INFO] [^---Recovery]: Highwater for active changelog partitions:
(0l(BHighwater - Active(0qqqqqqqqqqqqqqqqqqqwqqqqqqqqqqqwqqqqqqqqqqqk(B
(0x(B topic                               (0x(B partition (0x(B highwater (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqnqqqqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B 6         (0x(B -1        (0x(B
(0x(B 〃                                  (0x(B 7         (0x(B -1        (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqvqqqqqqqqqqqj(B 
[2020-11-27 16:09:54,032] [6912] [INFO] [^---Recovery]: active offsets at start of reading:
(0l(BReading Starts At - Active(0qqqqqqqqqqqwqqqqqqqqqqqwqqqqqqqqk(B
(0x(B topic                               (0x(B partition (0x(B offset (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqnqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B 6         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 7         (0x(B -1     (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqvqqqqqqqqj(B 
[2020-11-27 16:09:54,038] [6912] [INFO] [^---Recovery]: standby offsets at start of reading:
(0l(BReading Starts At - Standby(0qqqqqqqqqqwqqqqqqqqqqqwqqqqqqqqk(B
(0x(B topic                               (0x(B partition (0x(B offset (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqnqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B 0         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 1         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 2         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 3         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 4         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 5         (0x(B -1     (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqvqqqqqqqqj(B 
[2020-11-27 16:09:54,067] [6912] [INFO] [^---Recovery]: Resuming flow... 
[2020-11-27 16:09:54,067] [6912] [INFO] [^---Recovery]: Recovery complete 
[2020-11-27 16:09:54,067] [6912] [INFO] [^---Recovery]: Starting standby partitions... 
[2020-11-27 16:09:54,085] [6912] [INFO] [^---Recovery]: Highwater for standby changelog partitions:
(0l(BHighwater - Standby(0qqqqqqqqqqqqqqqqqqwqqqqqqqqqqqwqqqqqqqqqqqk(B
(0x(B topic                               (0x(B partition (0x(B highwater (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqnqqqqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B 0         (0x(B -1        (0x(B
(0x(B 〃                                  (0x(B 1         (0x(B -1        (0x(B
(0x(B 〃                                  (0x(B 2         (0x(B -1        (0x(B
(0x(B 〃                                  (0x(B 3         (0x(B -1        (0x(B
(0x(B 〃                                  (0x(B 4         (0x(B 14        (0x(B
(0x(B 〃                                  (0x(B 5         (0x(B -1        (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqvqqqqqqqqqqqj(B 
[2020-11-27 16:09:54,087] [6912] [INFO] [^---Recovery]: Restore complete! 
[2020-11-27 16:09:54,087] [6912] [INFO] [^---Recovery]: Seek stream partitions to committed offsets. 
[2020-11-27 16:09:54,148] [6912] [WARNING] [^-App]: Missing sensor state for rebalance #1 
[2020-11-27 16:09:54,148] [6912] [INFO] [^---Recovery]: Worker ready 
[2020-11-27 16:09:54,959] [6912] [WARNING] ids ['30'] 
[2020-11-27 16:09:54,960] [6912] [WARNING] Updated just f last 40 {'f'} 
[2020-11-27 16:09:54,960] [6912] [WARNING] {'uber-trace-id': '8b3fdf51e3db9697:50922ff43b94ddd0:0:1'} 
[2020-11-27 16:09:54,960] [6912] [INFO] Reporting span 8b3fdf51e3db9697:473fd69b5377156f:50922ff43b94ddd0:1 counter.send 
[2020-11-27 16:09:54,961] [6912] [WARNING] a: 1 
[2020-11-27 16:09:54,961] [6912] [WARNING] f: 1 
[2020-11-27 16:09:54,961] [6912] [INFO] Reporting span 8b3fdf51e3db9697:15e2c5a844e72dc1:50922ff43b94ddd0:1 counter.print-table 
[2020-11-27 16:09:54,961] [6912] [INFO] Reporting span 8b3fdf51e3db9697:50922ff43b94ddd0:0:1 counter.send-event 
[2020-11-27 16:09:54,962] [6912] [WARNING] ids ['30', '32'] 
[2020-11-27 16:09:54,962] [6912] [WARNING] Updated just f last 40 {'f'} 
[2020-11-27 16:09:54,962] [6912] [WARNING] {'uber-trace-id': 'fb3610cd9ee441c9:f181c3d04b96eae9:0:1'} 
[2020-11-27 16:09:54,963] [6912] [INFO] Reporting span fb3610cd9ee441c9:64ed5c18b8695213:f181c3d04b96eae9:1 counter.send 
[2020-11-27 16:09:54,963] [6912] [WARNING] a: 2 
[2020-11-27 16:09:54,963] [6912] [WARNING] f: 2 
[2020-11-27 16:09:54,963] [6912] [INFO] Reporting span fb3610cd9ee441c9:24b1bc9d0138325c:f181c3d04b96eae9:1 counter.print-table 
[2020-11-27 16:09:54,963] [6912] [INFO] Reporting span fb3610cd9ee441c9:f181c3d04b96eae9:0:1 counter.send-event 
[2020-11-27 16:09:54,964] [6912] [WARNING] ids ['30', '32', '33'] 
[2020-11-27 16:09:54,964] [6912] [WARNING] Updated just f last 40 {'f'} 
[2020-11-27 16:09:54,964] [6912] [WARNING] {'uber-trace-id': '2527d46cfdc9383e:f34a7d87d2c25e36:0:1'} 
[2020-11-27 16:09:54,965] [6912] [INFO] Reporting span 2527d46cfdc9383e:21c1fe27f306d18f:f34a7d87d2c25e36:1 counter.send 
[2020-11-27 16:09:54,965] [6912] [WARNING] a: 3 
[2020-11-27 16:09:54,965] [6912] [WARNING] b: 1 
[2020-11-27 16:09:54,965] [6912] [WARNING] f: 3 
[2020-11-27 16:09:54,965] [6912] [INFO] Reporting span 2527d46cfdc9383e:53083337a03f2f4f:f34a7d87d2c25e36:1 counter.print-table 
[2020-11-27 16:09:54,965] [6912] [INFO] Reporting span 2527d46cfdc9383e:f34a7d87d2c25e36:0:1 counter.send-event 
[2020-11-27 16:09:54,966] [6912] [WARNING] ids ['30', '32', '33', '34'] 
[2020-11-27 16:09:54,966] [6912] [WARNING] Updated just f last 40 {'f'} 
[2020-11-27 16:09:54,966] [6912] [WARNING] {'uber-trace-id': '4f4eae4f74d9a5a5:8b0886193ca0fa4c:0:1'} 
[2020-11-27 16:09:54,967] [6912] [INFO] Reporting span 4f4eae4f74d9a5a5:73f3fdcdd99bbaa4:8b0886193ca0fa4c:1 counter.send 
[2020-11-27 16:09:54,967] [6912] [WARNING] a: 3 
[2020-11-27 16:09:54,967] [6912] [WARNING] b: 2 
[2020-11-27 16:09:54,967] [6912] [WARNING] f: 4 
[2020-11-27 16:09:54,967] [6912] [INFO] Reporting span 4f4eae4f74d9a5a5:453b85add4020411:8b0886193ca0fa4c:1 counter.print-table 
[2020-11-27 16:09:54,968] [6912] [INFO] Reporting span 4f4eae4f74d9a5a5:8b0886193ca0fa4c:0:1 counter.send-event 
[2020-11-27 16:09:54,969] [6912] [WARNING] ids ['30', '32', '33', '34', '37'] 
[2020-11-27 16:09:54,970] [6912] [WARNING] Updated just f last 40 {'f'} 
[2020-11-27 16:09:54,970] [6912] [WARNING] {'uber-trace-id': '85d9bc698b98d56:a8e8b64a80dce494:0:1'} 
[2020-11-27 16:09:54,971] [6912] [INFO] Reporting span 85d9bc698b98d56:7e738e3ff4bfee9:a8e8b64a80dce494:1 counter.send 
[2020-11-27 16:09:54,972] [6912] [WARNING] a: 3 
[2020-11-27 16:09:54,972] [6912] [WARNING] b: 3 
[2020-11-27 16:09:54,973] [6912] [WARNING] f: 5 
[2020-11-27 16:09:54,973] [6912] [INFO] Reporting span 85d9bc698b98d56:24e548f29af224ba:a8e8b64a80dce494:1 counter.print-table 
[2020-11-27 16:09:54,973] [6912] [INFO] Reporting span 85d9bc698b98d56:a8e8b64a80dce494:0:1 counter.send-event 
[2020-11-27 16:09:54,974] [6912] [WARNING] ids ['30', '32', '33', '34', '37', '39'] 
[2020-11-27 16:09:54,975] [6912] [WARNING] Updated just f last 40 {'f'} 
[2020-11-27 16:09:54,975] [6912] [WARNING] {'uber-trace-id': '8043ef001ca4def2:f61531179d18e314:0:1'} 
[2020-11-27 16:09:54,976] [6912] [INFO] Reporting span 8043ef001ca4def2:75c982a045762891:f61531179d18e314:1 counter.send 
[2020-11-27 16:09:54,976] [6912] [WARNING] a: 4 
[2020-11-27 16:09:54,977] [6912] [WARNING] b: 4 
[2020-11-27 16:09:54,977] [6912] [WARNING] f: 6 
[2020-11-27 16:09:54,977] [6912] [INFO] Reporting span 8043ef001ca4def2:235568d544bc469d:f61531179d18e314:1 counter.print-table 
[2020-11-27 16:09:54,977] [6912] [INFO] Reporting span 8043ef001ca4def2:f61531179d18e314:0:1 counter.send-event 
[2020-11-27 16:09:54,978] [6912] [WARNING] ids ['30', '32', '33', '34', '37', '39', '43'] 
[2020-11-27 16:09:54,978] [6912] [WARNING] Updated just f last 40 {'f'} 
[2020-11-27 16:09:54,978] [6912] [WARNING] {'uber-trace-id': '49a7b3927b29cfb9:9ad2290aecc3093c:0:1'} 
[2020-11-27 16:09:54,980] [6912] [INFO] Reporting span 49a7b3927b29cfb9:da15c32cd2802ed2:9ad2290aecc3093c:1 counter.send 
[2020-11-27 16:09:54,980] [6912] [WARNING] a: 5 
[2020-11-27 16:09:54,981] [6912] [WARNING] b: 4 
[2020-11-27 16:09:54,981] [6912] [WARNING] f: 7 
[2020-11-27 16:09:54,981] [6912] [INFO] Reporting span 49a7b3927b29cfb9:66e3455b93b25ca7:9ad2290aecc3093c:1 counter.print-table 
[2020-11-27 16:09:54,981] [6912] [INFO] Reporting span 49a7b3927b29cfb9:9ad2290aecc3093c:0:1 counter.send-event 
[2020-11-27 16:09:55,354] [6912] [WARNING] ids ['30', '32', '33', '34', '37', '39', '43', '50'] 
[2020-11-27 16:09:55,355] [6912] [WARNING] Updated just f last 40 {'f'} 
[2020-11-27 16:09:55,356] [6912] [WARNING] {'uber-trace-id': 'b4391b6787839efa:78cc9c0cee962b00:0:1'} 
[2020-11-27 16:09:55,356] [6912] [INFO] Reporting span b4391b6787839efa:38ff46cd25c77013:78cc9c0cee962b00:1 counter.send 
[2020-11-27 16:09:55,357] [6912] [WARNING] a: 10 
[2020-11-27 16:09:55,357] [6912] [WARNING] b: 8 
[2020-11-27 16:09:55,357] [6912] [WARNING] f: 8 
[2020-11-27 16:09:55,357] [6912] [INFO] Reporting span b4391b6787839efa:4b183ca40fb46a46:78cc9c0cee962b00:1 counter.print-table 
[2020-11-27 16:09:55,357] [6912] [INFO] Reporting span b4391b6787839efa:78cc9c0cee962b00:0:1 counter.send-event 
[2020-11-27 16:09:56,361] [6912] [WARNING] ids ['30', '32', '33', '34', '37', '39', '43', '50', '51'] 
[2020-11-27 16:09:56,362] [6912] [WARNING] Updated just f last 40 {'f'} 
[2020-11-27 16:09:56,362] [6912] [WARNING] {'uber-trace-id': 'b4a7a6fea9d4b89e:d7afaa547e55ca53:0:1'} 
[2020-11-27 16:09:56,364] [6912] [INFO] Reporting span b4a7a6fea9d4b89e:5a5d394abeace2e0:d7afaa547e55ca53:1 counter.send 
[2020-11-27 16:09:56,365] [6912] [WARNING] a: 10 
[2020-11-27 16:09:56,365] [6912] [WARNING] b: 8 
[2020-11-27 16:09:56,366] [6912] [WARNING] f: 9 
[2020-11-27 16:09:56,366] [6912] [INFO] Reporting span b4a7a6fea9d4b89e:cb6b0ab38bb333ba:d7afaa547e55ca53:1 counter.print-table 
[2020-11-27 16:09:56,367] [6912] [INFO] Reporting span b4a7a6fea9d4b89e:d7afaa547e55ca53:0:1 counter.send-event 
[2020-11-27 16:09:57,021] [6912] [WARNING] Heartbeat failed for group count-events because it is rebalancing 
[2020-11-27 16:09:57,021] [6912] [INFO] Revoking previously assigned partitions 
(0l(BTopic Partition Set(0qqqqqqqqqqqqqqqqqqwqqqqqqqqqqqqk(B
(0x(B topic                               (0x(B partitions (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B {0-7}      (0x(B
(0x(B raw-events                          (0x(B {6-7}      (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqqj(B for group count-events 
[2020-11-27 16:09:57,029] [6912] [INFO] (Re-)joining group count-events 
[2020-11-27 16:09:57,035] [6912] [INFO] Joined group 'count-events' (generation 8) with member_id faust-0.3.0-dd5ce5a3-da6b-47e3-b404-7e3b687f46fd 
[2020-11-27 16:09:57,042] [6912] [INFO] Successfully synced group count-events with generation 8 
[2020-11-27 16:09:57,043] [6912] [INFO] Setting newly assigned partitions 
(0l(BTopic Partition Set(0qqqqqqqqqqqqqqqqqqwqqqqqqqqqqqqk(B
(0x(B topic                               (0x(B partitions (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B {0-7}      (0x(B
(0x(B raw-events                          (0x(B {6-7}      (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqqj(B for group count-events 
[2020-11-27 16:09:57,187] [6912] [INFO] [^---Recovery]: Highwater for active changelog partitions:
(0l(BHighwater - Active(0qqqqqqqqqqqqqqqqqqqwqqqqqqqqqqqwqqqqqqqqqqqk(B
(0x(B topic                               (0x(B partition (0x(B highwater (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqnqqqqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B 6         (0x(B -1        (0x(B
(0x(B 〃                                  (0x(B 7         (0x(B 8         (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqvqqqqqqqqqqqj(B 
[2020-11-27 16:09:57,197] [6912] [INFO] [^---Recovery]: active offsets at start of reading:
(0l(BReading Starts At - Active(0qqqqqqqqqqqwqqqqqqqqqqqwqqqqqqqqk(B
(0x(B topic                               (0x(B partition (0x(B offset (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqnqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B 6         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 7         (0x(B -1     (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqvqqqqqqqqj(B 
[2020-11-27 16:09:57,366] [6912] [INFO] [^---Recovery]: standby offsets at start of reading:
(0l(BReading Starts At - Standby(0qqqqqqqqqqwqqqqqqqqqqqwqqqqqqqqk(B
(0x(B topic                               (0x(B partition (0x(B offset (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqnqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B 0         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 1         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 2         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 3         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 4         (0x(B 17     (0x(B
(0x(B 〃                                  (0x(B 5         (0x(B -1     (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqvqqqqqqqqj(B 
[2020-11-27 16:09:57,368] [6912] [INFO] [^---Recovery]: Restoring state from changelog topics... 
[2020-11-27 16:09:57,368] [6912] [INFO] [^---Recovery]: Resuming flow... 
[2020-11-27 16:09:57,475] [6912] [INFO] [^---Recovery]: Done reading from changelog topics 
[2020-11-27 16:09:57,475] [6912] [INFO] [^---Recovery]: Recovery complete 
[2020-11-27 16:09:57,475] [6912] [INFO] [^---Recovery]: Starting standby partitions... 
[2020-11-27 16:09:58,983] [6912] [INFO] [^---Recovery]: Highwater for standby changelog partitions:
(0l(BHighwater - Standby(0qqqqqqqqqqqqqqqqqqwqqqqqqqqqqqwqqqqqqqqqqqk(B
(0x(B topic                               (0x(B partition (0x(B highwater (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqnqqqqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B 0         (0x(B -1        (0x(B
(0x(B 〃                                  (0x(B 1         (0x(B 2         (0x(B
(0x(B 〃                                  (0x(B 2         (0x(B -1        (0x(B
(0x(B 〃                                  (0x(B 3         (0x(B -1        (0x(B
(0x(B 〃                                  (0x(B 4         (0x(B 17        (0x(B
(0x(B 〃                                  (0x(B 5         (0x(B -1        (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqvqqqqqqqqqqqj(B 
[2020-11-27 16:09:58,984] [6912] [INFO] [^---Recovery]: Restore complete! 
[2020-11-27 16:09:58,984] [6912] [INFO] [^---Recovery]: Seek stream partitions to committed offsets. 
[2020-11-27 16:09:59,020] [6912] [INFO] [^---Recovery]: Worker ready 
[2020-11-27 16:09:59,482] [6912] [WARNING] ERROR dup vdkfjaklhaflkjashdflkjashdfkjldhaslkjfhaslk ERROR 
[2020-11-27 16:09:59,482] [6912] [WARNING] ids ['30', '32', '33', '34', '37', '39', '43', '50', '51', '51'] 
[2020-11-27 16:09:59,483] [6912] [WARNING] Updated just f last 40 {'f'} 
[2020-11-27 16:09:59,483] [6912] [WARNING] {'uber-trace-id': '20dc4594deb5304e:55995790f017d65c:0:1'} 
[2020-11-27 16:09:59,483] [6912] [INFO] Reporting span 20dc4594deb5304e:a890965b55c476d2:55995790f017d65c:1 counter.send 
[2020-11-27 16:09:59,483] [6912] [WARNING] a: 10 
[2020-11-27 16:09:59,484] [6912] [WARNING] b: 8 
[2020-11-27 16:09:59,484] [6912] [WARNING] d: 1 
[2020-11-27 16:09:59,484] [6912] [WARNING] f: 10 
[2020-11-27 16:09:59,484] [6912] [INFO] Reporting span 20dc4594deb5304e:2cf10ef1a8015a9d:55995790f017d65c:1 counter.print-table 
[2020-11-27 16:09:59,484] [6912] [INFO] Reporting span 20dc4594deb5304e:55995790f017d65c:0:1 counter.send-event 
[2020-11-27 16:09:59,484] [6912] [WARNING] ids ['30', '32', '33', '34', '37', '39', '43', '50', '51', '51', '52'] 
[2020-11-27 16:09:59,484] [6912] [WARNING] Updated just f last 40 {'f'} 
[2020-11-27 16:09:59,485] [6912] [WARNING] {'uber-trace-id': 'd2c129799bc7b98a:b12c296a3253121c:0:1'} 
[2020-11-27 16:09:59,485] [6912] [INFO] Reporting span d2c129799bc7b98a:4019aacf14d2141c:b12c296a3253121c:1 counter.send 
[2020-11-27 16:09:59,485] [6912] [WARNING] a: 10 
[2020-11-27 16:09:59,485] [6912] [WARNING] b: 8 
[2020-11-27 16:09:59,486] [6912] [WARNING] d: 1 
[2020-11-27 16:09:59,486] [6912] [WARNING] f: 11 
[2020-11-27 16:09:59,486] [6912] [INFO] Reporting span d2c129799bc7b98a:68997bb49367bb27:b12c296a3253121c:1 counter.print-table 
[2020-11-27 16:09:59,486] [6912] [INFO] Reporting span d2c129799bc7b98a:b12c296a3253121c:0:1 counter.send-event 
[2020-11-27 16:09:59,610] [6912] [WARNING] ids ['30', '32', '33', '34', '37', '39', '43', '50', '51', '51', '52', '54'] 
[2020-11-27 16:09:59,611] [6912] [WARNING] Updated just f last 40 {'f'} 
[2020-11-27 16:09:59,611] [6912] [WARNING] {'uber-trace-id': '44985a210ff16fea:bb57782a498c446f:0:1'} 
[2020-11-27 16:09:59,611] [6912] [INFO] Reporting span 44985a210ff16fea:690989603c056e68:bb57782a498c446f:1 counter.send 
[2020-11-27 16:09:59,612] [6912] [WARNING] a: 10 
[2020-11-27 16:09:59,612] [6912] [WARNING] b: 8 
[2020-11-27 16:09:59,612] [6912] [WARNING] d: 3 
[2020-11-27 16:09:59,612] [6912] [WARNING] f: 12 
[2020-11-27 16:09:59,612] [6912] [INFO] Reporting span 44985a210ff16fea:1a4b8aac1587a157:bb57782a498c446f:1 counter.print-table 
[2020-11-27 16:09:59,613] [6912] [INFO] Reporting span 44985a210ff16fea:bb57782a498c446f:0:1 counter.send-event 
[2020-11-27 16:10:05,383] [6912] [WARNING] ids ['30', '32', '33', '34', '37', '39', '43', '50', '51', '51', '52', '54', '60'] 
[2020-11-27 16:10:05,384] [6912] [WARNING] Updated just f last 40 {'f'} 
[2020-11-27 16:10:05,384] [6912] [WARNING] {'uber-trace-id': 'b94d0b53427c1b:db6c01836a3d09c3:0:1'} 
[2020-11-27 16:10:05,384] [6912] [INFO] Reporting span b94d0b53427c1b:9135af43a3d18682:db6c01836a3d09c3:1 counter.send 
[2020-11-27 16:10:05,385] [6912] [WARNING] a: 11 
[2020-11-27 16:10:05,385] [6912] [WARNING] b: 9 
[2020-11-27 16:10:05,385] [6912] [WARNING] d: 4 
[2020-11-27 16:10:05,385] [6912] [WARNING] f: 13 
[2020-11-27 16:10:05,385] [6912] [INFO] Reporting span b94d0b53427c1b:ccb12123011c4bb2:db6c01836a3d09c3:1 counter.print-table 
[2020-11-27 16:10:05,385] [6912] [INFO] Reporting span b94d0b53427c1b:db6c01836a3d09c3:0:1 counter.send-event 
[2020-11-27 16:10:06,057] [6912] [WARNING] Heartbeat failed for group count-events because it is rebalancing 
[2020-11-27 16:10:06,058] [6912] [INFO] Revoking previously assigned partitions 
(0l(BTopic Partition Set(0qqqqqqqqqqqqqqqqqqwqqqqqqqqqqqqk(B
(0x(B topic                               (0x(B partitions (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B {0-7}      (0x(B
(0x(B raw-events                          (0x(B {6-7}      (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqqj(B for group count-events 
[2020-11-27 16:10:06,060] [6912] [INFO] (Re-)joining group count-events 
[2020-11-27 16:10:06,071] [6912] [INFO] Joined group 'count-events' (generation 9) with member_id faust-0.3.0-dd5ce5a3-da6b-47e3-b404-7e3b687f46fd 
[2020-11-27 16:10:06,077] [6912] [INFO] Successfully synced group count-events with generation 9 
[2020-11-27 16:10:06,078] [6912] [INFO] Setting newly assigned partitions 
(0l(BTopic Partition Set(0qqqqqqqqqqqqqqqqqqwqqqqqqqqqqqqk(B
(0x(B topic                               (0x(B partitions (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B {0-7}      (0x(B
(0x(B raw-events                          (0x(B {3, 6-7}   (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqqj(B for group count-events 
[2020-11-27 16:10:06,894] [6912] [INFO] [^---Recovery]: Highwater for active changelog partitions:
(0l(BHighwater - Active(0qqqqqqqqqqqqqqqqqqqwqqqqqqqqqqqwqqqqqqqqqqqk(B
(0x(B topic                               (0x(B partition (0x(B highwater (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqnqqqqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B 3         (0x(B -1        (0x(B
(0x(B 〃                                  (0x(B 6         (0x(B -1        (0x(B
(0x(B 〃                                  (0x(B 7         (0x(B 12        (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqvqqqqqqqqqqqj(B 
[2020-11-27 16:10:06,905] [6912] [INFO] [^---Recovery]: active offsets at start of reading:
(0l(BReading Starts At - Active(0qqqqqqqqqqqwqqqqqqqqqqqwqqqqqqqqk(B
(0x(B topic                               (0x(B partition (0x(B offset (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqnqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B 3         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 6         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 7         (0x(B 8      (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqvqqqqqqqqj(B 
[2020-11-27 16:10:06,911] [6912] [INFO] [^---Recovery]: standby offsets at start of reading:
(0l(BReading Starts At - Standby(0qqqqqqqqqqwqqqqqqqqqqqwqqqqqqqqk(B
(0x(B topic                               (0x(B partition (0x(B offset (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqnqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B 0         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 1         (0x(B 3      (0x(B
(0x(B 〃                                  (0x(B 2         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 3         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 4         (0x(B 19     (0x(B
(0x(B 〃                                  (0x(B 5         (0x(B -1     (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqvqqqqqqqqj(B 
[2020-11-27 16:10:06,913] [6912] [INFO] [^---Recovery]: Restoring state from changelog topics... 
[2020-11-27 16:10:06,913] [6912] [INFO] [^---Recovery]: Resuming flow... 
[2020-11-27 16:10:07,011] [6912] [INFO] [^---Recovery]: Done reading from changelog topics 
[2020-11-27 16:10:07,012] [6912] [INFO] [^---Recovery]: Recovery complete 
[2020-11-27 16:10:07,012] [6912] [INFO] [^---Recovery]: Starting standby partitions... 
[2020-11-27 16:10:08,515] [6912] [INFO] [^---Recovery]: Highwater for standby changelog partitions:
(0l(BHighwater - Standby(0qqqqqqqqqqqqqqqqqqwqqqqqqqqqqqwqqqqqqqqqqqk(B
(0x(B topic                               (0x(B partition (0x(B highwater (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqnqqqqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B 0         (0x(B -1        (0x(B
(0x(B 〃                                  (0x(B 1         (0x(B 3         (0x(B
(0x(B 〃                                  (0x(B 2         (0x(B -1        (0x(B
(0x(B 〃                                  (0x(B 4         (0x(B 19        (0x(B
(0x(B 〃                                  (0x(B 5         (0x(B -1        (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqvqqqqqqqqqqqj(B 
[2020-11-27 16:10:08,515] [6912] [INFO] [^---Recovery]: Restore complete! 
[2020-11-27 16:10:08,515] [6912] [INFO] [^---Recovery]: Seek stream partitions to committed offsets. 
[2020-11-27 16:10:08,575] [6912] [INFO] [^---Recovery]: Worker ready 
[2020-11-27 16:10:09,020] [6912] [WARNING] ERROR dup vdkfjaklhaflkjashdflkjashdfkjldhaslkjfhaslk ERROR 
[2020-11-27 16:10:09,020] [6912] [WARNING] ids ['30', '32', '33', '34', '37', '39', '43', '50', '51', '51', '52', '54', '60', '60'] 
[2020-11-27 16:10:09,020] [6912] [WARNING] Updated just f last 40 {'f'} 
[2020-11-27 16:10:09,020] [6912] [WARNING] {'uber-trace-id': '663f04d91e3dc574:85881d9e71c33914:0:1'} 
[2020-11-27 16:10:09,021] [6912] [INFO] Reporting span 663f04d91e3dc574:3520a067b0414e8:85881d9e71c33914:1 counter.send 
[2020-11-27 16:10:09,021] [6912] [WARNING] a: 11 
[2020-11-27 16:10:09,021] [6912] [WARNING] b: 9 
[2020-11-27 16:10:09,021] [6912] [WARNING] d: 4 
[2020-11-27 16:10:09,022] [6912] [WARNING] f: 14 
[2020-11-27 16:10:09,022] [6912] [INFO] Reporting span 663f04d91e3dc574:134f3b952a86348f:85881d9e71c33914:1 counter.print-table 
[2020-11-27 16:10:09,022] [6912] [INFO] Reporting span 663f04d91e3dc574:85881d9e71c33914:0:1 counter.send-event 
[2020-11-27 16:10:09,090] [6912] [WARNING] Heartbeat failed for group count-events because it is rebalancing 
[2020-11-27 16:10:09,090] [6912] [INFO] Revoking previously assigned partitions 
(0l(BTopic Partition Set(0qqqqqqqqqqqqqqqqqqwqqqqqqqqqqqqk(B
(0x(B topic                               (0x(B partitions (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B {0-7}      (0x(B
(0x(B raw-events                          (0x(B {3, 6-7}   (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqqj(B for group count-events 
[2020-11-27 16:10:09,093] [6912] [INFO] (Re-)joining group count-events 
[2020-11-27 16:10:09,120] [6912] [INFO] [^---Recovery]: Highwater for active changelog partitions:
(0l(BHighwater - Active(0qqqqqqqqqqqqqqqqqqqwqqqqqqqqqqqwqqqqqqqqqqqk(B
(0x(B topic                               (0x(B partition (0x(B highwater (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqnqqqqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B 3         (0x(B -1        (0x(B
(0x(B 〃                                  (0x(B 6         (0x(B -1        (0x(B
(0x(B 〃                                  (0x(B 7         (0x(B 13        (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqvqqqqqqqqqqqj(B 
[2020-11-27 16:10:09,132] [6912] [INFO] Joined group 'count-events' (generation 10) with member_id faust-0.3.0-dd5ce5a3-da6b-47e3-b404-7e3b687f46fd 
[2020-11-27 16:10:09,142] [6912] [INFO] [^---Recovery]: active offsets at start of reading:
(0l(BReading Starts At - Active(0qqqqqqqqqqqwqqqqqqqqqqqwqqqqqqqqk(B
(0x(B topic                               (0x(B partition (0x(B offset (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqnqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B 3         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 6         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 7         (0x(B 12     (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqvqqqqqqqqj(B 
[2020-11-27 16:10:09,187] [6912] [INFO] [^---Recovery]: standby offsets at start of reading:
(0l(BReading Starts At - Standby(0qqqqqqqqqqwqqqqqqqqqqqwqqqqqqqqk(B
(0x(B topic                               (0x(B partition (0x(B offset (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqnqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B 0         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 1         (0x(B 3      (0x(B
(0x(B 〃                                  (0x(B 2         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 3         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 4         (0x(B 19     (0x(B
(0x(B 〃                                  (0x(B 5         (0x(B -1     (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqvqqqqqqqqj(B 
[2020-11-27 16:10:09,189] [6912] [INFO] Successfully synced group count-events with generation 10 
[2020-11-27 16:10:09,190] [6912] [INFO] Setting newly assigned partitions 
(0l(BTopic Partition Set(0qqqqqqqqqqqqqqqqqqwqqqqqqqqqqqqk(B
(0x(B topic                               (0x(B partitions (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B {0-7}      (0x(B
(0x(B raw-events                          (0x(B {6-7}      (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqqj(B for group count-events 
[2020-11-27 16:10:09,195] [6912] [INFO] Restarting Recovery 
[2020-11-27 16:10:09,217] [6912] [INFO] [^---Recovery]: Highwater for active changelog partitions:
(0l(BHighwater - Active(0qqqqqqqqqqqqqqqqqqqwqqqqqqqqqqqwqqqqqqqqqqqk(B
(0x(B topic                               (0x(B partition (0x(B highwater (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqnqqqqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B 6         (0x(B -1        (0x(B
(0x(B 〃                                  (0x(B 7         (0x(B 13        (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqvqqqqqqqqqqqj(B 
[2020-11-27 16:10:09,227] [6912] [INFO] [^---Recovery]: active offsets at start of reading:
(0l(BReading Starts At - Active(0qqqqqqqqqqqwqqqqqqqqqqqwqqqqqqqqk(B
(0x(B topic                               (0x(B partition (0x(B offset (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqnqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B 6         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 7         (0x(B 12     (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqvqqqqqqqqj(B 
[2020-11-27 16:10:09,249] [6912] [INFO] [^---Recovery]: standby offsets at start of reading:
(0l(BReading Starts At - Standby(0qqqqqqqqqqwqqqqqqqqqqqwqqqqqqqqk(B
(0x(B topic                               (0x(B partition (0x(B offset (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqnqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B 0         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 1         (0x(B 3      (0x(B
(0x(B 〃                                  (0x(B 2         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 3         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 4         (0x(B 19     (0x(B
(0x(B 〃                                  (0x(B 5         (0x(B -1     (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqvqqqqqqqqj(B 
[2020-11-27 16:10:09,251] [6912] [INFO] [^---Recovery]: Restoring state from changelog topics... 
[2020-11-27 16:10:09,251] [6912] [INFO] [^---Recovery]: Resuming flow... 
[2020-11-27 16:10:33,223] [6912] [WARNING] Heartbeat failed for group count-events because it is rebalancing 
[2020-11-27 16:10:33,223] [6912] [INFO] Revoking previously assigned partitions 
(0l(BTopic Partition Set(0qqqqqqqqqqqqqqqqqqwqqqqqqqqqqqqk(B
(0x(B topic                               (0x(B partitions (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B {0-7}      (0x(B
(0x(B raw-events                          (0x(B {6-7}      (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqqj(B for group count-events 
[2020-11-27 16:10:33,224] [6912] [INFO] [^---Recovery]: Done reading from changelog topics 
[2020-11-27 16:10:33,225] [6912] [INFO] (Re-)joining group count-events 
[2020-11-27 16:10:33,225] [6912] [INFO] [^---Recovery]: Recovery complete 
[2020-11-27 16:10:33,225] [6912] [INFO] [^---Recovery]: Starting standby partitions... 
[2020-11-27 16:10:33,231] [6912] [INFO] Joined group 'count-events' (generation 11) with member_id faust-0.3.0-dd5ce5a3-da6b-47e3-b404-7e3b687f46fd 
[2020-11-27 16:10:33,238] [6912] [INFO] Successfully synced group count-events with generation 11 
[2020-11-27 16:10:33,239] [6912] [INFO] Setting newly assigned partitions 
(0l(BTopic Partition Set(0qqqqqqqqqqqqqqqqqqwqqqqqqqqqqqqk(B
(0x(B topic                               (0x(B partitions (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqqu(B
(0x(B count-events-__assignor-__leader    (0x(B {0}        (0x(B
(0x(B count-events-event_counts-changelog (0x(B {0-7}      (0x(B
(0x(B raw-events                          (0x(B {4, 6-7}   (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqqj(B for group count-events 
[2020-11-27 16:10:34,597] [6912] [INFO] [^---Recovery]: Highwater for active changelog partitions:
(0l(BHighwater - Active(0qqqqqqqqqqqqqqqqqqqwqqqqqqqqqqqwqqqqqqqqqqqk(B
(0x(B topic                               (0x(B partition (0x(B highwater (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqnqqqqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B 4         (0x(B 21        (0x(B
(0x(B 〃                                  (0x(B 6         (0x(B -1        (0x(B
(0x(B 〃                                  (0x(B 7         (0x(B 13        (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqvqqqqqqqqqqqj(B 
[2020-11-27 16:10:34,608] [6912] [INFO] [^---Recovery]: active offsets at start of reading:
(0l(BReading Starts At - Active(0qqqqqqqqqqqwqqqqqqqqqqqwqqqqqqqqk(B
(0x(B topic                               (0x(B partition (0x(B offset (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqnqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B 4         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 6         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 7         (0x(B 12     (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqvqqqqqqqqj(B 
[2020-11-27 16:10:34,619] [6912] [INFO] [^---Recovery]: standby offsets at start of reading:
(0l(BReading Starts At - Standby(0qqqqqqqqqqwqqqqqqqqqqqwqqqqqqqqk(B
(0x(B topic                               (0x(B partition (0x(B offset (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqnqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B 0         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 1         (0x(B 3      (0x(B
(0x(B 〃                                  (0x(B 2         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 3         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 4         (0x(B 19     (0x(B
(0x(B 〃                                  (0x(B 5         (0x(B -1     (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqvqqqqqqqqj(B 
[2020-11-27 16:10:34,622] [6912] [INFO] [^---Recovery]: Restoring state from changelog topics... 
[2020-11-27 16:10:34,623] [6912] [INFO] [^---Recovery]: Resuming flow... 
[2020-11-27 16:10:34,742] [6912] [INFO] [^---Recovery]: Done reading from changelog topics 
[2020-11-27 16:10:34,742] [6912] [INFO] [^---Recovery]: Recovery complete 
[2020-11-27 16:10:34,742] [6912] [INFO] [^---Recovery]: Starting standby partitions... 
[2020-11-27 16:10:36,248] [6912] [INFO] [^---Recovery]: Highwater for standby changelog partitions:
(0l(BHighwater - Standby(0qqqqqqqqqqqqqqqqqqwqqqqqqqqqqqwqqqqqqqqqqqk(B
(0x(B topic                               (0x(B partition (0x(B highwater (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqnqqqqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B 0         (0x(B -1        (0x(B
(0x(B 〃                                  (0x(B 1         (0x(B 10        (0x(B
(0x(B 〃                                  (0x(B 2         (0x(B 22        (0x(B
(0x(B 〃                                  (0x(B 3         (0x(B -1        (0x(B
(0x(B 〃                                  (0x(B 5         (0x(B -1        (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqvqqqqqqqqqqqj(B 
[2020-11-27 16:10:36,249] [6912] [INFO] [^---Recovery]: Restore complete! 
[2020-11-27 16:10:36,250] [6912] [INFO] [^---Recovery]: Seek stream partitions to committed offsets. 
[2020-11-27 16:10:36,257] [6912] [WARNING] Heartbeat failed for group count-events because it is rebalancing 
[2020-11-27 16:10:36,258] [6912] [INFO] Revoking previously assigned partitions 
(0l(BTopic Partition Set(0qqqqqqqqqqqqqqqqqqwqqqqqqqqqqqqk(B
(0x(B topic                               (0x(B partitions (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqqu(B
(0x(B count-events-__assignor-__leader    (0x(B {0}        (0x(B
(0x(B count-events-event_counts-changelog (0x(B {0-7}      (0x(B
(0x(B raw-events                          (0x(B {4, 6-7}   (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqqj(B for group count-events 
[2020-11-27 16:10:36,261] [6912] [INFO] (Re-)joining group count-events 
[2020-11-27 16:10:36,270] [6912] [INFO] [^---Recovery]: Highwater for active changelog partitions:
(0l(BHighwater - Active(0qqqqqqqqqqqqqqqqqqqwqqqqqqqqqqqwqqqqqqqqqqqk(B
(0x(B topic                               (0x(B partition (0x(B highwater (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqnqqqqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B 4         (0x(B 21        (0x(B
(0x(B 〃                                  (0x(B 6         (0x(B -1        (0x(B
(0x(B 〃                                  (0x(B 7         (0x(B 13        (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqvqqqqqqqqqqqj(B 
[2020-11-27 16:10:36,282] [6912] [INFO] [^---Recovery]: active offsets at start of reading:
(0l(BReading Starts At - Active(0qqqqqqqqqqqwqqqqqqqqqqqwqqqqqqqqk(B
(0x(B topic                               (0x(B partition (0x(B offset (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqnqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B 4         (0x(B 21     (0x(B
(0x(B 〃                                  (0x(B 6         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 7         (0x(B 13     (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqvqqqqqqqqj(B 
[2020-11-27 16:10:36,284] [6912] [INFO] Joined group 'count-events' (generation 12) with member_id faust-0.3.0-dd5ce5a3-da6b-47e3-b404-7e3b687f46fd 
[2020-11-27 16:10:36,294] [6912] [INFO] [^---Recovery]: standby offsets at start of reading:
(0l(BReading Starts At - Standby(0qqqqqqqqqqwqqqqqqqqqqqwqqqqqqqqk(B
(0x(B topic                               (0x(B partition (0x(B offset (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqnqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B 0         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 1         (0x(B 3      (0x(B
(0x(B 〃                                  (0x(B 2         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 3         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 4         (0x(B 19     (0x(B
(0x(B 〃                                  (0x(B 5         (0x(B -1     (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqvqqqqqqqqj(B 
[2020-11-27 16:10:36,297] [6912] [INFO] [^---Recovery]: Resuming flow... 
[2020-11-27 16:10:36,297] [6912] [INFO] [^---Recovery]: Recovery complete 
[2020-11-27 16:10:36,297] [6912] [INFO] [^---Recovery]: Starting standby partitions... 
[2020-11-27 16:10:36,300] [6912] [INFO] Successfully synced group count-events with generation 12 
[2020-11-27 16:10:36,302] [6912] [INFO] Setting newly assigned partitions 
(0l(BTopic Partition Set(0qqqqqqqqqqqqqqqqqqwqqqqqqqqqqqqk(B
(0x(B topic                               (0x(B partitions (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqqu(B
(0x(B count-events-__assignor-__leader    (0x(B {0}        (0x(B
(0x(B count-events-event_counts-changelog (0x(B {0-7}      (0x(B
(0x(B raw-events                          (0x(B {6-7}      (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqqj(B for group count-events 
[2020-11-27 16:10:36,327] [6912] [INFO] [^---Recovery]: Highwater for active changelog partitions:
(0l(BHighwater - Active(0qqqqqqqqqqqqqqqqqqqwqqqqqqqqqqqwqqqqqqqqqqqk(B
(0x(B topic                               (0x(B partition (0x(B highwater (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqnqqqqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B 6         (0x(B -1        (0x(B
(0x(B 〃                                  (0x(B 7         (0x(B 13        (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqvqqqqqqqqqqqj(B 
[2020-11-27 16:10:36,336] [6912] [INFO] [^---Recovery]: active offsets at start of reading:
(0l(BReading Starts At - Active(0qqqqqqqqqqqwqqqqqqqqqqqwqqqqqqqqk(B
(0x(B topic                               (0x(B partition (0x(B offset (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqnqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B 6         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 7         (0x(B 13     (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqvqqqqqqqqj(B 
[2020-11-27 16:10:36,343] [6912] [INFO] [^---Recovery]: standby offsets at start of reading:
(0l(BReading Starts At - Standby(0qqqqqqqqqqwqqqqqqqqqqqwqqqqqqqqk(B
(0x(B topic                               (0x(B partition (0x(B offset (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqnqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B 0         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 1         (0x(B 3      (0x(B
(0x(B 〃                                  (0x(B 2         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 3         (0x(B -1     (0x(B
(0x(B 〃                                  (0x(B 4         (0x(B 19     (0x(B
(0x(B 〃                                  (0x(B 5         (0x(B -1     (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqvqqqqqqqqj(B 
[2020-11-27 16:10:36,345] [6912] [INFO] [^---Recovery]: Resuming flow... 
[2020-11-27 16:10:36,345] [6912] [INFO] [^---Recovery]: Recovery complete 
[2020-11-27 16:10:36,345] [6912] [INFO] [^---Recovery]: Starting standby partitions... 
[2020-11-27 16:10:36,363] [6912] [INFO] [^---Recovery]: Highwater for standby changelog partitions:
(0l(BHighwater - Standby(0qqqqqqqqqqqqqqqqqqwqqqqqqqqqqqwqqqqqqqqqqqk(B
(0x(B topic                               (0x(B partition (0x(B highwater (0x(B
(0tqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqnqqqqqqqqqqqnqqqqqqqqqqqu(B
(0x(B count-events-event_counts-changelog (0x(B 0         (0x(B -1        (0x(B
(0x(B 〃                                  (0x(B 1         (0x(B 10        (0x(B
(0x(B 〃                                  (0x(B 2         (0x(B 22        (0x(B
(0x(B 〃                                  (0x(B 3         (0x(B -1        (0x(B
(0x(B 〃                                  (0x(B 4         (0x(B 21        (0x(B
(0x(B 〃                                  (0x(B 5         (0x(B -1        (0x(B
(0mqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqvqqqqqqqqqqqvqqqqqqqqqqqj(B 
[2020-11-27 16:10:36,366] [6912] [INFO] [^---Recovery]: Restore complete! 
[2020-11-27 16:10:36,367] [6912] [INFO] [^---Recovery]: Seek stream partitions to committed offsets. 
[2020-11-27 16:10:36,441] [6912] [INFO] [^---Recovery]: Worker ready 
[2020-11-27 16:10:36,742] [6912] [WARNING] ERROR dup vdkfjaklhaflkjashdflkjashdfkjldhaslkjfhaslk ERROR 
[2020-11-27 16:10:36,742] [6912] [WARNING] ids ['30', '32', '33', '34', '37', '39', '43', '50', '51', '51', '52', '54', '60', '60', '60'] 
[2020-11-27 16:10:36,742] [6912] [WARNING] Updated just f last 40 {'f'} 
[2020-11-27 16:10:36,743] [6912] [WARNING] {'uber-trace-id': 'b2d208233addd959:b0492752c83187f3:0:1'} 
[2020-11-27 16:10:36,744] [6912] [INFO] Reporting span b2d208233addd959:6c676c1d9063ab7d:b0492752c83187f3:1 counter.send 
[2020-11-27 16:10:36,744] [6912] [WARNING] a: 13 
[2020-11-27 16:10:36,745] [6912] [WARNING] b: 9 
[2020-11-27 16:10:36,745] [6912] [WARNING] d: 4 
[2020-11-27 16:10:36,745] [6912] [WARNING] f: 15 
[2020-11-27 16:10:36,745] [6912] [INFO] Reporting span b2d208233addd959:e52b7fc5a665c9c9:b0492752c83187f3:1 counter.print-table 
[2020-11-27 16:10:36,745] [6912] [INFO] Reporting span b2d208233addd959:b0492752c83187f3:0:1 counter.send-event 
[2020-11-27 16:10:36,746] [6912] [WARNING] ids ['30', '32', '33', '34', '37', '39', '43', '50', '51', '51', '52', '54', '60', '60', '60', '71'] 
[2020-11-27 16:10:36,746] [6912] [WARNING] Updated just f last 40 {'f'} 
[2020-11-27 16:10:36,746] [6912] [WARNING] {'uber-trace-id': '97dc4a8b4724f990:1444456e40f14737:0:1'} 
[2020-11-27 16:10:36,747] [6912] [INFO] Reporting span 97dc4a8b4724f990:2a890bf1cfb42987:1444456e40f14737:1 counter.send 
[2020-11-27 16:10:36,747] [6912] [WARNING] a: 13 
[2020-11-27 16:10:36,747] [6912] [WARNING] b: 9 
[2020-11-27 16:10:36,748] [6912] [WARNING] c: 1 
[2020-11-27 16:10:36,748] [6912] [WARNING] d: 4 
[2020-11-27 16:10:36,748] [6912] [WARNING] f: 16 
[2020-11-27 16:10:36,748] [6912] [INFO] Reporting span 97dc4a8b4724f990:5580b43bc5e4e901:1444456e40f14737:1 counter.print-table 
[2020-11-27 16:10:36,748] [6912] [INFO] Reporting span 97dc4a8b4724f990:1444456e40f14737:0:1 counter.send-event 
[2020-11-27 16:10:36,749] [6912] [WARNING] ids ['30', '32', '33', '34', '37', '39', '43', '50', '51', '51', '52', '54', '60', '60', '60', '71', '81'] 
[2020-11-27 16:10:36,749] [6912] [WARNING] Updated just f last 40 {'f'} 
[2020-11-27 16:10:36,749] [6912] [WARNING] {'uber-trace-id': 'a48c4fb2dc20c8df:f00e3e438b25b952:0:1'} 
[2020-11-27 16:10:36,750] [6912] [INFO] Reporting span a48c4fb2dc20c8df:2422e849bf767080:f00e3e438b25b952:1 counter.send 
[2020-11-27 16:10:36,750] [6912] [WARNING] a: 12 
[2020-11-27 16:10:36,750] [6912] [WARNING] b: 9 
[2020-11-27 16:10:36,751] [6912] [WARNING] c: 1 
[2020-11-27 16:10:36,751] [6912] [WARNING] d: 4 
[2020-11-27 16:10:36,751] [6912] [WARNING] f: 17 
[2020-11-27 16:10:36,751] [6912] [INFO] Reporting span a48c4fb2dc20c8df:4480b0741de0f76e:f00e3e438b25b952:1 counter.print-table 
[2020-11-27 16:10:36,751] [6912] [INFO] Reporting span a48c4fb2dc20c8df:f00e3e438b25b952:0:1 counter.send-event 
[2020-11-27 16:10:36,752] [6912] [WARNING] ids ['30', '32', '33', '34', '37', '39', '43', '50', '51', '51', '52', '54', '60', '60', '60', '71', '81', '83'] 
[2020-11-27 16:10:36,752] [6912] [WARNING] Updated just f last 40 {'f'} 
[2020-11-27 16:10:36,752] [6912] [WARNING] {'uber-trace-id': '392c6cecfed21162:aeb149894b5fbce1:0:1'} 
[2020-11-27 16:10:36,753] [6912] [INFO] Reporting span 392c6cecfed21162:e4fa2b91d6dbf73:aeb149894b5fbce1:1 counter.send 
[2020-11-27 16:10:36,754] [6912] [WARNING] a: 12 
[2020-11-27 16:10:36,756] [6912] [WARNING] b: 9 
[2020-11-27 16:10:36,756] [6912] [WARNING] c: 1 
[2020-11-27 16:10:36,756] [6912] [WARNING] d: 4 
[2020-11-27 16:10:36,757] [6912] [WARNING] e: 1 
[2020-11-27 16:10:36,757] [6912] [WARNING] f: 18 
[2020-11-27 16:10:36,757] [6912] [INFO] Reporting span 392c6cecfed21162:ca5d8aea46a314b1:aeb149894b5fbce1:1 counter.print-table 
[2020-11-27 16:10:36,757] [6912] [INFO] Reporting span 392c6cecfed21162:aeb149894b5fbce1:0:1 counter.send-event 
[2020-11-27 16:10:36,758] [6912] [WARNING] ids ['30', '32', '33', '34', '37', '39', '43', '50', '51', '51', '52', '54', '60', '60', '60', '71', '81', '83', '91'] 
[2020-11-27 16:10:36,759] [6912] [WARNING] Updated just f last 40 {'f'} 
[2020-11-27 16:10:36,759] [6912] [WARNING] {'uber-trace-id': '92baf9da10e32015:433d5d82aacc3450:0:1'} 
[2020-11-27 16:10:36,760] [6912] [INFO] Reporting span 92baf9da10e32015:daf246617921816e:433d5d82aacc3450:1 counter.send 
[2020-11-27 16:10:36,760] [6912] [WARNING] a: 12 
[2020-11-27 16:10:36,761] [6912] [WARNING] b: 9 
[2020-11-27 16:10:36,761] [6912] [WARNING] c: 1 
[2020-11-27 16:10:36,761] [6912] [WARNING] d: 5 
[2020-11-27 16:10:36,761] [6912] [WARNING] e: 1 
[2020-11-27 16:10:36,761] [6912] [WARNING] f: 19 
[2020-11-27 16:10:36,761] [6912] [INFO] Reporting span 92baf9da10e32015:8e415cf773aa9999:433d5d82aacc3450:1 counter.print-table 
[2020-11-27 16:10:36,762] [6912] [INFO] Reporting span 92baf9da10e32015:433d5d82aacc3450:0:1 counter.send-event 
[2020-11-27 16:10:38,130] [6912] [WARNING] ids ['30', '32', '33', '34', '37', '39', '43', '50', '51', '51', '52', '54', '60', '60', '60', '71', '81', '83', '91', '92'] 
[2020-11-27 16:10:38,130] [6912] [WARNING] Updated just f last 40 {'f'} 
[2020-11-27 16:10:38,130] [6912] [WARNING] {'uber-trace-id': 'ebad42b4fe7c9866:76ba9a1a244e57f7:0:1'} 
[2020-11-27 16:10:38,132] [6912] [INFO] Reporting span ebad42b4fe7c9866:f40a52e236364cbe:76ba9a1a244e57f7:1 counter.send 
[2020-11-27 16:10:38,132] [6912] [WARNING] a: 13 
[2020-11-27 16:10:38,133] [6912] [WARNING] b: 9 
[2020-11-27 16:10:38,133] [6912] [WARNING] c: 14 
[2020-11-27 16:10:38,133] [6912] [WARNING] d: 12 
[2020-11-27 16:10:38,133] [6912] [WARNING] e: 9 
[2020-11-27 16:10:38,133] [6912] [WARNING] f: 20 
[2020-11-27 16:10:38,134] [6912] [INFO] Reporting span ebad42b4fe7c9866:c10db9f9c8e78a38:76ba9a1a244e57f7:1 counter.print-table 
[2020-11-27 16:10:38,134] [6912] [INFO] Reporting span ebad42b4fe7c9866:76ba9a1a244e57f7:0:1 counter.send-event 
[2020-11-27 16:10:40,482] [6912] [WARNING] ids ['30', '32', '33', '34', '37', '39', '43', '50', '51', '51', '52', '54', '60', '60', '60', '71', '81', '83', '91', '92', '95'] 
[2020-11-27 16:10:40,482] [6912] [WARNING] Updated just f last 40 {'f'} 
[2020-11-27 16:10:40,482] [6912] [WARNING] {'uber-trace-id': '8fd0fff279af7ff8:299c4d0f4f2795a0:0:1'} 
[2020-11-27 16:10:40,483] [6912] [INFO] Reporting span 8fd0fff279af7ff8:84256f9ba52ca1a6:299c4d0f4f2795a0:1 counter.send 
[2020-11-27 16:10:40,483] [6912] [WARNING] a: 19 
[2020-11-27 16:10:40,483] [6912] [WARNING] b: 13 
[2020-11-27 16:10:40,484] [6912] [WARNING] c: 17 
[2020-11-27 16:10:40,484] [6912] [WARNING] d: 12 
[2020-11-27 16:10:40,484] [6912] [WARNING] e: 9 
[2020-11-27 16:10:40,484] [6912] [WARNING] f: 21 
[2020-11-27 16:10:40,484] [6912] [INFO] Reporting span 8fd0fff279af7ff8:4a1785645e907510:299c4d0f4f2795a0:1 counter.print-table 
[2020-11-27 16:10:40,484] [6912] [INFO] Reporting span 8fd0fff279af7ff8:299c4d0f4f2795a0:0:1 counter.send-event 
[2020-11-27 16:10:45,506] [6912] [WARNING] ids ['30', '32', '33', '34', '37', '39', '43', '50', '51', '51', '52', '54', '60', '60', '60', '71', '81', '83', '91', '92', '95', '100'] 
[2020-11-27 16:10:45,506] [6912] [WARNING] Updated just f last 40 {'f'} 
[2020-11-27 16:10:45,506] [6912] [WARNING] {'uber-trace-id': '9119f38b47d33c2c:6d796b1ddcada2c7:0:1'} 
[2020-11-27 16:10:45,507] [6912] [INFO] Reporting span 9119f38b47d33c2c:10df61558b0a61f5:6d796b1ddcada2c7:1 counter.send 
[2020-11-27 16:10:45,508] [6912] [WARNING] a: 20 
[2020-11-27 16:10:45,508] [6912] [WARNING] b: 13 
[2020-11-27 16:10:45,508] [6912] [WARNING] c: 17 
[2020-11-27 16:10:45,508] [6912] [WARNING] d: 13 
[2020-11-27 16:10:45,508] [6912] [WARNING] e: 11 
[2020-11-27 16:10:45,508] [6912] [WARNING] f: 22 
[2020-11-27 16:10:45,508] [6912] [INFO] Reporting span 9119f38b47d33c2c:402b42d0c27955cb:6d796b1ddcada2c7:1 counter.print-table 
[2020-11-27 16:10:45,509] [6912] [INFO] Reporting span 9119f38b47d33c2c:6d796b1ddcada2c7:0:1 counter.send-event 
[2020-11-27 16:10:46,497] [6912] [WARNING] ids ['30', '32', '33', '34', '37', '39', '43', '50', '51', '51', '52', '54', '60', '60', '60', '71', '81', '83', '91', '92', '95', '100', '101'] 
[2020-11-27 16:10:46,498] [6912] [WARNING] Updated just f last 40 {'f'} 
[2020-11-27 16:10:46,498] [6912] [WARNING] {'uber-trace-id': '7cd4f45152d35aff:634ba57719c0582f:0:1'} 
[2020-11-27 16:10:46,498] [6912] [INFO] Reporting span 7cd4f45152d35aff:6c0eca00b9431140:634ba57719c0582f:1 counter.send 
[2020-11-27 16:10:46,499] [6912] [WARNING] a: 20 
[2020-11-27 16:10:46,499] [6912] [WARNING] b: 13 
[2020-11-27 16:10:46,499] [6912] [WARNING] c: 17 
[2020-11-27 16:10:46,499] [6912] [WARNING] d: 13 
[2020-11-27 16:10:46,499] [6912] [WARNING] e: 11 
[2020-11-27 16:10:46,499] [6912] [WARNING] f: 23 
[2020-11-27 16:10:46,499] [6912] [INFO] Reporting span 7cd4f45152d35aff:6dbce57fb1b8341a:634ba57719c0582f:1 counter.print-table 
[2020-11-27 16:10:46,500] [6912] [INFO] Reporting span 7cd4f45152d35aff:634ba57719c0582f:0:1 counter.send-event 
[2020-11-27 16:10:47,518] [6912] [WARNING] ids ['30', '32', '33', '34', '37', '39', '43', '50', '51', '51', '52', '54', '60', '60', '60', '71', '81', '83', '91', '92', '95', '100', '101', '102'] 
[2020-11-27 16:10:47,519] [6912] [WARNING] Updated just f last 40 {'f'} 
[2020-11-27 16:10:47,519] [6912] [WARNING] {'uber-trace-id': '199b1c39f2652a8d:4fcd717ea6ed0c7e:0:1'} 
[2020-11-27 16:10:47,520] [6912] [INFO] Reporting span 199b1c39f2652a8d:ed42e47320eeebae:4fcd717ea6ed0c7e:1 counter.send 
[2020-11-27 16:10:47,520] [6912] [WARNING] a: 20 
[2020-11-27 16:10:47,521] [6912] [WARNING] b: 13 
[2020-11-27 16:10:47,521] [6912] [WARNING] c: 17 
[2020-11-27 16:10:47,521] [6912] [WARNING] d: 13 
[2020-11-27 16:10:47,521] [6912] [WARNING] e: 11 
[2020-11-27 16:10:47,521] [6912] [WARNING] f: 24 
[2020-11-27 16:10:47,521] [6912] [INFO] Reporting span 199b1c39f2652a8d:cc39be51ca2a7cd3:4fcd717ea6ed0c7e:1 counter.print-table 
[2020-11-27 16:10:47,522] [6912] [INFO] Reporting span 199b1c39f2652a8d:4fcd717ea6ed0c7e:0:1 counter.send-event 
[2020-11-27 16:10:59,545] [6912] [WARNING] ids ['30', '32', '33', '34', '37', '39', '43', '50', '51', '51', '52', '54', '60', '60', '60', '71', '81', '83', '91', '92', '95', '100', '101', '102', '114'] 
[2020-11-27 16:10:59,546] [6912] [WARNING] Updated just f last 40 {'f'} 
[2020-11-27 16:10:59,546] [6912] [WARNING] {'uber-trace-id': '9872a21fdcb8c36f:2e8f1289e54f6a93:0:1'} 
[2020-11-27 16:10:59,547] [6912] [INFO] Reporting span 9872a21fdcb8c36f:36bbd16b9819ed3a:2e8f1289e54f6a93:1 counter.send 
[2020-11-27 16:10:59,547] [6912] [WARNING] a: 22 
[2020-11-27 16:10:59,547] [6912] [WARNING] b: 16 
[2020-11-27 16:10:59,547] [6912] [WARNING] c: 18 
[2020-11-27 16:10:59,548] [6912] [WARNING] d: 17 
[2020-11-27 16:10:59,548] [6912] [WARNING] e: 12 
[2020-11-27 16:10:59,548] [6912] [WARNING] f: 25 
[2020-11-27 16:10:59,548] [6912] [INFO] Reporting span 9872a21fdcb8c36f:dca0ddf9f50329f0:2e8f1289e54f6a93:1 counter.print-table 
[2020-11-27 16:10:59,548] [6912] [INFO] Reporting span 9872a21fdcb8c36f:2e8f1289e54f6a93:0:1 counter.send-event 
[2020-11-27 16:11:01,561] [6912] [WARNING] ids ['30', '32', '33', '34', '37', '39', '43', '50', '51', '51', '52', '54', '60', '60', '60', '71', '81', '83', '91', '92', '95', '100', '101', '102', '114', '116'] 
[2020-11-27 16:11:01,561] [6912] [WARNING] Updated just f last 40 {'f'} 
[2020-11-27 16:11:01,562] [6912] [WARNING] {'uber-trace-id': 'eda2bedba14d32fe:b6e26b034596129:0:1'} 
[2020-11-27 16:11:01,563] [6912] [INFO] Reporting span eda2bedba14d32fe:24dad8dc562bbc4e:b6e26b034596129:1 counter.send 
[2020-11-27 16:11:01,563] [6912] [WARNING] a: 22 
[2020-11-27 16:11:01,564] [6912] [WARNING] b: 16 
[2020-11-27 16:11:01,564] [6912] [WARNING] c: 19 
[2020-11-27 16:11:01,564] [6912] [WARNING] d: 17 
[2020-11-27 16:11:01,564] [6912] [WARNING] e: 12 
[2020-11-27 16:11:01,564] [6912] [WARNING] f: 26 
[2020-11-27 16:11:01,565] [6912] [INFO] Reporting span eda2bedba14d32fe:b327f0c6d38ddf13:b6e26b034596129:1 counter.print-table 
[2020-11-27 16:11:01,565] [6912] [INFO] Reporting span eda2bedba14d32fe:b6e26b034596129:0:1 counter.send-event 

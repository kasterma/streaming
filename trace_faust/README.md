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
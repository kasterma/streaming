# debugging a Faust program

Run a simple Faust example, and collect tracing data about the data flow that results.

0. kafka docker-compose
   copy-paste from other dir + version update

1. make example; Faust flow
     generator different events
     count types of events; asyncio with random sleep, and sometimes an error
     check if N more, then emit a message
        
     G --{a,a,b,b,c,a,b,c,d}--> C --{a:1, a:2, b:1, b:2, c:1}--> A --{there were 10 a's, there were 10 b's}-->



[WARNING] [^-App]: Missing sensor state for rebalance #1 


---------------------------------------------------------


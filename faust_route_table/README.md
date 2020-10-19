# faust example using table_route

    make venv
    make up
    make topics
    make run/generator
    WEB_PORT=6668 make run/worker
    WEB_PORT=6669 make run/worker
    make query  <-- doesn't give the expected answers
    
    git clone https://github.com/robinhood/faust.git
    git checkout v1.10.3    (pip installs 1.10.4 but there is no such tag on github)
    pip install -e .        with venv in table_route example active, then can put debug prints to see values in the code
    
    
## inside pycharm

Ensure have docker-compose installed

Then add run configuration for docker-compose file.

Ensure have Makefile plugin installed, run and save make topics, list-topics, query, run/generator
Create the different make run/worker with argument `WEB_PORT=6668` (and similar for other workers)

Created venv with make venv, but now need the checked out faust code installed there.  So go to other project
with this venv active and `pip install -e .` there.  Put `print("XXXXXXXXXXXXXXXXXXX")` or some such in `App.__init__`
and start a worker.  Should see the string first thing, then the working setup is present.

Issue: lots of failed encoding in output window.

## hellohello-0

    >>> murmur2(b'hellohello-0')%8
    3
    >>> murmur2(b'"hellohello-0"')%8
    4
    
But when sending in the changelog topic we get

    key = b'"hellohello-0"'
    parition = 3
    
    key = b'"hellohello-5"'
    partition = 2 == murmur2(b'hellohello-5') % 8  # murmur2(b'"hellohello-5"') == 4
    
See this by putting a breakpoint on aiokafka.py L 1044, self._send_on_produce_message().


1. table.py:l.73:in on_key_set, call partition_for_key(key)
2. in self.partition_for_key(key) we call event = current_event() and take the partition from it

## hello_topic.send(key=x, val=x)

get_codec("json").dumps("hello") == b'"hello"'
get_codec("raw").dumps("hello") == b'hello'

It seems like the default codec is json in some places and raw elsewhere.
No: the (json) below is set somewhere explicitly (there are four values that can be *default*, the parens
indicate the serializer)

get-hello-hello_counts-changelog.prepare_key(hellohello-8, json, <Schema: KT=*default* (json) VT=*default* (json)>, {}) = (b'"hellohello-8"', {})
hellos-here.prepare_key(hellohello-6, None, <Schema: KT=*default* (*default*) VT=*default* (*default*)>, {}) = (b'hellohello-6', {})
Q: how to make it explicit?
Q: where are these defaults set?

## how to set the schema for a table?

CollectionT has schema in its __init__

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
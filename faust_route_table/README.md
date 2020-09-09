# faust example using table_route

make up
make topic
make run/generator
WEB_PORT=6668 make run/worker
WEB_PORT=6669 make run/worker
make query  <-- doesn't give the expected answers
testing the setup for a log topic

generate events in order per partition
collect these in a list, appending to mem[parition]
then can check at any stage that state is [0, 1, ...., n] with maybe repetitions, but no missing
then go to town on this with restarting all over the place

# kafkacat -b localhost:9092 -t get-hello-hello_counts-changelog -f 'Topic %t[%p], offset: %o, key: %k, payload: %S bytes: %s\n' > hello-counts-changelog-listing.txt
# kafkacat -b localhost:9092 -t hellos-here -f 'Topic %t[%p], offset: %o, key: %k, payload: %S bytes: %s\n' > hellos-here-listing.txt

import os
os.chdir("faust_route_table")
hello_counts_changelog_filename = "hello-counts-changelog-listing.txt"
with open(hello_counts_changelog_filename) as f:
    hcc = f.readlines()
hellos_here_filename = "hellos-here-listing.txt"
with open(hellos_here_filename) as f:
    hh = f.readlines()

import re

part_key = re.compile("[^]]*\[([^]]*)\].*key: ([^,]*),.*")

from collections import defaultdict

def get_table(lines):
    d = defaultdict(set)
    for line in lines:
        m = part_key.match(line)
        d[m.group(1)].add(m.group(2))
    return d

get_table(hh)
get_table(hcc)

# get_table(hh)
# defaultdict(<class 'set'>, {'0': {'hellohello-4'}, '2': {'hellohello-5'}, '3': {'hellohello-0'}, '4': {'hellohello-8', 'hellohello-9'}, '5': {'hellohello-1'}, '6': {'hellohello-2'}, '7': {'hellohello-7', 'hellohello-3', 'hellohello-6', 'hellohello-10'}})
# get_table(hcc)
# defaultdict(<class 'set'>, {'0': {'"hellohello-4"'}, '2': {'"hellohello-5"'}, '3': {'"hellohello-0"'}, '4': {'"hellohello-9"', '"hellohello-8"'}, '5': {'"hellohello-1"'}, '6': {'"hellohello-2"'}, '7': {'"hellohello-3"', '"hellohello-10"', '"hellohello-6"', '"hellohello-7"'}})

from kafka.partitioner.hashed import murmur2

murmur2(b"\"hellohello-5\"") % 8
murmur2(b"hellohello-5") % 8

def make_table(quotes=True):
    d = defaultdict(set)
    for i in range(10):
        s = f"hellohello-{i}"
        if quotes:
            b = bytes(s, 'ascii')
        else:
            b = s.encode('ascii')
        d[murmur2(b)%8].add(b)
    return d

make_table()

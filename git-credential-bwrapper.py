#!/usr/bin/env python

import sys
import subprocess
import json

OUT_ATTRIBUTES = ['username', 'password']

if sys.argv[1] != 'get':
    exit(0)

info = {}
for line in sys.stdin:
    line = line.rstrip()
    if line == '':
        break
    splitted_line = line.split('=', 1)
    info[splitted_line[0]] = splitted_line[1]

#TODO: check protocol

base_domain = info['host'].split('.')[-2]

process = subprocess.run(['bw', 'get', 'item', base_domain],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
#TODO: check stderr
bw_item = json.loads(process.stdout)

for attr in OUT_ATTRIBUTES:
    try:
        print(attr + '=' + bw_item['login'][attr])
    except KeyError:
        exit(0)


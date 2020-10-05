#!/usr/bin/env python

import sys
import subprocess
import json
import logging
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('operation', metavar='OP', type=str, help="git credential operation, only get is supported")
parser.add_argument('--debug', action='store_true')
args = parser.parse_args()

if args.operation != 'get':
    logging.debug("Wrong operation: " + args.operation)
    exit(0)

if args.debug:
    logging.basicConfig(level=logging.DEBUG)

def check_bw_status():
    logging.debug("Checking Bitwarden status...")
    process = subprocess.run(['bw', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    logging.debug("Bitwarden output:\n\tstdout: {}\n\tstderr: {}".format(process.stdout.decode('utf-8'),
                                                                     process.stderr.decode('utf-8')))
    try:
        bw_status = json.loads(process.stdout)
        if bw_status['status'] != 'unlocked':
            print("Warning: cannot access vault, your vault is {}".format(bw_status['status']), file=sys.stderr)
    except json.decoder.JSONDecodeError:
        print("Warning: no valid bw CLI found", file=sys.stderr)

OUT_ATTRIBUTES = ['username', 'password']

def output_out_attributes(bw_item):
    for attr in OUT_ATTRIBUTES:
        try:
            print(attr + '=' + bw_item['login'][attr])
        except KeyError:
            exit(0)

def get_git_config_email():
    command = ['git', 'config', 'user.email']
    process = subprocess.run(command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    return process.stdout.decode('utf-8').rstrip()

def select_item(bw_items, base_domain):
    email = get_git_config_email()
    logging.debug("git config user.email: {}".format(email))
    for bw_item in bw_items:
        username = bw_item['login']['username']
        logging.debug("bw item with username: {}".format(username))
        if email == username:
            return bw_item
    print("Warning: several items for {} but no items matching {} the email in git config".format(base_domain, email), file=sys.stderr)
    exit(0)

info = {}
for line in sys.stdin:
    line = line.rstrip()
    if line == '':
        break
    splitted_line = line.split('=', 1)
    info[splitted_line[0]] = splitted_line[1]

logging.debug("Received information from git:\n\t{}".format(info))

#TODO: check protocol

base_domain = info['host'].split('.')[-2]
command = ['bw', 'list', 'items', '--search', base_domain]

logging.debug("Bitwarden query: {}".format(' '.join(command)))

process = subprocess.run(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

logging.debug("Bitwarden output:\n\tstdout: {}\n\tstderr: {}".format(process.stdout.decode('utf-8'),
                                                                 process.stderr.decode('utf-8')))

#TODO: check stderr

try:
    bw_items = json.loads(process.stdout)
except json.decoder.JSONDecodeError:
    check_bw_status()
    exit(0)

if len(bw_items) == 0:
    print("Warning: no items for base domain {} in vault".format(base_domain), file=sys.stderr)
elif len(bw_items) == 1:
    output_out_attributes(bw_items[0])
else:
    bw_item = select_item(bw_items, base_domain)
    output_out_attributes(bw_item)



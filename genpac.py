#!/usr/bin/env python3

import argparse
import base64
import binascii
import json
import logging
import os
import re
import urllib.parse
import urllib.request

prog = 'GenPAC'
desc = 'generate PAC file from gfwlist and user-rules'
version = '0.1'
logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

default_gfwlist_url = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'
args_dict = {}


def update_args():
    if urllib.parse.urlparse(args_dict['gfwlist']).scheme == '':
        args_dict['gfwlist'] = 'file://' + \
            os.path.abspath(args_dict['gfwlist'])
    args_dict['proxy'] = args_dict['proxy'].strip()
    if not args_dict['proxy'].endswith(';'):
        args_dict['proxy'] += ';'
    args_dict['gfwlist'] = urllib.parse.urlparse(args_dict['gfwlist'])


def get_gfwlist():
    # req = urllib.request.Request(gfwlist_url)
    try:
        with urllib.request.urlopen(args_dict['gfwlist'].geturl()) as f:
            base64_string = f.read().decode('utf-8').rstrip()
            return base64_string
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        logging.error(
            'Error {} occured when retrieving gfwlist from "{}"'.format(e, args_dict['gfwlist'].geturl()))


def generate_pac():
    gfwlist_base64 = get_gfwlist()
    if gfwlist_base64 == None:
        return
    try:
        gfwlist = base64.b64decode(gfwlist_base64).decode('utf-8')
        lines = gfwlist.split('\n')
        if args_dict['user_rule'] != None:
            userRuleString = args_dict['user_rule'].read()
            userRuleLines = userRuleString.split('\n')
            # ignore rules confict with user rules
            lines = userRuleLines + list(filter(lambda line: line not in userRuleLines and
                                                line.lstrip('@@') not in userRuleLines and
                                                ('@@' + line) not in userRuleLines, lines))
        # filter empty and comment lines
        lines = list(filter(lambda s: s.strip() !=
                            '' and not re.match(r'^[!\[].*', s.lstrip()), lines))

        # rule lines to json array
        ruleJsonString = json.dumps(lines, indent=2)

        # get raw pac js
        jsString = None
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pac_template.js'), 'r') as f:
            jsString = f.read()
        jsString = jsString.replace('__RULES__', ruleJsonString)
        jsString = jsString.replace('__PROXY__', args_dict['proxy'])

        # write to output
        with open(args_dict['output'], 'w') as f:
            f.write(jsString)
            return True
    except binascii.Error as e:
        logging.error('Error <{}> occured when decoding gfwlist'.format(e))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=prog, description=desc)
    parser.add_argument('-v', '--version', action='version',
                        version='{} {}'.format(prog, version))
    parser.add_argument('-g', '--gfwlist', type=str, required=False,
                        default=default_gfwlist_url,
                        help='a local path or remote url to the gfwlist encoded in base64')
    parser.add_argument('-u', '--user-rule', type=argparse.FileType('r'),
                        required=False, metavar='/path/to/user-rule',
                        help='the file contains user rules')
    parser.add_argument('--log-level', type=str, required=False, metavar='LEVEL',
                        default='INFO',
                        choices=['DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL'],
                        help='the value must be "DEBUG", "INFO" (default), "WARN", "ERROR" or "FATAL')
    parser.add_argument('-p', '--proxy', type=str, required=True,
                        help='proxy string in PAC file')
    parser.add_argument('output', type=str,
                        help='the path to the output PAC file')
    args = parser.parse_args()
    args_dict = vars(args)
    update_args()
    # if validate_args == False:
    #     exit()
    logging.getLogger().setLevel(getattr(logging, args_dict['log_level']))
    logging.debug('args: {}'.format(args_dict))

    if generate_pac():
        logging.info('Generate PAC: Succeeded')
    else:
        logging.warn('Generate PAC: Failed')

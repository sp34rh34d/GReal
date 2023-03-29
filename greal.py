#!/usr/bin/env python3

from core.core import *
from core.GRealRCPT import *
import argparse

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-d','--domain',help='Set target domain')
parser.add_argument('-f','--firtsname-list',default='wordlist/firstname.txt',help='Set firtsname list file')
parser.add_argument('-l','--lastname-list',default='wordlist/lastname.txt',help='Set lastname list file')
parser.add_argument('--format',default="1",help="Set what kind of email format use for enumeration")
parser.add_argument('-t','--threads',default='10',help='Set threads')
parser.add_argument('mode',help='Set attack mode (rcpt,vrfy,extn)')
parser.add_argument('-h','--help',action='store_true',help="")
parser.add_argument('-k','--mail-rate',action='store_true',help="ignore 'OK' response and show only email with 'receiving mail at a rate ' status")
args = parser.parse_args()
ATTACK_MODE=args.mode

if ATTACK_MODE == 'rcpt':
	RCPT_MODULE.main(args)



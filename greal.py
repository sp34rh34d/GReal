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
args = parser.parse_args()
ATTACK_MODE=args.mode

if ATTACK_MODE == 'rcpt':
	RCPT_MODULE.main(args)

# from telnetlib import Telnet
# from smtplib import SMTP
# import pydig
# import validators
# import sys


# domain = "kapa7.com"

# if not validators.domain(domain):
# 	print(f'{TerminalColor.Red}Invalid domain! {TerminalColor.Reset}')
# 	sys.exit()

# mx_server_list=pydig.query(domain, 'MX')

# if mx_server_list:
# 	for mx in mx_server_list:
# 		print(f'[{TerminalColor.Green}+{TerminalColor.Reset}] {mx}')

# mx_server=input("select MX from list:")

# server=SMTP(mx_server)
# server.ehlo(domain)
# server.docmd(f'MAIL FROM:<test@{domain}>')

# cont=True
# while cont:
# 	target_account=input("target account:")
# 	# server.set_debuglevel(1)
# 	result=str(server.docmd(f'RCPT TO:<{target_account}@{domain}>'))

# 	if "not exist." in result:
# 		print('account not detected')
# 	else:
# 		print(f'Output: {result}')

# 	if input('continuar y/n: ')=='n':
# 		cont=False



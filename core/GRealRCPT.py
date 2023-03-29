from telnetlib import Telnet
from smtplib import SMTP
import pydig
import validators
import concurrent.futures
import sys
from core.core import *

class RCPT_OPTIONS:
	MODULE_NAME="RCPT Email enumeration mode"
	TARGET_DOMAIN=""
	FIRSTNAME_LIST=""
	LASTNAME_LIST=""
	TARGET_MX=""
	THREADS=10
	FORMAT=""
	MAIL_RATE=False
	HELP=False

class RCPT_MODULE:
	def main(args):
		RCPT_OPTIONS.TARGET_DOMAIN=args.domain
		RCPT_OPTIONS.FIRSTNAME_LIST=args.firtsname_list
		RCPT_OPTIONS.LASTNAME_LIST=args.lastname_list
		RCPT_OPTIONS.HELP=args.help 
		RCPT_OPTIONS.FORMAT=args.format
		RCPT_OPTIONS.MAIL_RATE=args.mail_rate

		if RCPT_OPTIONS.HELP:
			RCPT_HELP.Help()

		if not RCPT_OPTIONS.TARGET_DOMAIN:
			print(f'{TerminalColor.Red}Target domain is requered!{TerminalColor.Reset}')
			sys.exit()

		if not RCPT_OPTIONS.FIRSTNAME_LIST:
			RCPT_OPTIONS.FIRSTNAME_LIST="wordlist/firstname.txt"

		if not RCPT_OPTIONS.LASTNAME_LIST:
			RCPT_OPTIONS.LASTNAME_LIST="wordlist/lastname.txt"

		if not validators.domain(RCPT_OPTIONS.TARGET_DOMAIN):
			print(f'{TerminalColor.Red}Invalid domain!{TerminalColor.Reset}')
			sys.exit()

		Core.Banner()
		RCPT_MODULE.Banner()

		print(f"{TerminalColor.Orange}Getting MX servers for {RCPT_OPTIONS.TARGET_DOMAIN}{TerminalColor.Reset} ")
		mx_server_list=[]
		mx_server_list=pydig.query(RCPT_OPTIONS.TARGET_DOMAIN, 'MX')
		if mx_server_list:
			for mx in mx_server_list:
				print(f'[{TerminalColor.Green}+{TerminalColor.Reset}] {mx}')

		RCPT_OPTIONS.TARGET_MX=input(f"{TerminalColor.Orange}Select MX server:{TerminalColor.Reset} ")

		if not RCPT_OPTIONS.TARGET_MX:
			print(f'{TerminalColor.Red}Invalid MX server!{TerminalColor.Reset}')
			sys.exit()

		try:
			SMTP_SERVER = SMTP(RCPT_OPTIONS.TARGET_MX)
			SMTP_SERVER.ehlo(RCPT_OPTIONS.TARGET_DOMAIN)
		except:
			print(f'{TerminalColor.Red}Invalid connection to MX server {RCPT_OPTIONS.TARGET_MX}!{TerminalColor.Reset}')
			sys.exit()
		
		if not RCPT_OPTIONS.MAIL_RATE:
			if RCPT_TASK.NonExistingEmail():
				sys.exit()

		RCPT_TASK.Threads()

	def Banner():
		Message=f"""- Target domain: {TerminalColor.Green}{RCPT_OPTIONS.TARGET_DOMAIN}{TerminalColor.Reset}
- Attack mode: {TerminalColor.Green}{RCPT_OPTIONS.MODULE_NAME}{TerminalColor.Reset}
- Format: {TerminalColor.Green}{RCPT_OPTIONS.FORMAT}{TerminalColor.Reset}
- Threads: {TerminalColor.Green}{RCPT_OPTIONS.THREADS}{TerminalColor.Reset}"""

		if RCPT_OPTIONS.FORMAT=="1" or RCPT_OPTIONS.FORMAT=="2":
			Message=f"""{Message}
- Firstname file: {TerminalColor.Green}{RCPT_OPTIONS.FIRSTNAME_LIST}{TerminalColor.Reset}
- Lastname file: {TerminalColor.Green}{RCPT_OPTIONS.LASTNAME_LIST}{TerminalColor.Reset}"""

		if RCPT_OPTIONS.FORMAT=="3" or RCPT_OPTIONS.FORMAT=="4":
			Message=f"""{Message}
- Lastname file: {TerminalColor.Green}{RCPT_OPTIONS.LASTNAME_LIST}{TerminalColor.Reset}"""
		
		if RCPT_OPTIONS.FORMAT=="5":
			Message=f"""{Message}
- Firstname file: {TerminalColor.Green}{RCPT_OPTIONS.FIRSTNAME_LIST}{TerminalColor.Reset}"""

		print(f"""{Message}
======================================================================================================""")


class RCPT_TASK:
	def Threads():
		if RCPT_OPTIONS.FORMAT=="1":
			account_list=RCPT_TASK.Format1()
		if RCPT_OPTIONS.FORMAT=="2":
			account_list=RCPT_TASK.Format2()
		if RCPT_OPTIONS.FORMAT=="3":
			account_list=RCPT_TASK.Format3()
		if RCPT_OPTIONS.FORMAT=="4":
			account_list=RCPT_TASK.Format4()
		if RCPT_OPTIONS.FORMAT=="5":
			account_list=RCPT_TASK.Format5()

		with concurrent.futures.ThreadPoolExecutor(max_workers=int(RCPT_OPTIONS.THREADS)) as executor:
			future_to_url = {executor.submit(RCPT_TASK.Run,account): account for account in account_list}

			for future in concurrent.futures.as_completed(future_to_url):
				future.result()

	def NonExistingEmail():
		try:
			print(f"[{TerminalColor.Blue}!{TerminalColor.Reset}] {TerminalColor.Orange}Testing MX server for non existing email response...{TerminalColor.Reset}")
			SMTP_SERVER = SMTP(RCPT_OPTIONS.TARGET_MX)
			SMTP_SERVER.ehlo(RCPT_OPTIONS.TARGET_DOMAIN)
			SMTP_SERVER.docmd(f'MAIL FROM:<test@{RCPT_OPTIONS.TARGET_DOMAIN}>')
			RESULT=str(SMTP_SERVER.docmd(f'RCPT TO:<wakk4k23lem23@{RCPT_OPTIONS.TARGET_DOMAIN}>'))

			if "OK" in RESULT:
				print(f'{TerminalColor.Red}The MX server [{RCPT_OPTIONS.TARGET_MX}] response with status OK for non existing email.{TerminalColor.Reset}')
				print(f'{TerminalColor.Orange}Try adding -k arg, example: ./greal rcpt -d {RCPT_OPTIONS.TARGET_DOMAIN} --format {RCPT_OPTIONS.FORMAT} -k {TerminalColor.Reset}')
				return True
					
		except:
			pass

	def Format1():
		f = open(RCPT_OPTIONS.FIRSTNAME_LIST,'r')
		account_list=[]

		for name in f.read().split('\n'):
			if name:
				l = open(RCPT_OPTIONS.LASTNAME_LIST,'r')
				for lastname in l.read().split('\n'):
					if lastname:
						account_list.append(f'{name}.{lastname}')

		return account_list


	def Format2():
		f = open(RCPT_OPTIONS.FIRSTNAME_LIST,'r')
		account_list=[]

		for name in f.read().split('\n'):
			if name:
				l = open(RCPT_OPTIONS.LASTNAME_LIST,'r')
				for lastname in l.read().split('\n'):
					if lastname:
						account_list.append(f'{name}{lastname}')

		return account_list

	def Format3():
		letters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
		account_list=[]

		for letter in letters:
			l = open(RCPT_OPTIONS.LASTNAME_LIST,'r')
			for lastname in l.read().split('\n'):
				if lastname:
					account_list.append(f'{letter}.{lastname}')

		return account_list

	def Format4():
		letters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
		account_list=[]

		for letter in letters:
			l = open(RCPT_OPTIONS.LASTNAME_LIST,'r')
			for lastname in l.read().split('\n'):
				if lastname:
					account_list.append(f'{letter}{lastname}')

		return account_list

	def Format5():
		f = open(RCPT_OPTIONS.FIRSTNAME_LIST,'r')
		account_list=[]

		for name in f.read().split('\n'):
			if name:
				account_list.append(name)

		return account_list


	def Run(account=""):
		try:
			print(f'processing: {account}@{RCPT_OPTIONS.TARGET_DOMAIN}                                                   ',end="\r")
			SMTP_SERVER = SMTP(RCPT_OPTIONS.TARGET_MX)
			SMTP_SERVER.ehlo(RCPT_OPTIONS.TARGET_DOMAIN)
			SMTP_SERVER.docmd(f'MAIL FROM:<test@{RCPT_OPTIONS.TARGET_DOMAIN}>')
			RESULT=str(SMTP_SERVER.docmd(f'RCPT TO:<{account}@{RCPT_OPTIONS.TARGET_DOMAIN}>'))

			if RCPT_OPTIONS.MAIL_RATE:
				if "receiving mail at a rate" in RESULT:
					print(f'[{TerminalColor.Green}+{TerminalColor.Reset}] {TerminalColor.Green}{account}@{RCPT_OPTIONS.TARGET_DOMAIN}{TerminalColor.Reset}                                                                            ')
			else:

				if not "not exist." in RESULT and not "Access denied." in RESULT:
					if "Server busy." in RESULT:
						print(f'{TerminalColor.Red}The MX server [{RCPT_OPTIONS.TARGET_MX}] response with status 500 Server busy, please try later.{TerminalColor.Reset}')
						sys.exit()
					print(f'[{TerminalColor.Green}+{TerminalColor.Reset}] {TerminalColor.Green}{account}@{RCPT_OPTIONS.TARGET_DOMAIN}{TerminalColor.Reset}                                                                            ')
		except:
			pass

class RCPT_HELP:
	def Help():
		print("""RCPT Enumeration mode - Help menu

Uses RCPT enumeration mode

Usage:
  python3 greal.py rcpt [args]

Args
	-d, --domain              set target domain (required)
	-f, --firstname-list      set firstname list file
	-l, --lastname-list       set lastname list file
	-t, --threads             set threads
	    --format              set what kind of email format use for enumeration
		                      [ 1 - Firstname.Lastname ]
		                      [ 2 - FirstnameLastname ]
		                      [ 3 - F.Lastname ]
		                      [ 4 - FLastname ]
		                      [ 5 - firstname ]

	-k, --mail-rate           Ignore 'OK' response and show only email with 'receiving mail at a rate ' status response
	-h, --help                show this message

Examples:

	rcpt enumeration email format [ Firstname.Lastname ]
	use: python3 greal.py rcpt -d domain.com --format 1 -f wordlist/firstname.txt -l wordlist/lastname.txt

	rcpt enumeration email format [ FLastname ]
	use: python3 greal.py rcpt -d domain.com --format 4 -l wordlist/lastname.txt

	rcpt enumeration email format [ Firstname ]
	use: python3 greal.py rcpt -d domain.com --format 5 -f wordlist/firstname.txt

				""")
		sys.exit()


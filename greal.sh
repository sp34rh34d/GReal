#!/bin/bash

cBlack='\033[0;30m'
cRed='\033[0;31m'
cGreen='\033[0;32m'
cOrange='\033[0;33m'
cBlue='\033[0;34m'
cPurple='\033[0;35m'
cCyan='\033[0;36m'
cLightGray='\033[0;37m'
cDarkGray='\033[1;30m'
cLightRed='\033[1;31m'
cLightGreen='\033[1;32m'
cYellow='\033[1;33m'
cLightBlue='\033[1;34m'
cLightPurple='\033[1;35m'
cLightCyan='\033[1;36m'
cWhite='\033[1;37m'
cNothing='\033[0m'

while getopts d:i:f:l:I:F:L:h: option
do 
    case "${option}"
        in
        d)domain=${OPTARG};;
        f)firstname=${OPTARG};;
				l)lastname=${OPTARG};;
				i)initial=${OPTARG};;
			  I)initialFile=${OPTARG};;
				F)firstnameFile=${OPTARG};;
				L)lastnameFile=${OPTARG};;
				?|h)
				echo -e """
				-d: set domain
				-f: set first name 
				-l: set last name
				-i: set initials letter for search
				-I: set file with initials letter for search
				-F: set file with first name list
				-L: set file with last name list
				-h: show this message

				use: ./greal -d example.com -f adonis -l izaguirre
				use: ./greal -d example.com -F nombres.txt -L apellidos.txt
				use: ./greal -d example.com -f adonis -L apellidos.txt
				use: ./greal -d example.com -F nombres.txt -l izaguirre
				use: ./greal -d example.com -i a -l izaguirre
				use: ./greal -d example.com -I iniciales.txt -l izaguirre
				use: ./greal -d example.com -i a -L apellidos.txt
				use: ./greal -d example.com -I iniciales.txt -L apellidos.txt

				"""
				exit 1
				;;
    esac
done

echo -e """
 .d8888b.  8888888b.                    888 
d88P  Y88b 888   Y88b                   888 
888    888 888    888                   888 
888        888   d88P  .d88b.   8888b.  888 
888  88888 8888888P'  d8P  Y8b     '88b 888 
888    888 888 T88b   88888888 .d888888 888 
Y88b  d88P 888  T88b  Y8b.     888  888 888 
 'Y8888P88 888   T88b  'Y8888  'Y888888 888

Coded by:$cRed Adonis Izaguirre$cNothing Email:$cRed adonis.izaguirre@kapa7.com $cNothing
Welcome to GReal, Gmail/Gsuite account enumeration tool!"""

function GetMX(){
	echo -e $cNothing"===============Getting MX registers============="$cOrange
  if [[ $(dig +short MX $1 | awk '{print $2}' | wc -l) -gt 0 ]];
  then
  	dig +short MX $1 | awk '{print $2}' | nl
  	echo -e $cNothing
  else
  	echo -e $cRed"No MX found!"$cNothing
  	exit 1
  fi;
}

function CheckFirstname(){
	if [ -z "$firstname" ] && [ -z "$firstnameFile" ] && [ -z "$initial" ] && [ -z "$initialFile" ];
	then
			echo -e $cRed"No args detected for first name!"$cNothing
			exit 1
	fi;
}

function CheckLastname(){
	if [ -z "$lastname" ] && [ -z "$lastnameFile" ];
	then
			echo -e $cRed"No args detected for last name!"$cNothing
			exit 1
	fi;
}

GetMX $domain
read -e -p "Select MX from list (mx1.example.com): " MX
if [ -z "$MX" ];
then
	echo -e $cRed"No MX selected!"$cNothing
	exit 1
fi;

port=25
function CheckMXPort(){
	echo -e $cOrange"checking $MX SMTP port"$cNothing
	if curl -s --connect-timeout 5 -k "$MX:25";then
		echo -e $cGreen"Port 25 OK!"$cNothing
	elif curl -s --connect-timeout 5 -k "$MX:465";then
		echo -e $cGreen"Port 465 OK!"$cNothing
		port=465
	elif curl -s --connect-timeout 5 -k "$MX:587";then
		echo -e $cGreen"Port 587 OK!"$cNothing
		port=587
	else
		echo -e $cRed"No port detected or server is refusing our connection!"
		exit 1
	fi;
}

CheckMXPort
CheckFirstname
CheckLastname

echo "" > accounts.list

function Query(){
echo -ne $cOrange"\rchecking account: {$1}                        "$cNothing
curl --output query.txt --connect-timeout 5 -s -k "telnet://$MX:$port" <<EOF
EHLO $domain
MAIL FROM:<$1>
RCPT TO:<$1>
quit
EOF
}

function EnumEmails(){
	varFirstName=$1
	varLastName=$2

	formato1="$varFirstName$varLastName@$domain" #adonisizaguirre@kapa7.com
	formato2="$varFirstName.$varLastName@$domain" #adonis.izaguirre@kapa7.com

  declare -a emails
	emails=("$formato1" "$formato2")

	for i in "${emails[@]}"; 
	do 
		Query $i
		sleep 1
		check=$(cat query.txt | grep -o -E "(250 2.1.5 OK|250 2.1.5 Ok|250 2.1.5 ok)" )
		googleblock=$(cat query.txt | grep -o -E "(450-4.2.1 The user you are trying to contact is receiving mail at a rate)")
		if [ ! -z "$check" ];
		then
 			echo -ne $cGreen"\rAccount found: $i                                  \n"$cNothing
 			echo $i >> accounts.list
 		elif [ ! -z "$googleblock" ];
 			then
 			echo -e $cRed"\rThe user you are trying to contact is receiving mail at a rate that prevents additional messages. try later (maybe google is blocking our queries)"$cNothing
		fi;
	done
	
}

function EnumEmailsByInitials(){
	varFirstName=$1
	varLastName=$2

	formato1="$varFirstName$varLastName@$domain" #aizaguirre@kapa7.com
	formato2="$varFirstName.$varLastName@$domain" #a.izaguirre@kapa7.com

  declare -a emails
	emails=("$formato1" "$formato2")

	for i in "${emails[@]}"; 
	do 
		Query $i
		sleep 1
		check=$(cat query.txt | grep -o -E "(250 2.1.5 OK|250 2.1.5 Ok|250 2.1.5 ok)" )
		googleblock=$(cat query.txt | grep -o -E "(450-4.2.1 The user you are trying to contact is receiving mail at a rate)")
		if [ ! -z "$check" ];
		then
 			echo -ne $cGreen"\rAccount found: $i                                  \n"$cNothing
 			echo $i >> accounts.list
 		elif [ ! -z "$googleblock" ];
 			then
 			echo -e $cRed"\rThe user you are trying to contact is receiving mail at a rate that prevents additional messages. Try later."$cNothing
		fi;
	done
	
}


if [ ! -z "$firstname" ] && [ ! -z "$lastname" ]; ################################################################ if -f and -l was set
then
	EnumEmails $firstname $lastname
	echo -e $cBlue"\naccounts.list file is created when an account is detected."$cNothing

elif [ ! -z "$firstname" ] && [ ! -z "$lastnameFile" ];########################################################### if -f and -L was set
	then
		while read line;
		do
			EnumEmails $firstname $line
		done < $lastnameFile
		echo -e $cBlue"\naccounts.list file is created when an account is detected."$cNothing

	elif [ ! -z "$firstnameFile" ] && [ ! -z "$lastname" ]; ######################################################## if -F and -l was set
		then
			while read line;
			do
				EnumEmails $line $lastname
			done < $firstnameFile
			echo -e $cBlue"\naccounts.list file is created when an account is detected."$cNothing

		elif [ ! -z "$initial" ] && [ ! -z "$lastname" ]; ############################################################ if -i and -l was set
			then
				EnumEmailsByInitials $initial $lastname
				echo -e $cBlue"\naccounts.list file is created when an account is detected."$cNothing

			elif [ ! -z "$initial" ] && [ ! -z "$lastnameFile" ]; ###################################################### if -i and -L was set
				then
					while read line;
					do
						EnumEmailsByInitials $initial $line
					done < $lastnameFile
					echo -e $cBlue"\naccounts.list file is created when an account is detected."$cNothing

				elif [ ! -z "$initialFile" ] && [ ! -z "$lastname" ]; ################################################### if -I and -l was set
					then
						while read line;
						do
							EnumEmailsByInitials $line $lastname
						done < $initialFile
						echo -e $cBlue"\naccounts.list file is created when an account is detected."$cNothing

					elif [ ! -z "$initialFile" ] && [ ! -z "$lastnameFile" ]; ############################################# if -I and -L was set
						then
							while read line;
							do
								while read line2;
								do
									EnumEmailsByInitials $line $line2
								done < $lastnameFile
							done < $initialFile
							echo -e $cBlue"\naccounts.list file is created when an account is detected."$cNothing

							else ############################################################################################# if -F and -L was set
								while read line;
								do
									while read line2;
									do
										EnumEmails $line $line2
									done < $lastnameFile
								done < $firstnameFile
								echo -e $cBlue"\naccounts.list file is created when an account is detected."$cNothing
fi;













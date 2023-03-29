# GReal
email account enumeration tool (O365/GMAIL/GSUITE)

```
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
```
![ezgif com-video-to-gif](https://user-images.githubusercontent.com/94752464/228414183-24cd515e-f6a6-4d9c-9db4-7ede0b039408.gif)


<img width="1068" alt="Screenshot 2023-03-28 at 20 00 26" src="https://user-images.githubusercontent.com/94752464/228407411-356adea0-d03d-46ae-9018-9da6b693d0f0.png">

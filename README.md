# GReal
Gmail/Gsuite account enumeration tool

set execution permissions
```
chmod +x greal.sh
```

optional arguments:
```
-d: set domain
-f: set first name 
-l: set last name
-i: set initials letter for search
-I: set file with initials letter for search
-F: set file with first name list
-L: set file with last name list
-h: show this message
```

To search for only one user:
```
use: ./greal -d example.com -f adonis -l izaguirre

output:
	{adonis}.{izaguirre}@example.com
	{adonis}{izaguirre}@example.com
```

To search one user with lastname list
```
use: ./greal -d example.com -f adonis -L apellidos.txt

output:
	{adonis}.{izaguirre}@example.com
	{adonis}{izaguirre}@example.com
```

To search username list with one lastname
```
use: ./greal -d example.com -F nombres.txt -l izaguirre

output:
	{adonis}.{izaguirre}@example.com
	{adonis}{izaguirre}@example.com
```

To search username list with lastname list
```
use: ./greal -d example.com -F nombres.txt -L apellidos.txt

output:
	{adonis}.{izaguirre}@example.com
	{adonis}{izaguirre}@example.com
```

To search an initial letter with one lastname
```
use: ./greal -d example.com -i a -l izaguirre

output:
	{a}.{izaguirre}@example.com
	{a}{izaguirre}@example.com
```

To search an initial letter with a lastname list
```
use: ./greal -d example.com -i a -L apellidos.txt

output:
	{a}.{izaguirre}@example.com
	{a}{izaguirre}@example.com
```
To search an initial letter list with a lastname list
```
use: ./greal -d example.com -I inicales.txt -L apellidos.txt

output:
	{a}.{izaguirre}@example.com
	{a}{izaguirre}@example.com
```

To search an initial letter list with a lastname
```
use: ./greal -d example.com -I inicales.txt -l izaguirre

output:
	{a}.{izaguirre}@example.com
	{a}{izaguirre}@example.com
```



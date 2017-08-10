# Sites Monitoring Utility

Utility to check the status of sites. At the input - a text file with URLs for verification. At the output, the status of each site is based on the following checks:
 the server responds to the request with the status of HTTP 200,
 the domain name of the site is paid for a given period in advance. And prints result to the console.

## Quickstart

Example of script launch on Linux, Python 3.5:

```
$ pip install -r requirements.txt # alternatively try pip3
$ python3 check_sites_health.py urls.txt

Enter number of days: 30

Sites health report

Domain name          | is 200  | is payed
devman.org           | 1       | 0      
google.com           | 1       | 1      
github.com           | 1       | 1      
      

```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)

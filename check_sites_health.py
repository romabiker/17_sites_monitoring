import datetime
import os
import requests
import sys
import whois


def get_domain_expiration_date(domain_name):
    return whois.whois(domain_name).expiration_date[0]


def get_filepath_from_argv():
    if not len(sys.argv) > 1:
        print('\nEnter: python3 check_sites_health.py "filepath"\n')
        sys.exit()
    path = sys.argv[1]
    if not os.path.exists(path):
        print('\nThis path does not exist\n')
        sys.exit()
    return path


def load_urls4check(path):
    with open(path, 'r') as file_handler:
        return file_handler.read().splitlines()


def is_server_respond_with_200(url):
    return requests.head(url).ok


def output_sites_health_to_console(sites_report):
    print('\nSites health report\n')
    print('{:<20} | {:<7} | {:<7}'.format('Domain name', "is 200", "is payed"))
    for domain_name, (is_200, is_payed) in sites_report.items():
        print('{:<20} | {:<7} | {:<7}'.format(domain_name, is_200, is_payed))
    print()


def prompt_days_ahead():
    try:
        return int(input('\nEnter number of days: '))
    except ValueError as e:
        print('\nYou have enter digits\n')
        print('\nExample: Enter number of days: 30')
        sys.exit()


def request_sites_health(urls, days):
    sites_health = {}
    future_date = datetime.datetime.now() + datetime.timedelta(days=days)
    for url in urls:
        dom_name = url.split('://')[1]
        dom_exp_date = get_domain_expiration_date(dom_name)
        is_200 = is_server_respond_with_200(url)
        sites_health[dom_name] = (
                                    is_200,
                                    dom_exp_date > future_date,
                                    )
    return sites_health


if __name__ == '__main__':
    path = get_filepath_from_argv()
    urls4check = load_urls4check(path)
    payed_days_ahead = prompt_days_ahead()
    sites_health_report = request_sites_health(urls4check, payed_days_ahead)
    output_sites_health_to_console(sites_health_report)

import argparse
import datetime
import os
import requests
import sys
import whois


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--days', default=30, type=int,
                        help='number of the days payed ahead')
    parser.add_argument('-f', '--file', type=argparse.FileType(mode='r'),
                        required=True, help='path to the file of urls')
    return parser


def get_domain_expiration_date(domain_name):
    return whois.whois(domain_name).expiration_date[0]


def load_urls4check(file_handler):
    return file_handler.read().splitlines()


def is_server_respond_with_200(url):
    return requests.head(url).ok


def output_sites_health_to_console(sites_report):
    print('\nSites health report\n')
    print('{:<20} | {:<7} | {:<7}'.format('Domain name', "is 200", "is payed"))
    for domain_name, (is_200, is_payed) in sites_report.items():
        print('{:<20} | {:<7} | {:<7}'.format(domain_name, is_200, is_payed))
    print()


def request_sites_health(urls, days):
    sites_health = {}
    future_date = datetime.datetime.now() + datetime.timedelta(days=days)
    for url in urls:
        dom_name = url.split('://')[1]
        dom_exp_date = get_domain_expiration_date(dom_name)
        is_200 = is_server_respond_with_200(url)
        sites_health[dom_name] = (is_200, dom_exp_date > future_date)
    return sites_health


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    urls4check = load_urls4check(namespace.file)
    payed_days_ahead = namespace.days
    sites_health_report = request_sites_health(urls4check, payed_days_ahead)
    output_sites_health_to_console(sites_health_report)

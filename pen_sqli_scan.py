import sys
from urllib import parse

import requests


# TODO: Implement google dorks search
# TODO: Implement time based vulnerability scan
# TODO: Implement boolean basead vulnerability scan
# TODO: Implement header settings from a file


def is_vulnerable(html):
    sql_errors = []
    sql_errors.append('mysql_fetch_array()')
    sql_errors.append('You have an error in your SQL syntax')

    for sql_error in sql_errors:
        if sql_error in html:
            return True


def make_request(url):
    request_header = {'Host': 'www.bancocn.com',
                      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                    'Chrome/102.0.5005.63 Safari/537.36',
                      'Cookie': 'cf_clearance=6YXvf961g56uoqMB0BV3RKY.bXWxChaEuD3ZA8ydGw0-1654112456-0-150'}
    try:
        request = requests.get(url, headers=request_header)
        if request:
            return request.text
    except Exception as error:
        print('Unexpect error ', error)


def check_union_vulnerability(target):
    parsed_url = parse.urlparse(target)
    query = parsed_url.query
    test_parameters = parse.parse_qs(query)

    for parameter in test_parameters.keys():
        vulnerable_pars = test_parameters.copy()

        for c in '\"\'':
            vulnerable_pars[parameter] = [c]
            vulnerable_query = parse.urlencode(vulnerable_pars, doseq=True)
            vulnerable_url_tuple = parsed_url._replace(query=vulnerable_query)
            vulnerable_url = vulnerable_url_tuple.geturl()

            html = make_request(vulnerable_url)

            if is_vulnerable(html):
                print(f'Parameter {parameter} vulnerable')


def main():
    try:
        target = sys.argv[1]
    except IndexError:
        print('Usage: pen_sqli_scan.py <target_url>')
        sys.exit()

    check_union_vulnerability(target)


if __name__ == '__main__':
    main()

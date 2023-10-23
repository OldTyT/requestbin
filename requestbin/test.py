# -*- coding: utf-8 -*-
import json
import urllib
import random


url = "http://localhost:8000/"
uniq_data = str(random.randint(1000000, 99999999)) + "ENGLISH_РУССКИЙ"  # noqa: E501


def get_status_200(url):
    for i in range(20):
        if urllib.urlopen(url).getcode() == 200:
            print "Status code == 200"
            return
        print "Status code != 200"


def create_bins(url):
    f = urllib.urlopen(url+"api/v1/bins", "private=false")
    if f.getcode() != 200:
        print "Status code != 200 on /api/v1/bins"
        exit(1)
    print "Bin create successful"
    create_json = json.loads(f.read())
    test_request_to_bin(create_json['name'])


def test_request_to_bin(bin_url):
    f = urllib.urlopen(url+bin_url, uniq_data)
    if f.getcode() != 200:
        print "Status code != 200 on /" + bin_url
        exit(1)
    print "Status code == 200 on test bin"
    check_bin_data(bin_url)
    return


def check_bin_data(bin_url):
    f = urllib.urlopen(url+bin_url+"?inspect")
    if f.getcode() != 200:
        print "Status code != 200 on /" + bin_url + "?inspect"
        exit(1)
        return
    print "Status code == 200 on /" + bin_url + "?inspect"
    if uniq_data in f.read():
        print "Uniq data in response"
        exit(0)
        return
    print "Uniq data not in response"
    exit(1)
    return


def check_resp_api_stats(resp, type_value, key):
    try:
        if isinstance(resp[key], type_value):
            print key + " - good"
        else:
            print key + " isn't " + str(type_value)
            print resp
            exit(1)
    except:  # noqa: E722
        print "Error on check - " + key
        print resp
        exit(1)


def check_api_stats(url):
    print url
    f = urllib.urlopen(url+"api/v1/stats")
    print f.getcode()
    if f.getcode() != 200:
        print "Status code != 200 on /api/v1/stats"
        exit(1)
        return
    print "Status code == 200 on /api/v1/stats"
    resp = json.loads(f.read())
    check_resp_api_stats(resp, int, "max_raw_size")
    check_resp_api_stats(resp, unicode, "realm")
    check_resp_api_stats(resp, int, "bin_ttl")
    check_resp_api_stats(resp, int, "bin_count")
    check_resp_api_stats(resp, int, "cleanup_interval")
    check_resp_api_stats(resp, int, "max_requests")
    check_resp_api_stats(resp, unicode, "version")
    check_resp_api_stats(resp, int, "request_count")


def start_tests(url):
    print "Test staring"
    get_status_200(url)
    create_bins(url)
    check_api_stats(url)


start_tests(url)

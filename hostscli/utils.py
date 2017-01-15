#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# vim: fenc=utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
#

"""
File name: utils.py
Author: dhilipsiva <dhilipsiva@gmail.com>
Date created: 2016-12-29
"""

from functools import wraps
from importlib import import_module
from os import listdir, access, W_OK

from hostscli.errors import WebsiteImportError, SudoRequiredError
from hostscli.constants import HOSTS_FILE, FORMAT, WEBSITES_PACKAGE, \
    IMPORT_ERROR, ROOT_ERROR


def hosts_write_access(f):
    @wraps(f)
    def wrapper(website, hosts_file=HOSTS_FILE):
        if not access(hosts_file, W_OK):
            raise SudoRequiredError(ROOT_ERROR)
        return f(website, hosts_file)
    return wrapper


def get_websites():
    websites_path = import_module(WEBSITES_PACKAGE)
    websites_path = websites_path.__file__.replace("__init__.py", "")
    websites = listdir(websites_path)
    websites.remove('__pycache__')
    websites.remove('__init__.py')
    return [website[:-3] for website in websites]


def get_lines(website):
    website = website.lower()
    try:
        module = import_module('%s.%s' % (WEBSITES_PACKAGE, website))
        return [FORMAT % domain for domain in module.DOMAINS]
    except ImportError:
        raise WebsiteImportError(IMPORT_ERROR % website)


@hosts_write_access
def block(website, hosts_file):
    target_lines = get_lines(website)
    with open(hosts_file, 'a') as hosts_file:
        for target_line in target_lines:
            hosts_file.write(target_line)
    return target_line


@hosts_write_access
def unblock(website, hosts_file):
    target_lines = get_lines(website)
    input_lines = open(hosts_file, "r").readlines()
    with open(hosts_file, "w") as hosts_file:
        for input_line in input_lines:
            if input_line not in target_lines:
                hosts_file.write(input_line)
    return target_lines

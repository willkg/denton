#!/usr/bin/env python

from ConfigParser import ConfigParser
import argparse
import requests
import sys


def get_config(cfg_fn):
    cfg = ConfigParser()
    with open(cfg_fn) as fp:
        cfg.readfp(fp)

    return cfg


def get_project(url):
    url = url + '/api/v2/statuses/project_timeline.json'
    args = {
        'count': 100,  # max count
        'slug': 'sumodev',
        'weekly': True
    }

    print url

    resp = requests.get(url, params=args)
    print resp.content


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', type=str, help='Config file')

    args = parser.parse_args()

    try:
        cfg = get_config(args.config)
    except IOError:
        print 'That config file doesn\'t exist. Please make one.'
        print 'See docs for details.'
        return 1

    url = cfg.get('main', 'url')
    url = url.strip('/')

    get_project(url)

    return 0


if __name__ == '__main__':
    sys.exit(main())

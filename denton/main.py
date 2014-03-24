#!/usr/bin/env python

from datetime import datetime, timedelta
from email.mime.text import MIMEText
import ConfigParser
import argparse
import email.utils
import requests
import smtplib
import sys

from .utils import DenTemplate


def get_config(cfg_fn):
    cfg = ConfigParser.ConfigParser()
    with open(cfg_fn) as fp:
        cfg.readfp(fp)

    return cfg


def get_content(url):
    resp = requests.get(url)
    return resp.json()


def parse_datetime(text):
    text = text.strip()
    for fmt in (
            '%Y-%m-%dT%H:%M:%S.%f',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%d'
    ):
        try:
            return datetime.strptime(text, fmt)
        except (TypeError, ValueError):
            pass

    raise ValueError('Cannot parse {0} as a date.'.format(text))


def load_template(template):
    return open(template, 'r').read().strip()


def generate_subject(text):
    today = datetime.now()
    today_bits = dict((m, today.strftime('%' + m))
                      for m in ('a', 'A', 'b', 'B', 'c', 'd', 'H', 'I', 'j',
                                'm', 'M', 'p', 'S', 'U', 'v', 'W', 'x', 'X',
                                'y', 'Y', 'Z'))
    return text.format(**today_bits)


def generate_output(template, subject, content):
    dt = DenTemplate()
    output = dt.templatize(template, {
        'content': content,
        'subject': subject
    })

    return output.rstrip()


def send_mail_smtp(sender, to_list, subject, body, host, port):
    server = smtplib.SMTP(host, port)

    sender_name, sender_addr = email.utils.parseaddr(sender)
    to_list = [email.utils.parseaddr(addr) for addr in to_list]

    for to_name, to_addr in to_list:
        msg = MIMEText(body)
        msg['To'] = email.utils.formataddr((to_name, to_addr))
        msg['From'] = email.utils.formataddr((sender_name, sender_addr))
        msg['Subject'] = subject
        server.sendmail(sender_addr, [to_addr], msg.as_string())

    server.quit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('config', type=str, help='Config file')
    parser.add_argument('--test', action='store_true',
                        help='Test and do not send email')

    args = parser.parse_args()

    try:
        cfg = get_config(args.config)
    except IOError:
        print 'That config file doesn\'t exist. Please make one.'
        print 'See docs for details.'
        return 1

    url = cfg.get('main', 'url')
    url = url.strip('/')

    content = get_content(url)

    if cfg.has_option('main', 'content_field'):
        content_field = cfg.get('main', 'content_field')
        # FIXME - This only handles one level
        content = content[content_field]

    if cfg.has_option('main', 'date_field'):
        date_field = cfg.get('main', 'date_field')
        last_week = datetime.now() - timedelta(days=7)
        content = [
            item for item in content
            if parse_datetime(item[date_field]) > last_week
        ]

    sender = cfg.get('main', 'from')
    to_list = [item.strip() for item in cfg.get('main', 'to').split(',')]
    host = cfg.get('main', 'host')
    port = cfg.get('main', 'port')

    subject = cfg.get('main', 'subject')
    subject = generate_subject(subject)

    template = cfg.get('main', 'template')
    template = load_template(template)
    output = generate_output(template, subject, content)

    if args.test:
        print '%<-----------------------------------------------------'
        print 'From:    ', sender
        print 'To:      ', ','.join(to_list)
        print 'Subject: ', generate_subject(subject)
        print ''
        print output
        print '%<-----------------------------------------------------'
    else:
        send_mail_smtp(sender, to_list, generate_subject(subject), output,
                       host, port)

    print 'Done!'
    return 0


if __name__ == '__main__':
    sys.exit(main())

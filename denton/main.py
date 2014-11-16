#!/usr/bin/env python

from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ConfigParser
import optparse
import email.utils
import smtplib
import sys

from . import __version__
from .utils import DenTemplate, request_url


def get_config(cfg_fn):
    cfg = ConfigParser.ConfigParser()
    with open(cfg_fn) as fp:
        cfg.readfp(fp)

    return cfg


def get_content(url):
    return request_url(url, is_json=True)['json']


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


def interpolate_date(text, date=None):
    """Interpolates date bits in text

    :arg text: the text with things like "%Y-%m-%d" in it to get
        interpolated with the date
    :arg date: the date to interpolate with

    :returns: new text

    """
    if date is None:
        date = datetime.now()
    for m in ('a', 'A', 'b', 'B', 'c', 'd', 'H', 'I', 'j',
              'm', 'M', 'p', 'S', 'U', 'W', 'x', 'X', 'y',
              'Y', 'Z'):
        text = text.replace('%' + m, date.strftime('%' + m))
    return text


def generate_output(template, subject, content):
    dt = DenTemplate()
    output = dt.templatize(template, {
        'content': content,
        'subject': subject,
        'dentonurl': 'https://github.com/willkg/denton',
        'dentonver': __version__
    })

    output = output.rstrip()
    return output


def send_mail_smtp(sender, to_list, subject, body, htmlbody, host, port):
    server = smtplib.SMTP(host, port)

    sender_name, sender_addr = email.utils.parseaddr(sender)
    to_list = [email.utils.parseaddr(addr) for addr in to_list]

    for to_name, to_addr in to_list:
        if htmlbody:
            msg = MIMEMultipart('alternative')
            msg.attach(MIMEText(body.encode('utf-8'), 'plain'))
            msg.attach(MIMEText(htmlbody.encode('utf-8'), 'html'))
        else:
            msg = MIMEText(body.encode('utf-8'))

        msg['To'] = email.utils.formataddr((to_name, to_addr))
        msg['From'] = email.utils.formataddr((sender_name, sender_addr))
        msg['Subject'] = subject
        server.sendmail(sender_addr, [to_addr], msg.as_string())

    server.quit()


def main():
    parser = optparse.OptionParser(usage='usage: %prog [options] config-file',
                                   version='%prog {0}'.format(__version__))
    parser.add_option('--test', action='store_true',
                      help='Test and do not send email')

    (options, args) = parser.parse_args()

    if not args:
        parser.error('Please specify config file.')

    try:
        cfg = get_config(args[0])
    except IOError:
        print 'That config file doesn\'t exist. Please make one.'
        print 'See docs for details.'
        return 1

    url = interpolate_date(cfg.get('main', 'url')).rstrip('/')

    if options.test:
        print url

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
    if cfg.has_option('main', 'host'):
        host = cfg.get('main', 'host')
    else:
        host = 'localhost'
    if cfg.has_option('main', 'port'):
        port = cfg.get('main', 'port')
    else:
        port = '25'

    subject = interpolate_date(cfg.get('main', 'subject')).strip()

    template = cfg.get('main', 'template')
    template = load_template(template)
    output = generate_output(template, subject, content)

    if cfg.has_option('main', 'htmltemplate'):
        htmltemplate = cfg.get('main', 'htmltemplate')
        htmltemplate = load_template(htmltemplate)
        htmloutput = generate_output(htmltemplate, subject, content)
    else:
        htmloutput = None

    if options.test:
        print '%<-----------------------------------------------------'
        print 'From:    ', sender
        print 'To:      ', ','.join(to_list)
        print 'Subject: ', subject
        print ''
        print output
        if htmloutput:
            print ''
            print htmloutput
        print '%<-----------------------------------------------------'
    else:
        send_mail_smtp(sender, to_list, subject, output,
                       htmloutput, host, port)

    print 'Done!'
    return 0


if __name__ == '__main__':
    sys.exit(main())

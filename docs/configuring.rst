===========
Configuring
===========

Denton uses a config.ini style config file. Each config file has a
``[main]`` block that everything is under.

It has the following variables:

url
    The url to retrieve and run Denton on. This should return JSON.

content_field
    (optional) The name of the field where the content you want to
    iterate over is.

    For example, if the returned JSON is::

        {'count': 23, 'results': [{'title': 'foo'}, ...]}

    you'd want to set ``content_field = results``.

date_field
    (optional) The name of the field in each content item that
    Denton can look at to determine the last week of stuff.

    For example, if the returned JSON is::

        {'count': 23,
         'results': [
            {'title': 'foo', 'created': '2014-08-23 12:23:33'},
            ...
          ]}

    You'd want to set ``date_field = created``.

template
    The filename for the template to use to generate the email.

    See :ref:`templates`.

htmltemplate
    (optional) The filename for the HTML version of the template to
    use to generate the email.

    This allows you to have a text version for people who don't have
    HTML-capable email clients and an HTML version of the template for
    people who do.

    See :ref:`templates`.

subject
    The subject line to use. You can use strftime-style variables to
    flesh out the date.

    For example::

        subject = Weekly report for week %U (%Y-%m-%d)

from
    The person this email is from.

    For example::

        from = Me <janet@example.com>

to
    The list of people this email address is to. You can put this on multiple
    lines. Addresses should be comma separated.

    Examples::

        to = you@example.com,
            andyou@example.com

        to = my-department@example.com

host
    (optional) SMTP host to send to. Defaults to "localhost".

    Example::

        host = localhost

port
    (optional) SMTP port to use. Defaults to "25".

    Example::

        port = 25

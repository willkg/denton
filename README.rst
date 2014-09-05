======
denton
======

System for emailing weekly reports with data derived from a JSON API
endpoint.

:Code:         https://github.com/willkg/denton/
:Issues:       https://github.com/willkg/denton/issues
:License:      BSD 3-clause; See LICENSE
:Contributors: See AUTHORS.rst


Status - March 24, 2014
=======================

I threw this together to scratch an itch and implemented as much as
I needed to scratch the itch.

If you have things you want to change, submit an issue or a PR.


Requirements
============

* Python 2.6 or 2.7


Install and run
===============

Run::

    $ git clone https://github.com/willkg/denton
    $ cd denton
    $ python denton-runner.py


Wait, what? No virtual environment? No dependencies? Right.

Also, this isn't being released on PyPI until there's a compelling reason
to do so.


Configure
=========

Denton uses a config file in config file format. Here's a sample::

    [main]
    # URL to retrieve
    url = http://example.com/api/whatever.json

    # Content field for JSON responses where there's metadata
    # at the top and the list of items is under some key (optional)
    # content_field = content

    # Date field to determine the last week of stuff (optional)
    # date_field = created

    # Template file for email
    template = template.tmpl

    # HTML template file for email
    htmltemplate = template.html.tmpl

    # subject for the email
    subject = Weekly report for week %U (%Y-%m-%d)

    # Who is this from?
    from = Me <janet@example.com>

    # List of email addresses this is sent to
    to = you@example.com,
        andyou@example.com

    # SMTP Host (defaults to 'localhost')
    # host = localhost

    # SMTP port (defaults to 25)
    # port = 25


Templates
=========

Denton has a built-in templating engine that's kind of mediocre and
small. It allows for eval parts with ``{{`` and ``}}`` and also has
some rough blocks like ``if``, ``else``, and ``for``. It also has
support for eval filters.

Here's an example::

    Total entries: {{ len(content) }}

    {% if content %}
    {% for item in content %}
    **{{ item['created']|datetime('%c') }} :: {{ item['user']['name'] }}**
    http://standu.ps/status/{{ item['id'] }}

    {{ item['content'] }}


    {% endfor %}
    {% else %}
    Nothing happened.

    {% endif %}


Locals dict is carried throughout so you can modify the environment as you
go along.

Whitespace handling kind of sucks. Best to left-align all block tags
and give it an extra carriage return if you need one before and after
block tags.

See documentation for more details.

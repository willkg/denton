======
denton
======

System for emailing weekly reports with data derived from JSON API
endpoints.

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

    # Template file to use for each item in the list
    template = template.tmpl

    # subject for the email
    subject = Weekly report for week {U} ({Y}-{m}-{d})

    # Who is this from?
    from = Me <janet@example.com>

    # List of email addresses this is sent to
    to = you@example.com,
        andyou@example.com

    # SMTP Host (defaults to 'localhost')
    # host = localhost

    # SMTP port (defaults to 25)
    # port = 25


The template format is atrocious. It allows for exec and eval parts. Here's
an example::

    
    Total entries: {{ len(content) }}


    {%
    for item in content:
        print('**{created} :: {user[name]}**'.format(
            created=item['created'], user=item['user']))
        print('http://standu.ps/status/{id}'.format(id=item['id']))
        print('')
        print('{content}'.format(content=item['content']))
        print('')
        print('')
    %}


The eval block is wrapped in ``{{`` and ``}}``.

The exec block is wrapped in ``{%`` and ``%}``.

Locals dict is carried throughout so you can modify the environment as you
go along.

.. Note::

   This is a mediocre template format. I may fiddle with it some more, but
   it was good enough for my purposes.
